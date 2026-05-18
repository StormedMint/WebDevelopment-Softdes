from flask import Blueprint, render_template
from .db import get_db_connection
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from pathlib import Path
import pandas as pd

admin = Blueprint('admin',__name__)


@admin.route('/AdminDashboard')
def AdminDashboard():
    return render_template("AdminDashboard.html")

@admin.route('/LibrarianDashboard')
def LibrarianDashboard():
    return render_template("LibrarianDashboard.html")

@admin.route('/dashboard') #Smart Routing para mabalik sa corresponding dashboards
def dashboard():

    #Session is para ma-remember ng app sino yung user between pages.
    role = session.get('admin_type')

    if role == "High Admin":
        return redirect(url_for('admin.AdminDashboard'))

    elif role == "Librarian":
        return redirect(url_for('admin.LibrarianDashboard'))

    return redirect(url_for('auth.AdminLogIn'))

@admin.route('/AdminAccManagement')
def AdminAccManagement():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT username, password, type_admin FROM admin_accounts")
    admins = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "AdminAccManagement.html",
        admins=admins
    )

@admin.route('/clear_selected_admin', methods=['POST'])
def clear_selected_admin():
    session.pop("selected_admin_username", None)
    return {"success": True}

@admin.route('/set_selected_admin', methods=['POST'])
def set_selected_admin():
    username = request.form.get('username', '').strip()

    if not username:
        return {"success": False, "message": "No username received"}

    session["selected_admin_username"] = username

    return {"success": True, "selected_admin_username": username}

@admin.route('/handle_admin_actions', methods=['POST'])
def handle_admin_actions():

    action = request.form.get('action')
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # ADD function
        if action == "add":

            type_admin = "Librarian"

            if not all([username, password]):
                flash("All fields required for adding!")
                return redirect(url_for('admin.AdminAccManagement'))

            cursor.execute("""
                SELECT username 
                FROM admin_accounts 
                WHERE username = %s
            """, (username,))

            if cursor.fetchone():
                flash("Username already exists!")
                return redirect(url_for('admin.AdminAccManagement'))

            cursor.execute("""
                INSERT INTO admin_accounts (username, password, type_admin)
                VALUES (%s, %s, %s)
            """, (username, password, type_admin))

            db.commit()
            flash("Admin added successfully!")

        elif action == "edit":

            old_username = session.get("selected_admin_username")

            if not old_username:
                flash("Please select an admin account first!")
                return redirect(url_for('admin.AdminAccManagement'))

            if not all([username, password]):
                flash("Username and password are required to edit!")
                return redirect(url_for('admin.AdminAccManagement'))

            # Check if old username still exists
            cursor.execute("""
                SELECT username
                FROM admin_accounts
                WHERE username = %s
            """, (old_username,))

            existing_old = cursor.fetchone()

            if not existing_old:
                flash("Admin account not found!")
                return redirect(url_for('admin.AdminAccManagement'))

            # If username was changed, check duplicate
            if username != old_username:
                cursor.execute("""
                    SELECT username
                    FROM admin_accounts
                    WHERE username = %s
                """, (username,))

                existing_new = cursor.fetchone()

                if existing_new:
                    flash("Username already exists!")
                    return redirect(url_for('admin.AdminAccManagement'))

            # Update username and password
            cursor.execute("""
                UPDATE admin_accounts
                SET username = %s,
                    password = %s
                WHERE username = %s
            """, (username, password, old_username))

            db.commit()

            # Update session to new username
            session["selected_admin_username"] = username

            flash("Admin account updated successfully!")

        # DELETE function
        elif action == "delete":

            selected_username = session.get("selected_admin_username")
            type_admin = request.form.get('type_admin', '').strip()

            if not selected_username:
                flash("Please select an admin account first!")
                return redirect(url_for('admin.AdminAccManagement'))
            
            if type_admin == "High Admin":
                flash("High Admin Cannot Be Deleted!")
                return redirect(url_for('admin.AdminAccManagement'))

            cursor.execute("""
                SELECT * 
                FROM admin_accounts 
                WHERE username = %s
            """, (selected_username,))

            existing = cursor.fetchone()

            if not existing:
                flash("Admin account not found!")
                return redirect(url_for('admin.AdminAccManagement'))

            cursor.execute("""
                DELETE FROM admin_accounts 
                WHERE username = %s
            """, (selected_username,))

            db.commit()

            session.pop("selected_admin_username", None)

            flash("Admin deleted successfully!")

    except Exception as e:
        db.rollback()
        flash(f"Error: {e}")

    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.AdminAccManagement'))

