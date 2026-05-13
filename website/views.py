from flask import Blueprint, render_template

views = Blueprint('views',__name__)

# students/profs to log in
@views.route('/')
def CapacityTrackingUserLogin():
    return render_template("CapacityTrackingUserLogin.html")

#student/prof confirms seat
@views.route('/CapacityTrackingConfirmSeat')
def CapacityTrackingConfirmSeat():
    return render_template("CapacityTrackingConfirmSeat.html")



