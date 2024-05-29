from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Staff
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricNumber = request.form.get('matricNumber')
        password = request.form.get('password')

        user = User.query.filter_by(matricNumber=matricNumber).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
           flash('User does not exist.', category='error')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        surname = request.form.get('surname')
        otherNames = request.form.get('otherNames')
        matricNumber = request.form.get('matricNumber')
        level = request.form.get('level')
        college = request.form.get('college')
        department = request.form.get('department')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        user = User.query.filter_by(matricNumber=matricNumber).first()
        if user:
            flash('Matric number is already registered.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(surname) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif len(otherNames) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif password != confirmPassword:
           flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
           flash('Password must be atleast 7 character', category='error')
        else:
            # add user to database
            new_user = User(surname=surname, otherNames=otherNames, matricNumber=matricNumber, level=level,
                            college=college, department=department, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            #login_user(user, remember=True)

            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template('register.html')

@auth.route('/staff-login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        staff = Staff.query.filter_by(email=email).first()
        if staff:
            if check_password_hash(staff.password, password):
                flash('Logged in successfully!', category='success')
                login_user(staff, remember=True)
                return redirect(url_for('views.staff_dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')
    return render_template('staff_login.html')

@auth.route('/staff-register', methods=['GET', 'POST'])
def staff_register():
    if request.method == 'POST':
        fullName = request.form.get('fullName')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        staff = Staff.query.filter_by(email=email).first()
        if staff:
            flash('Email is already registered.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(fullName) < 5:
            flash('Name must be greater than 5 characters.', category='error')
        elif password != confirmPassword:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be atleast 7 character', category='error')
        else:
            # add user to database
            new_staff = Staff(fullName=fullName, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_staff)
            db.session.commit()
            # login_user(user, remember=True)

            flash('Account created', category='success')
            return redirect(url_for('views.staff_dashboard'))
    return render_template('staff_register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