@admin.route('/admin_search_username', methods=['POST'])
def admin_search_username():

    username = request.form.get('searchUsername').strip()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # STRICT MATCH (ONLY 1 USER)
    cursor.execute("""
        SELECT username, password, type_admin
        FROM admin_accounts
        WHERE username = %s
    """, (username,))

    admin = cursor.fetchone()

    cursor.close()
    db.close()

    # convert single result into list (so Jinja table still works)
    admins = [admin] if admin else []

    return render_template(
        "AdminAccManagement.html",
        admins=admins #Pinapasa sa html value
    )

@admin.route('/UserAccManagement')
def UserAccManagement():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, fname, lname, account_type, course_section
        FROM user_accounts
    """)

    users = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("UserAccManagement.html", users=users)

@admin.route('/clear_selected_user', methods=['POST'])
def clear_selected_user():
    session.pop("selected_user_id", None)
    return {"success": True}

@admin.route('/set_selected_user', methods=['POST'])
def set_selected_user():
    user_id = request.form.get('user_id', '').strip()

    if not user_id:
        return {"success": False, "message": "No user ID received"}

    session["selected_user_id"] = user_id

    return {"success": True, "selected_user_id": user_id}

@admin.route('/handle_user_actions', methods=['POST'])
def handle_user_actions():

    action = request.form.get('action')
    new_id = request.form.get('id', '').strip()
    fname = request.form.get('fname', '').strip()
    lname = request.form.get('lname', '').strip()
    course_section = request.form.get('course_section', '').strip()
    account_type = request.form.get('account_type', '').strip()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        if action == "edit":

            old_id = session.get("selected_user_id")

            if not old_id:
                flash("Please select a user from the table first!")
                return redirect(url_for('admin.UserAccManagement'))

            if not all([new_id, fname, lname, course_section, account_type]):
                flash("Please fill in all fields!")
                return redirect(url_for('admin.UserAccManagement'))

            valid_id = (
                (len(new_id) == 11 and re.fullmatch(r"\d{4}-\d{6}", new_id)) or
                (len(new_id) == 10 and new_id.isdigit())
            )

            if not valid_id:
                flash("Invalid ID format!")
                return redirect(url_for('admin.UserAccManagement'))

            # Check if new ID already exists
            if new_id != old_id:
                cursor.execute("""
                    SELECT id 
                    FROM user_accounts 
                    WHERE id = %s
                """, (new_id,))

                existing = cursor.fetchone()

                if existing:
                    flash("ID already exists!")
                    return redirect(url_for('admin.UserAccManagement'))

            cursor.execute("""
                UPDATE user_accounts
                SET id = %s,
                    fname = %s,
                    lname = %s,
                    course_section = %s,
                    account_type = %s
                WHERE id = %s
            """, (
                new_id,
                fname,
                lname,
                course_section,
                account_type,
                old_id
            ))

            db.commit()

            if cursor.rowcount == 0:
                flash("User not found!")
            else:
                session["selected_user_id"] = new_id
                flash("User updated successfully!")

        elif action == "delete":

            old_id = session.get("selected_user_id")

            if not old_id or new_id != old_id:
                flash("Please select a user from the table first!")
                return redirect(url_for('admin.UserAccManagement'))

            cursor.execute("""
                SELECT * 
                FROM user_accounts 
                WHERE id = %s
            """, (old_id,))

            user = cursor.fetchone()

            if not user:
                flash("User not found!")
                return redirect(url_for('admin.UserAccManagement'))

            cursor.execute("""
                INSERT INTO deleted_user_accounts
                (id, fname, lname, account_type, course_section, picture)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user["id"],
                user["fname"],
                user["lname"],
                user["account_type"],
                user["course_section"],
                user["picture"]
            ))

            cursor.execute("""
                DELETE FROM user_accounts
                WHERE id = %s
            """, (old_id,))

            db.commit()

            session.pop("selected_user_id", None)

            flash("User archived and deleted!")

    except Exception as e:
        db.rollback()
        flash(f"Error: {e}")

    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.UserAccManagement'))

