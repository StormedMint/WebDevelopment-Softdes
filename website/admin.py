from flask import Blueprint, render_template

admin = Blueprint('admin',__name__)


@admin.route('/AdminDashboard')
def AdminDashboard():
    return render_template("AdminDashboard.html")

@admin.route('/AdminAccManagement')
def AdminAccManagement(): # <-- Fixed duplicate function name bug here
    return render_template("AdminAccManagement.html")

@admin.route('/UserAccManagement')
def UserAccManagement():
    return render_template("UserAccManagement.html")

@admin.route('/LogTableManagement')
def LogTableManagement():
    return render_template("LogTableManagement.html")

@admin.route('/DeletedUserManagement')
def DeletedUserManagement():
    return render_template("DeletedUserManagement.html")

@admin.route('/CapacityTrackingAdminSide')
def CapacityTrackingAdminSide():
    return render_template("CapacityTrackingAdminSide.html") # Added missing .html extension

@admin.route('/ReservedRoomsTracker')
def ReservedRoomsTracker():
    return render_template("ReservedRoomsTracker.html") 

@admin.route('/LostAndFound')
def LostAndFound():
    return render_template("LostAndFound.html") 