from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .db import get_db_connection
import base64
import re

auth = Blueprint('auth',__name__)

#routing for the different html


@auth.route('/UserSignUpPage', methods=['GET', 'POST'])
def UserSignUpPage():

    if request.method == 'POST':

        user_id = request.form.get('id')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        course = request.form.get('course_section')
        image_data = request.form.get('picture')

        if not all([user_id, fname, lname, course, image_data]):
            flash("Please fill in all fields!")
            return redirect(url_for('auth.UserSignUpPage'))

        user_id = user_id.strip()
        fname = fname.strip()
        lname = lname.strip()

        if any(char.isdigit() for char in fname) or any(char.isdigit() for char in lname):
            flash("Names must NOT contain numbers!")
            return redirect(url_for('auth.UserSignUpPage'))

        account_type = get_account_type(user_id)

        if not account_type:
            flash("Invalid ID format!")
            return redirect(url_for('auth.UserSignUpPage'))

        # remove base64 header
        try:
            image_data = image_data.split(",")[1]
            img_bytes = base64.b64decode(image_data)
        except:
            flash("Invalid image!")
            return redirect(url_for('auth.UserSignUpPage'))

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        #Validation for duplication
        cursor.execute("SELECT * FROM user_accounts WHERE id = %s", (user_id,))
        if cursor.fetchone():
            flash("User already exists!")
            cursor.close()
            db.close()
            return redirect(url_for('auth.UserSignUpPage'))

        cursor.execute("""
            INSERT INTO user_accounts
            (id, fname, lname, account_type, course_section, picture)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (user_id, fname, lname, account_type, course, img_bytes))

        db.commit()
        cursor.close()
        db.close()

        flash("Sign Up Successful!")
        return redirect(url_for('auth.UserLoginPage'))

    return render_template("UserSignupPage.html")

@auth.route('/UserLoginPage', methods=['GET', 'POST'])
def UserLoginPage():
    user_data = None
    verified = False

    if request.method == 'POST':
        user_id = request.form.get('user-id')

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM user_accounts WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()

        cursor.close()
        connection.close()

        if user_data:
            verified = True

            import base64
            user_data["full_name"] = f"{user_data['fname']} {user_data['lname']}"

            if user_data.get("picture"):
                user_data["picture"] = base64.b64encode(user_data["picture"]).decode("utf-8")

            # INSERTION SA LOG TABLE
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO log_table
                (id, fname, lname, account_type, course_section, date)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (
                user_data["id"],
                user_data["fname"],
                user_data["lname"],
                user_data["account_type"],
                user_data["course_section"]
            ))

            connection.commit()
            cursor.close()
            connection.close()

    # THIS MUST ALWAYS RUN
    return render_template(
        "UserLoginPage.html",
        user=user_data,
        verified=verified
    )

@auth.route('/AdminLogIn', methods=['POST', 'GET'])
def AdminLogIn():
    admin_data = None

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # 1. Connect DB
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # 2. Check if user exists
        cursor.execute(
            "SELECT * FROM admin_accounts WHERE username = %s",
            (username,)
        )
        admin_data = cursor.fetchone()

        # 3. If no user found
        if not admin_data:
            flash("Admin does not exist!")
            cursor.close()
            db.close()
            return render_template("AdminLogIn.html", admin=None)

        # 4. Check password
        if admin_data["password"] != password:
            flash("Incorrect password!")
            cursor.close()
            db.close()
            return render_template("AdminLogIn.html", admin=None)

        # 5. Check admin type
        if admin_data["type_admin"] not in ["High Admin", "Librarian"]:
            flash("Unauthorized admin type!")
            cursor.close()
            db.close()
            return render_template("AdminLogIn.html", admin=None)

        # 6. SUCCESS

        admin_type = admin_data["type_admin"]

        session['admin_type'] = admin_type #Para ma-store yung admin_type and ma-pass siya

        cursor.close()
        db.close()

        # REDIRECT BASED SA TYPE_ADMIN SA DB
        if admin_type == "High Admin":
            return redirect(url_for('admin.AdminDashboard'))

        elif admin_type == "Librarian":
            return redirect(url_for('admin.LibrarianDashboard'))

        else:
            flash("Invalid admin role!")
            return redirect(url_for('auth.AdminLogIn'))

    return render_template("AdminLogIn.html", admin=None)

@auth.route('/UserDashboard', methods=['POST'])
def UserDashboard():
    user_id = request.form.get('user_id')

    # You can fetch again OR use session later
    return render_template("UserDashboard.html")

def get_account_type(user_id):
    user_id = user_id.strip()

    # Professor: 4 digits + dash + 6 digits (total 11, dash at index 4)
    if len(user_id) == 11 and user_id[4] == "-" and re.fullmatch(r"\d{4}-\d{6}", user_id):
        return "professor"

    # Student: 10 digits only
    if len(user_id) == 10 and user_id.isdigit():
        return "student"

    return None