@admin.route('/search_user', methods=['POST'])
def search_user():

    action = request.form.get('action')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    users = []

    # ID search
    if action == "search_id":
        search_id = request.form.get('search_id', '').strip()

        # VALIDATION dapat digit sila or make dash sa pang lima (profs)
        valid_id = (
            search_id.isdigit() or
            (len(search_id) == 11 and search_id[4] == "-" and re.fullmatch(r"\d{4}-\d{6}", search_id))
        )

        if not valid_id:
            cursor.close()
            db.close()
            flash("Please Enter a Valid ID.")
            return redirect(url_for('admin.UserAccManagement'))
        
        cursor.execute("""
            SELECT * FROM user_accounts
            WHERE id = %s
        """, (search_id,))

        users = cursor.fetchall()

    # NAME search 
    elif action == "search_name":

        search_name = request.form.get('search_name', '').strip()

        if not search_name:
            flash("Please enter a name before trying to search!")
            return redirect(url_for('admin.UserAccManagement'))


        # VALIDATION kung may numbers
        if any(char.isdigit() for char in search_name):
            cursor.close()
            db.close()
            return redirect(url_for('admin.UserAccManagement'))

        cursor.execute("""
            SELECT * FROM user_accounts
            WHERE fname LIKE %s
               OR lname LIKE %s
        """, (f"%{search_name}%", f"%{search_name}%"))

        users = cursor.fetchall()

    cursor.close()
    db.close()

    # pag wala nahanap refresh lang page
    if not users:
        flash("No users found!")
        return redirect(url_for('admin.UserAccManagement'))

    return render_template("UserAccManagement.html", users=users)

@admin.route('/LogTableManagement')
def LogTableManagement():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, fname, lname, account_type, course_section, date
        FROM log_table
        ORDER BY date DESC
    """)
    logs = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("LogTableManagement.html", logs=logs)

@admin.route('/log_search_user', methods=['POST'])
def log_search_user():

    action = request.form.get('action')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    users = []

    # ID search
    if action == "search_id":
        search_id = request.form.get('search_id', '').strip()

        if not search_id:
            flash("Please enter an ID!")
            return redirect(url_for('admin.LogTableManagement'))


        # VALIDATION dapat digit sila or make dash sa pang lima (profs)
        valid_id = (
            search_id.isdigit() or
            (len(search_id) == 11 and search_id[4] == "-" and re.fullmatch(r"\d{4}-\d{6}", search_id))
        )

        if not valid_id:
            cursor.close()
            db.close()
            flash("Please enter a valid ID")
            return redirect(url_for('admin.LogTableManagement'))
        
        cursor.execute("""
            SELECT * FROM log_table
            WHERE id = %s
        """, (search_id,))

        users = cursor.fetchall()

        if not users:
            flash("ID not found!")
            return redirect(url_for('admin.LogTableManagement'))

    # NAME search 
    elif action == "search_name":

        search_name = request.form.get('search_name', '').strip()

        # VALIDATION kung may numbers
        if any(char.isdigit() for char in search_name):
            cursor.close()
            db.close()
            return redirect(url_for('admin.LogTableManagement'))

        cursor.execute("""
            SELECT * FROM log_table
            WHERE fname LIKE %s
               OR lname LIKE %s
        """, (f"%{search_name}%", f"%{search_name}%"))

        users = cursor.fetchall()

        cursor.close()
        db.close()
        flash("Invalid Name.")

    # pag wala nahanap refresh lang page
    if not users:
        return redirect(url_for('admin.LogTableManagement'))

    return render_template("LogTableManagement.html", logs=users)


@admin.route('/DeletedUserManagement')
def DeletedUserManagement():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM deleted_user_accounts
    """)
    archive = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("DeletedUserManagement.html", archive=archive)

