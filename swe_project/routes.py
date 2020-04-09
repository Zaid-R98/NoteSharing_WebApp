from flask import render_template, url_for, flash, redirect
from swe_project import app
from swe_project.forms import UserRegistrationForm,LoginForm
#from testproject_2.models import User,Post
#from testproject_2.forms import RegistrationForm,LoginForm

@app.route("/", methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash(f'Account has been logged in for {form.first_name.data} ', 'success')
    return render_template('login.html',form=form)

@app.route("/register",methods=['GET','POST'])
def register():
    form=UserRegistrationForm()
    
    if form.validate_on_submit():
        flash(f'Account has been created for {form.first_name.data}', 'success')
    else:
        print("Form has not been validated!") #data being inputted fine now.
    print(form.first_name.data)
    print(form.last_name.data)
    print(form.password.data)
    print(form.confirm_password.data)
    print(form.submit.data)
    print(form.email.data)
    return render_template('register.html',form=form)
