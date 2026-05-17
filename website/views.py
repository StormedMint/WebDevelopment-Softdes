from flask import Blueprint, render_template ,redirect, url_for, request
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

    cursor.execute("""
        SELECT area, current, capacity, floor
        FROM vacancy_table
    """)

    rooms = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("CapacityTrackingAdminSide.html", rooms=rooms)

#Used for Confirming Seating Area and updating the db value
@views.route("/confirm-selected-room", methods=["POST"])
def confirm_selected_room():
    selected_area = request.form.get("selected_area")

    allowed_rooms = [
        "Reading Area",
        "Internet Section",
        "Lounge Area",
        "Faculty Room",
        "Graduate Reading Area",
        "Undergraduate Reading Area"
    ]

    if selected_area not in allowed_rooms:
        return redirect(url_for("views.CapacityTrackingUserLogin"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT current, capacity FROM vacancy_table WHERE area = %s",
        (selected_area,)
    )

    room = cursor.fetchone()

    if room:
        current = room["current"]
        capacity = room["capacity"]

        if current < capacity:
            cursor.execute(
                "UPDATE vacancy_table SET current = current + 1 WHERE area = %s",
                (selected_area,)
            )
            conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("views.CapacityTrackingUserLogin"))