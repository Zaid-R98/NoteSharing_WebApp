from flask import render_template, url_for, flash, redirect
from swe_project import app
#from testproject_2.models import User,Post
#from testproject_2.forms import RegistrationForm,LoginForm

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