@admin.route('/restore_user', methods=['POST'])
def restore_user():

    user_id = request.form.get('id')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True, buffered=True)

    #Duplication check sa main table
    cursor.execute("""
        SELECT * FROM user_accounts
        WHERE id = %s
    """, (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        db.close()
        flash("User Account Already Exist")
        return redirect(url_for('admin.DeletedUserManagement'))
        #flash "User already exists in main table")

    #Kukunin sa archive table
    cursor.execute("""
        SELECT * FROM deleted_user_accounts
        WHERE id = %s
    """, (user_id,))
    archived_user = cursor.fetchone()

    if not archived_user:
        cursor.close()
        db.close()
        flash("User not found")
        return redirect(url_for('admin.DeletedUserManagement'))
        # flash "User not found in archive"

    #Babalik sa user_accounts
    cursor.execute("""
        INSERT INTO user_accounts
        (id, fname, lname, account_type, course_section, picture)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        archived_user["id"],
        archived_user["fname"],
        archived_user["lname"],
        archived_user["account_type"],
        archived_user["course_section"],
        archived_user["picture"]
    ))

    #DELETE sa archive
    cursor.execute("""
        DELETE FROM deleted_user_accounts
        WHERE id = %s
    """, (user_id,))
    flash("Restored Successfully!")

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('admin.DeletedUserManagement'))

@admin.route('/deleted_search_user', methods=['POST'])
def deleted_search_user():

    action = request.form.get('action')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    archive = []

    # ID search
    if action == "search_id":
        search_id = request.form.get('search_id', '').strip()

        if not search_id:
            cursor.close()
            db.close()
            flash("Enter an ID!")
            return redirect(url_for('admin.DeletedUserManagement'))


        # VALIDATION dapat digit sila or make dash sa pang lima (profs)
        valid_id = (
            search_id.isdigit() or
            (len(search_id) == 11 and search_id[4] == "-" and re.fullmatch(r"\d{4}-\d{6}", search_id))
        )

        if not valid_id:
            cursor.close()
            db.close()
            flash("Enter a valid ID format!")
            return redirect(url_for('admin.DeletedUserManagement'))
        
        cursor.execute("""
            SELECT * FROM deleted_user_accounts
            WHERE id = %s
        """, (search_id,))

        archive = cursor.fetchall()

    # NAME search 
    elif action == "search_name":

        search_name = request.form.get('search_name', '').strip()

        if not search_name:
            cursor.close()
            db.close()
            flash("Enter a Name First!")
            return redirect(url_for('admin.DeletedUserManagement'))

        # VALIDATION kung may numbers
        if any(char.isdigit() for char in search_name):
            cursor.close()
            db.close()
            return redirect(url_for('admin.DeletedUserManagement'))

        cursor.execute("""
            SELECT * FROM deleted_user_accounts
            WHERE fname LIKE %s
               OR lname LIKE %s
        """, (f"%{search_name}%", f"%{search_name}%"))

        archive = cursor.fetchall()

        cursor.close()
        db.close()

    # pag wala nahanap refresh lang page
    if not archive:
        flash("User Account not found!")
        return redirect(url_for('admin.DeletedUserManagement'))

    return render_template("DeletedUserManagement.html", archive=archive)

@admin.route('/CapacityTrackingAdminSide')
def CapacityTrackingAdminSide():
    return render_template("CapacityTrackingAdminSide.html") # Added missing .html extension

@admin.route('/ReservedRoomsTracker')
def ReservedRoomsTracker():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM room_reservation")
    reservations = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("ReservedRoomsTracker.html", reservations=reservations) 

@admin.route('/handle_reservation', methods=['POST'])
def handle_reservation():

    action = request.form.get('action')

    room = request.form.get('room')
    date = request.form.get('date')
    time = request.form.get('time')
    rep = request.form.get('representative')
    reason = request.form.get('reason')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # ADD RESERVATION

    if action == "add":

        if not all([room, date, time, rep, reason]):
            flash("Please finish all the fields.")
            return redirect(url_for('admin.ReservedRoomsTracker'))

        if room == "all-rooms":
            flash("Please select a room.")
            return redirect(url_for('admin.ReservedRoomsTracker'))

        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d/%Y")
        except ValueError:
            flash("Invalid date format.")
            return redirect(url_for('admin.ReservedRoomsTracker'))

        cursor.execute("""
            SELECT * FROM room_reservation
            WHERE room = %s AND date = %s AND time = %s
        """, (room, formatted_date, time))

        existing = cursor.fetchone()

        if existing:
            cursor.close()
            db.close()
            flash("Room is already booked at this date and time!")
            return redirect(url_for('admin.ReservedRoomsTracker'))

        cursor.execute("""
            INSERT INTO room_reservation (room, date, time, rep_name, reason)
            VALUES (%s, %s, %s, %s, %s)
        """, (room, formatted_date, time, rep, reason))

        db.commit()
        cursor.close()
        db.close()

        flash("Reservation added successfully!")
        return redirect(url_for('admin.ReservedRoomsTracker'))
    
    # DELETE + ARCHIVE

    elif action == "delete":

        # find matching record (match lahat ng records)
        cursor.execute("""
            SELECT * FROM room_reservation
            WHERE room=%s AND date=%s AND time=%s AND rep_name=%s
            LIMIT 1
        """, (room, date, time, rep))

        row = cursor.fetchone()

        if row:

            # archive first
            cursor.execute("""
                INSERT INTO deleted_room_reservation
                (room, date, time, rep_name, reason)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                row["room"],
                row["date"],
                row["time"],
                row["rep_name"],
                row["reason"]
            ))

            # delete original
            cursor.execute("""
                DELETE FROM room_reservation
                WHERE room=%s AND date=%s AND time=%s AND rep_name=%s
            """, (room, date, time, rep))

            db.commit()

        cursor.close()
        db.close()

        return redirect(url_for('admin.ReservedRoomsTracker'))

    cursor.close()
    db.close()
    return redirect(url_for('admin.ReservedRoomsTracker'))

@admin.route('/filter_reservation_rep', methods=['POST'])
def filter_reservation_rep():

    rep = request.form.get('search_rep', '').strip()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM room_reservation
        WHERE rep_name LIKE %s
    """, (f"%{rep}%",))

    reservations = cursor.fetchall()

    cursor.close()
    db.close()

    
    if not reservations:
        flash("No Reservations Under Name Searched!")
        return redirect(url_for('admin.ReservedRoomsTracker'))

    return render_template(
        "ReservedRoomsTracker.html",
        reservations=reservations
    )

@admin.route('/filter_reservation_date', methods=['POST'])
def filter_reservation_date():

    date = request.form.get('search_date')

    if not date:
        return redirect(url_for('admin.ReservedRoomsTracker'))

    # convert YYYY-MM-DD → MM/DD/YYYY
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%m/%d/%Y")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM room_reservation
        WHERE date = %s
    """, (formatted_date,))

    reservations = cursor.fetchall()

    if not reservations:
        flash("No Reservations Under The Date Searched!")
        return redirect(url_for('admin.ReservedRoomsTracker'))

    cursor.close()
    db.close()

    return render_template(
        "ReservedRoomsTracker.html",
        reservations=reservations
    )

