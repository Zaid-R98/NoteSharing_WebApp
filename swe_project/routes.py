from flask import render_template, url_for, flash, redirect
from swe_project import app
from swe_project.forms import UserRegistrationForm,LoginForm
from swe_project.models import *
from flask_login import login_user, current_user


#from testproject_2.forms import RegistrationForm,LoginForm

@app.route("/", methods=['GET', 'POST'])
def login():
    form=LoginForm()
    flash(f'TestFlash ', 'success')
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and (user.password == form.password.data):
            print(" SUCCESFULL")
            flash(f'Account has been logged in for {form.first_name.data} ', 'success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('register_student.html'))
        else:
            flash(f'Login has been unsuccessful. Email/password is wrong {form.first_name.data} ', 'success')
            print("NOT SUCCESFULL")
    return render_template('login.html',title ='Login', form=form)

@app.route("/register-student",methods=['GET','POST'])
def registerStudent():
    form=UserRegistrationForm()
    if University.query.first()==None:
        form.university_chosen.choices=[('0','No University in the System yet..')]
    else:
        form.university_chosen.choices=[(uni.id,uni.name) for uni in University.query.all()]
    if form.validate_on_submit():
        flash(f'Account has been created for {form.first_name.data}', 'success')
        addUserStudent(form)
    else:
        print("Form has not been validated!") #data being inputted fine now.
        print(form.errors)
    return render_template('register_student.html',form=form)


def addUserStudent(form):
    user=User(password=form.password.data,email=form.email.data,university_id=form.university_chosen.data,st_fa=False,uni_admin_check=False)
    db.session.add(user)
    db.session.commit()
    student=Student(user_id=user.id,firstname=form.first_name.data,lastname=form.last_name.data)
    db.session.add(student)
    db.session.commit()



@app.route("/register-faculty",methods=['GET','POST'])
def registerFaculty():
    form=UserRegistrationForm()
    if University.query.first()==None:
        form.university_chosen.choices=[('0','No University in the System yet..')]
    else:
        form.university_chosen.choices=[(uni.id,uni.name) for uni in University.query.all()]
    if form.validate_on_submit():
        flash(f'Account has been created for {form.first_name.data}', 'success')
        addUserFaculty(form)
    else:
        print("Form has not been validated!") #data being inputted fine now.
        print(form.errors)
    return render_template('register_faculty.html',form=form)

def addUserFaculty(form):
    user=User(password=form.password.data,email=form.email.data,university_id=form.university_chosen.data,st_fa=False,uni_admin_check=False)
    db.session.add(user)
    db.session.commit()
    faculty=Faculty(user_id=user.id,firstname=form.first_name.data,lastname=form.last_name.data)
    db.session.add(faculty)
    db.session.commit()

@app.route("/profile", methods=['GET','POST'])
def profile():
    return render_template('profile.html')

@app.route("/registeredcourses", methods=['GET','POST'])
def registered():
    return render_template('registeredCourses.html')