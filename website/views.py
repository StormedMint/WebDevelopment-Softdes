from flask import Blueprint, flash, render_template ,redirect, url_for, request, session
from .db import get_db_connection

views = Blueprint('views',__name__)

# students/profs to log in
#Get information from db current and capacity to show current and max capacity (seatVacancy)
@views.route('/')
def CapacityTrackingUserLogin():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT area, current, capacity, floor
        FROM vacancy_table
    """)

    rooms = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("CapacityTrackingUserLogin.html", rooms=rooms)

#Get information from db current and capacity to show current and max capacity (seatSelection)
@views.route('/CapacityTrackingConfirmSeat')
def CapacityTrackingConfirmSeat():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT area, current, capacity, floor
        FROM vacancy_table
    """)

    rooms = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("CapacityTrackingConfirmSeat.html", rooms=rooms)

#Get information from db current and capacity to show current and max capacity (Ril capacityTracking)
@views.route('/CapacityTrackingAdminSide')
def CapacityTrackingAdminSide():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT area, current, capacity, floor FROM vacancy_table")
    rooms = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "CapacityTrackingConfirmSeat.html",
        rooms=rooms,
        account_type=session.get("account_type")  # IMPORTANT
    )


@views.route("/confirm-selected-room", methods=["POST"])
def confirm_selected_room():
    selected_area = request.form.get("selected_area")
    account_type = session.get("account_type")

    if not selected_area:
        return redirect(url_for("views.CapacityTrackingUserLogin"))

    if not account_type:
        return "Not logged in", 401

    allowed_student = [
        "Reading Area",
        "Internet Section",
        "Lounge Area",
        "Graduate Reading Area",
        "Undergraduate Reading Area"
    ]

    allowed_professor = allowed_student + ["Faculty Room"]

    allowed_map = {
        "student": allowed_student,
        "professor": allowed_professor
    }

    if selected_area not in allowed_map.get(account_type, []):
        return redirect(url_for("views.CapacityTrackingConfirmSeat"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT current, capacity
        FROM vacancy_table
        WHERE area = %s
    """, (selected_area,))

    room = cursor.fetchone()

    if not room:
        return "Room not found", 404

    if room["current"] >= room["capacity"]:
        return "Room full", 400

    cursor.execute("""
        UPDATE vacancy_table
        SET current = current + 1
        WHERE area = %s
    """, (selected_area,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("views.CapacityTrackingUserLogin"))