@admin.route('/filter_reservation_room', methods=['POST'])
def filter_reservation_room():

    room = request.form.get('filter-status')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if room == "all-rooms":
        cursor.execute("SELECT * FROM room_reservation")
    else:
        cursor.execute("""
            SELECT * FROM room_reservation
            WHERE room = %s
        """, (room,))

    reservations = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "ReservedRoomsTracker.html",
        reservations=reservations
    )

@admin.route('/LostAndFound')
def LostAndFound():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM lost_and_found")
    items = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("LostAndFound.html", items=items)

@admin.route('/handle_lost_found', methods=['POST'])
def handle_lost_found():

    action = request.form.get('action')

    item_name = request.form.get('item_name')
    description = request.form.get('description')
    place = request.form.get('place')
    finder_name = request.form.get('finder_name')
    phone = request.form.get('phone')
    status = request.form.get('status')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # ADD ITEM
    if action == "add":

        if not all([item_name, description, place, finder_name, phone, status]):
            flash("All fields are required!")
            return redirect(url_for('admin.LostAndFound'))
        
        if len(phone) !=11:
            flash("Please Enter a correct phone number!")
            return redirect(url_for('admin.LostAndFound'))

        cursor.execute("""
            INSERT INTO lost_and_found
            (item_name, description, place, name, contact_number, status, date_time)
            VALUES (%s,%s,%s,%s,%s,%s,NOW())
        """, (item_name, description, place, finder_name, phone, status))

        db.commit()
        flash("Item added successfully!")

    # EDIT ITEM
    elif action == "edit":

        cursor.execute("""
            SELECT * FROM lost_and_found
            WHERE item_name = %s
        """, (item_name,))
        existing = cursor.fetchone()

        if not existing:
            flash("Item not found!")
            return redirect(url_for('admin.LostAndFound'))

        cursor.execute("""
            UPDATE lost_and_found
            SET description=%s,
                place=%s,
                name=%s,
                contact_number=%s,
                status=%s
            WHERE item_name=%s
        """, (description, place, finder_name, phone, status, item_name))

        db.commit()
        flash("Item updated!")

    # DELETE (WITH ARCHIVE)
    elif action == "delete":

        cursor.execute("""
            SELECT * FROM lost_and_found
            WHERE item_name=%s
        """, (item_name,))
        item = cursor.fetchone()

        if not item:
            flash("Item not found!")
            return redirect(url_for('admin.LostAndFound'))

        # Move to archive
        cursor.execute("""
            INSERT INTO deleted_lost_and_found
            (item_name, description, place, name, contact_number, status, date_time)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            item["item_name"],
            item["description"],
            item["place"],
            item["name"],
            item["contact_number"],
            item["Status"],
            item["date_time"]
        ))

        # Delete from main
        cursor.execute("""
            DELETE FROM lost_and_found
            WHERE item_name=%s
        """, (item_name,))

        db.commit()
        flash("Item archived and deleted!")

    # =========================
    cursor.close()
    db.close()

    return redirect(url_for('admin.LostAndFound'))

@admin.route('/search_lost_item', methods=['POST'])
def search_lost_item():

    search_item = request.form.get('search_item', '').strip()

    # VALIDATION (no empty, optional: no numbers restriction if you want)
    if not search_item:
        flash("No item found!")
        return redirect(url_for('admin.LostAndFound'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM lost_and_found
        WHERE item_name LIKE %s
    """, (f"%{search_item}%",))

    items = cursor.fetchall()

    cursor.close()
    db.close()

    # If nothing found → refresh page
    if not items:
        return redirect(url_for('admin.LostAndFound'))

    # Replace table with results
    return render_template("LostAndFound.html", items=items)

