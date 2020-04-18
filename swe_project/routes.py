from flask import render_template, url_for, flash, redirect
from swe_project import app,db
from swe_project.forms import *
from swe_project.models import *
from flask_login import login_user, current_user,login_required,logout_user

@app.route("/", methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and (user.password == form.password.data):
            flash(f'Account has been logged in for {form.email.data} ', 'success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))
        else:
            print(form.errors)
            flash(f'Login has been unsuccessful. Email/password is wrong {form.email.data} ', 'danger')
            return redirect(url_for('login'))
    else:
        print(form.errors)
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
    user=User(password=form.password.data,email=form.email.data,university_id=form.university_chosen.data,st_fa=True,uni_admin_check=False)
    db.session.add(user)
    db.session.commit()
    faculty=Faculty(user_id=user.id,firstname=form.first_name.data,lastname=form.last_name.data)
    db.session.add(faculty)
    db.session.commit()
    print("hello")


@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    Student_or_Faculty=current_user.st_fa
    print(Student_or_Faculty)
    if Student_or_Faculty==True:
        name=Faculty.query.filter_by(user_id=current_user.id).first().firstname
    if Student_or_Faculty==False:
        name=Student.query.filter_by(user_id=current_user.id).first().firstname
    return render_template('profile.html',University=University,User_FirstName=name)

@app.route('/logout')
def logout():
    logout_user()
    flash("Account has been logged out succesfully...", 'success')
    return redirect(url_for('login'))


@app.route("/registeredcourses", methods=['GET','POST'])
def registeredcourses():
    return render_template('registeredCourses.html')


##Feraas (Ability to view students, faculty, courses, and course student list) ##
@app.route('/uni-admin', methods=['GET', 'POST'])
def index():
    search = SearchForm()
    results = []
    search_string = search.data['search']
    return render_template('blank.html',form=search)


##The route stands for register student to course.
@app.route('/rstc', methods=['GET', 'POST'])
def register_student_to_course():
    form = RegistrationForm()

    if  form.validate():
        flash('User Sucessfully registered to Course!')
        return redirect('/uni-admin')

    return render_template('rstc.html', form=form)
