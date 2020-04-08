from flask import render_template, url_for, flash, redirect
from swe_project import app
from swe_project.forms import UserRegistrationForm,LoginForm
#from testproject_2.models import User,Post
#from testproject_2.forms import RegistrationForm,LoginForm

@app.route("/", methods=['GET', 'POST'])
def login():
    form=LoginForm()
    return render_template('login.html',form=form)

@app.route("/register",methods=['GET','POST'])
def register():
    form=UserRegistrationForm()
    return render_template('register.html',form=form)