@admin.route('/search_item_status', methods=['POST'])
def search_item_status():

    status = request.form.get('status')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if status == "all":
        cursor.execute("SELECT * FROM lost_and_found")
    else:
        cursor.execute("""
            SELECT * FROM lost_and_found
            WHERE status = %s
        """, (status,))

    items = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("LostAndFound.html", items=items)

@admin.route('/search_lost_date', methods=['POST'])
def search_lost_date():

    search_date = request.form.get('date')

    if not search_date:
        return redirect(url_for('admin.LostAndFound'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM lost_and_found
        WHERE DATE(date_time) = %s
    """, (search_date,))

    items = cursor.fetchall()

    cursor.close()
    db.close()

    # If nothing found -> refresh page
    if not items:
        flash("No lost item in this date.")
        return redirect(url_for('admin.LostAndFound'))

    return render_template("LostAndFound.html", items=items)

#for clear all sa user accounts
@admin.route('/clear_all_user', methods=['POST'])
def clear_all_user():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM user_accounts")
        users = cursor.fetchall()

        #lipat sa archive table
        for user in users:
            cursor.execute("""
                INSERT INTO deleted_user_accounts
                (id, fname, lname, account_type, course_section, picture)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user["id"],
                user["fname"],
                user["lname"],
                user["account_type"],
                user["course_section"],
                user["picture"]
            ))

        #delete all
        cursor.execute("DELETE FROM user_accounts")

        db.commit()

    except Exception as e:
        db.rollback()
        flash("Error clearing users:", e)

    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.UserAccManagement'))

