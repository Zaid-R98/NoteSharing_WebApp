from flask import render_template, url_for, flash, redirect
from swe_project import app
from swe_project.forms import UserRegistrationForm,LoginForm
from swe_project.models import *

@app.route("/", methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash(f'Account has been logged in for {form.first_name.data} ', 'success')
    return render_template('login.html',form=form)



@app.route("/register-student",methods=['GET','POST'])
def registerStudent():
    form=UserRegistrationForm()
    if form.validate_on_submit():
        flash(f'Account has been created for {form.first_name.data}', 'success')
    else:
        print("Form has not been validated!") #data being inputted fine now.
        print(form.errors)
    return render_template('register_student.html',form=form)


@app.route("/register-faculty",methods=['GET','POST'])
def registerFaculty():
    form=UserRegistrationForm()
    if form.validate_on_submit():
        flash(f'Account has been created for {form.first_name.data}', 'success')
    else:
        print("Form has not been validated!") #data being inputted fine now.
        print(form.errors)
    return render_template('register_faculty.html',form=form)