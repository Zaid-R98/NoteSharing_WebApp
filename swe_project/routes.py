from flask import render_template, url_for, flash, redirect,request,send_file
from swe_project import app,db
from swe_project.forms import *
from swe_project.models import *
from flask_login import login_user, current_user,login_required,logout_user
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from io import BytesIO


csrf = CSRFProtect(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route("/", methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and (user.password == form.password.data):
            flash(f'Account has been logged in for {form.email.data} ', 'success')
            login_user(user)
            if user.uni_admin_check==True:#Uni admin login is seperate
                return redirect(url_for('index'))
            if user.st_fa==True:
                return redirect(url_for('facprofile'))
            return redirect(url_for('profile')) #Normal User Login
        else:
            print(form.errors)
            flash(f'Login has been unsuccessful. Email/password is wrong {form.email.data} ', 'danger')
            return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('login.html',title ='Login', form=form)

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

@app.route('/logout')
def logout():
    logout_user()
    flash("Account has been logged out succesfully...", 'success')
    return redirect(url_for('login'))

#check this route below too...
@app.route("/registeredcourses", methods=['GET','POST'])
def registeredcourses():
    return render_template('registeredCourses.html')



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





##Feraas (Ability to view students, faculty, courses, and course student list) ##
@app.route('/uni-admin', methods=['GET', 'POST'])
@login_required
def index():
    form = SearchForm()
    form.choices.choices=[(0,'Student List'), (1,'Faculty List'), (2,'Courses List'), (3, 'Student- Course List'), (4,' Faculty Course List'),(5,'Department List'), (6,'College List')]
    if form.validate_on_submit():
        print(form.choices.data)
        print("Form has been Validated!")
    else:
        print(form.errors)
        print("Form Has Not Been Validated")
    return render_template('blank.html',form=form,StudentList=Student.getStudent(current_user.university_id),FacultyList=Faculty.getFaculty(current_user.university_id),CourseList=Courses.getCourse(current_user.university_id),StudentCourseList=Student_Course.getStudentCourse_ofUni(current_user.university_id),CollegeList=College.getCollege(current_user.university_id),DepartmentList=Department.getDepartment(current_user.university_id))


##The route stands for register student to course.
@app.route('/rstc', methods=['GET', 'POST'])
@login_required
def addStudentCourseAdmin():
    form = addStudentCourseForm()

    if  form.validate():
        flash('Student Sucessfully registered to Course!',category='success')
        addStudentCourse(form.student_id.data,form.course_id.data)
    else:
        flash('The student was not registered to the course. Invalid data entered!','danger')
        print(form.errors)

    return render_template('addStudentCourse.html', form=form)



def addStudentCourse(psid,pcid):
    sc_cr=Student_Course(student_id=psid , course_id=pcid)
    db.session.add(sc_cr)
    db.session.commit()


#Adding the College by Uni Admin
@app.route('/add_college',methods=['GET','POST'])
@login_required
def addCollegeAdmin():
    form=AddCollegeForm()
    if form.validate_on_submit():
        flash('College has been added succesfully ', category='success')
        AddCollege(current_user.university_id,form.name.data)
    
    else:
        print(form.errors)
        #flash('College has not been added. Please check the data entered!', category='danger')

    return render_template('addCollege.html',form=form)


def AddCollege(pid,pname):
    c1=College(uni_id=pid,name=pname)
    db.session.add(c1)
    db.session.commit()



#Adding the Department by Uni Admin
@app.route('/add_department',methods=['GET','POST'])
@login_required
def addDepartmentAdmin():
    form=AddDepartmentForm()
    if form.validate_on_submit():
        flash('Department has been added succesfully ', category='success')
        addDepartment(current_user.university_id,form.name.data,form.college_id.data)
    
    else:
        print(form.errors)
        #flash('Department has not been added. Please check the data entered!', category='danger')

    return render_template('addDepartment.html',form=form)


def addDepartment(pid,pname,pcollege_id):
    c1=Department(uni_id=pid,name=pname,college_id=pcollege_id)
    db.session.add(c1)
    db.session.commit()  


@app.route('/add-course', methods=['GET','POST'])
@login_required
def addCourseAdmin():
    form=AddCourseForm()
    if form.validate_on_submit():
        flash('Course has been added succesfully ', category='success')
        addCourse(current_user.university_id,form.name.data,form.faculty_id.data,form.department_id.data)
    else:
        flash('The form had errors. Please check data Entered..','danger')
        print(form.errors)
    return render_template('addCourse.html',form=form)


def addCourse(pid,pname,pfacultyid,pdepartmentid):
    c1=Courses(uni_id=pid,name=pname,faculty_id=pfacultyid,department_id=pdepartmentid)
    db.session.add(c1)
    db.session.commit()


@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    Student_or_Faculty=current_user.st_fa
    print(Student_or_Faculty)
    if Student_or_Faculty==True:
        name=Faculty.query.filter_by(user_id=current_user.id).first().firstname
    if Student_or_Faculty==False:
        name=Student.query.filter_by(user_id=current_user.id).first().firstname
    print("The current user id is "+str(current_user.id))
    return render_template('profile.html',University=University,User_FirstName=name,CourseList=Student_Course.studentcourselist(current_user.id))

@app.route('/upload', methods = ['GET','POST'])
@login_required
def upload():
    form=UploadNotesForm()
    if request.method == 'POST':
        file = request.files['inputFile'] 
        student=Student.getStudentFromUserID(current_user.id)
        print("STUDENT ID IS "+ str(student.id))
        print("The data from the form is "+ str(form.course_id.data))
        newFile = Notes(course_id = form.course_id.data, student_id =student.id, Note = file.read(),approve=False)
        db.session.add(newFile)
        db.session.commit()
        flash('The Note has been added to the database. Professor will approve..', category='success')
    return render_template('upload.html',form=form)


@app.route('/ratenote',methods=['GET','POST'])
@login_required
def rate():
    form=RateNoteForm()
    if form.validate_on_submit():
        flash('The Note was rated succesfully','success')
        RateNote(form.NoteID.data,form.Rating.data)
    else:
        flash('The rating was not succesful. Please check parameters.')
    return render_template('ratenote.html',form=form)

def RateNote(note_idd,ratingg): # Adds the rating to that perticular Note.
    new_rating=Rating(note_id=note_idd,rating=ratingg,student_id=current_user.id)
    db.session.add(new_rating)
    db.session.commit()




@app.route('/view-notes-student',methods=['GET','POST'])
@login_required
def ViewNote():
    print("Testing Notes Now-->")
    return render_template('viewnotes.html',NoteList=Student_Course.ReturnApproveNotesStudent(current_user.id),ratin=Rating)

@app.route('/download-notes/<int:noteid>',methods=['GET','POST'])
@login_required
def DownloadNote(noteid):
    print("The Note ID IS "+"    "+str(noteid))
    fileData=Notes.query.filter_by(id=noteid).first()
    return send_file(BytesIO(fileData.Note),attachment_filename='NoteSharingPlatformNote.pdf',as_attachment=True) 

@app.route('/view-feedback',methods=['GET','POST'])
@login_required
def viewfeedback():
    print("Student view feedback function now ...")
    return render_template('studentfeedback.html',FeedBackList=Feedback.fbl(current_user.id))



#---------------------------------------------xxxxxxxxxxxxx---------------------------------------------------------------------
#Faculty Routes - Profile, approve and Feedback

@app.route('/profile-faculty', methods=['GET','POST'])
@login_required
def facprofile():
    return render_template('profile_faculty.html',NoteList=Notes.GetFacultyNotes(current_user.id))

@app.route('/give-feedback',methods=['GET','POST'])
@login_required
def giveFeedback():
    form=FeedBackForm()
    if form.validate_on_submit():
        applyfeedback(form.note_id.data,current_user.id,form.feedback.data)
    else:
        flash('The form was not validated...','warning')
    return render_template('feedback.html',form=form)

def applyfeedback(noteiz,fid,feedbak):
    feedback=Feedback(note_id=noteiz,faculty_id=fid,feedback=feedbak)
    db.session.add(feedback)
    db.session.commit()
    flash('Feedback was succesfully given...','success')

@app.route('/approve-note/<int:noteID>',methods=['GET','POST'])
@login_required
def approveNote(noteID):
    print("Note ID For Note to be approved is "+ str(noteID))
    note_to_approve=Notes.query.filter_by(id=noteID).first()
    if note_to_approve:
        note_to_approve.approve=True
        db.session.commit()
        flash('The Note has been succesfully appoved', 'success')
    else:
        flash('Error encountered!','danger')
    return redirect(url_for('facprofile'))
