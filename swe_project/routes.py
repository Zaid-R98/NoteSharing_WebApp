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

@app.route("/register",methods=['GET','POST'])
def register():
    form=UserRegistrationForm()
    
    if form.validate_on_submit():
        flash(f'Account has been created for {form.first_name.data}', 'success')
    else:
        print("Form has not been validated!") #data being inputted fine now.
    form.university_chosen.choices=[('OPTION 1 UNI','AUS'), ('OPTION 2 UNI','AUD'),('OPTION3', 'Radom University')]
    #When connected to Database Have to do this->
    # form.university_choices=[(University.id,University.name) for Uni in University.query.all()]
    #if doubt- watch video here-  https://www.youtube.com/watch?v=I2dJuNwlIH0
    #sample on how to print here...
    print(form.first_name.data)
    #Passing the render template command.
    return render_template('register.html',form=form)
