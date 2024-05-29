from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from .models import Exeat
from . import db
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template('index.html')

@views.route('/dashboard')
@login_required
def staff_dashboard():
    return render_template('staff_dashboard.html')

@views.route('/exeat-form', methods=['GET', 'POST'])
@login_required
def exeat_form():
    if request.method == 'POST':
        surname = request.form.get('surname')
        otherNames = request.form.get('otherNames')
        matricNumber = request.form.get('matricNumber')
        college = request.form.get('college')
        department = request.form.get('department')
        level = request.form.get('level')
        reason = request.form.get('reason')
        address = request.form.get('address')
        parentsNumber = request.form.get('parentsNumber')
        exeat_date = request.form.get('exeatDate')
        return_date = request.form.get('returnDate')
        datetime_obj = datetime.now()
        today_date = datetime_obj.date()
        today_time = datetime_obj.strftime('%H:%M:%S')
        status = 'Pending'
        new_exeat = Exeat(surname=surname, otherNames=otherNames, matricNumber=matricNumber, college=college,
                          department=department, level=level, reason=reason, address=address, parentsNumber=parentsNumber,
                          exeat_date=exeat_date, return_date=return_date, status=status, today_date=today_date,
                          today_time=today_time)
        db.session.add(new_exeat)
        db.session.commit()
    return render_template('exeat.html', user=current_user)

@views.route('/exeat-history', methods=['GET', 'POST'])
def history():
    history = Exeat.query.filter_by(matricNumber=current_user.matricNumber).all()
    return render_template('history.html', history=history)

@views.route('/notifications', methods=['GET', 'POST'])
def notifcations():
    return render_template('notifications.html')

@views.route('pending-requests')
def pending_requests():
    open_requests = Exeat.query.filter_by(status='Pending').all()
    return render_template('pending_requests.html', open_requests=open_requests)

@views.route('/view-requests/<id>', methods=['GET', 'POST'])
def view_requests(id):
    open_requests = Exeat.query.filter_by(id=id).first()
    if request.method == 'POST':
        update_status = request.form.get('status')
        print(update_status)
        open_requests.status = update_status

        db.session.commit()

    return render_template('view_requests.html', open_requests=open_requests)