#for clear all sa admin accounts
@admin.route('/clear_all_admin', methods=['POST'])
def clear_all_admin():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""SELECT * FROM admin_accounts WHERE type_admin != %s""", ('High Admin',))
        users = cursor.fetchall()

        #lipat sa archive table
        for user in users:
            cursor.execute("""
                INSERT INTO deleted_admin_accounts
                (username, password, type_admin)
                VALUES (%s, %s, %s)
            """, (
                user["username"],
                user["password"],
                user["type_admin"],
            ))

        #delete all data
        cursor.execute("""DELETE FROM admin_accounts WHERE type_admin != %s""", ('High Admin',))

        db.commit()

    except Exception as e:
        db.rollback()
        flash("Error clearing users:", e)

    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.AdminAccManagement'))

#for clear all sa deleted user accounts
@admin.route('/clear_all_deleted_user', methods=['POST'])
def clear_all_deleted_user():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("DELETE FROM deleted_user_accounts")
        db.commit()

    except Exception as e:
        db.rollback()
        flash("Error clearing users:", e)

    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.DeleteUserManagement'))

#for clear all sa log table
@admin.route('/clear_all_log_table', methods=['POST'])
def clear_all_log_table():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("DELETE FROM log_table")
        db.commit()

    except Exception as e:
        db.rollback()
        flash("Error clearing log table:", e)

    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.LogTableManagement'))

#for clear all sa room reservation
@admin.route('/clear_all_rooms', methods=['POST'])
def clear_all_rooms():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:

        cursor.execute("SELECT * FROM room_reservation")
        reservations = cursor.fetchall()

        if not reservations:
            flash("No reserved rooms to clear!")
            return redirect(url_for('admin.ReservedRoomsTracker'))

        #lipat sa archive table
        for reservation in reservations:
            cursor.execute("""
                INSERT INTO deleted_room_reservation
                (room, date, time, rep_name, reason)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                reservation["room"],
                reservation["date"],
                reservation["time"],
                reservation["rep_name"],
                reservation["reason"]
            ))

        #delete all
        cursor.execute("DELETE FROM room_reservation")
        db.commit()

    except Exception as e:
        db.rollback()
        flash("Error clearing reserved rooms:", e)

    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.ReservedRoomsTracker'))

#for clear all sa lost and found table
@admin.route('/clear_all_lost', methods=['POST'])
def clear_all_lost():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        
        cursor.execute("SELECT * FROM lost_and_found")
        items = cursor.fetchall()

        if not items:
            flash("No items to clear!")
            return redirect(url_for('admin.ReservedRoomsTracker'))

        #lipat sa archive table
        for item in items:
            cursor.execute("""
                INSERT INTO deleted_lost_and_found
                (item_name, description, date_time, place, name,
                           contact_number, Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                item["item_name"],
                item["description"],
                item["date_time"],
                item["place"],
                item["name"],
                item["contact_number"],
                item["Status"]
            ))

        cursor.execute("DELETE FROM lost_and_found")
        db.commit()

    except Exception as e:
        db.rollback()
        flash("Error clearing lost items:", e)

    finally:
        cursor.close()
        db.close()

    return redirect(url_for('admin.LostAndFound'))

#for capacity tracking admin side add/deduct
@admin.route("/update-capacity", methods=["POST"])
def update_capacity():
    area = request.form.get("area")
    action = request.form.get("action")
    amount = request.form.get("amount")

    if not area or not action or not amount:
        return redirect(url_for("admin.CapacityTrackingAdminSide"))

    if not amount.isdigit():
        return redirect(url_for("admin.CapacityTrackingAdminSide"))

    amount = int(amount)

    if amount <= 0:
        return redirect(url_for("admin.CapacityTrackingAdminSide"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT current, capacity FROM vacancy_table WHERE area = %s",
        (area,)
    )

    room = cursor.fetchone()

    if room:
        current = room["current"]
        capacity = room["capacity"]

        if action == "add":
            new_current = current + amount

            if new_current > capacity:
                cursor.close()
                conn.close()
                return redirect(url_for("admin.CapacityTrackingAdminSide"))

        elif action == "deduct":
            new_current = current - amount

            if new_current < 0:
                cursor.close()
                conn.close()
                return redirect(url_for("admin.CapacityTrackingAdminSide"))

        else:
            cursor.close()
            conn.close()
            return redirect(url_for("admin.CapacityTrackingAdminSide"))

        cursor.execute(
            "UPDATE vacancy_table SET current = %s WHERE area = %s",
            (new_current, area)
        )

        conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("admin.CapacityTrackingAdminSide"))

#Exporting UserAccManagement into excel
@admin.route('/export/<table_name>')
def export_table(table_name):

    db = get_db_connection()

    # Read table
    df = pd.read_sql(f"SELECT * FROM {table_name}", db)

    db.close()

    # Desktop path
    desktop_path = Path.home() / "Desktop"

    # Create Desktop if missing
    desktop_path.mkdir(parents=True, exist_ok=True)

    # Filename
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_path = desktop_path / f"{table_name}_{current_date}.xlsx"

    # Export
    df.to_excel(file_path, index=False)

    flash(f"Exported successfully to Desktop: {file_path}")

    return redirect(request.referrer or url_for('admin.UserAccManagement'))