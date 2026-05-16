from flask import Blueprint, render_template
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