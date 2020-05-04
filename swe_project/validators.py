
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError,SelectField,IntegerField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,InputRequired
from swe_project import db
from flask_login import current_user
from swe_project.models import *
from flask import flash
#add Uni admin validators
def uni_id_check(FlaskForm,field):
    lsttocheck=University.query.get(field.data)
    if lsttocheck:
        pass
    else:
        flash('Check fields for error..!', 'danger')
        raise ValidationError('This university ID not exist')

def duplicate_id_check(FlaskForm,field):
    print('The field data to check for duplicate data is '+ str(field.data))
    for un in User.query.all():
        if un.uni_admin_check==True and un.university_id==field.data:
            raise ValidationError("This university has already been assigned!")

def duplicate_useremail_check(FlaskForm,field):
    for un in User.query.all():
        if un.email==field.data:
            raise ValidationError("The ID already belongs to a user..!")

#Add Uni Validator
def unicountry_check(FlaskForm,field):
    if field.data.isdigit():
        raise ValidationError("The field cannot be a number")


def checkUniname(FlaskForm,field):
    if len(field.data)>40:
        raise ValidationError('The length cannot be more than 40...')

def Namecheck(FlaskForm,field): 
    if field.data.isdigit():
        raise ValidationError('First name and Last name cannot contain any Numbers.')
    
def Emailcheck(FlaskForm,field):
   if field.data[(len(field.data)-3):(len(field.data))]!='edu':
       raise ValidationError("This email does not end with .edu")

def EmailRepeatCheck(FlaskForm,field):
    user=User.query.filter_by(email=field.data)
    if user:
        raise ValidationError('The User email already exists in the system...')

#Add Department
def checkCollege_id(FlaskForm,field):
    checklist=[]
    for c in College.query.all():
        checklist.append(c.id)
    
    if field.data not in checklist:
        raise ValidationError('The ID does not exist in the system...')


#Add Course
def checkdepartment_id(FlaskForm,field):
    checklist=[]
    for c in Department.query.all():
        checklist.append(c.id)
    
    if field.data not in checklist:
        raise ValidationError('The ID does not exist in the system...')


def checkfaculty_id(FlaskForm,field):
    checklist=[]
    for c in Faculty.query.all():
        checklist.append(c.id)
    
    if field.data not in checklist:
        raise ValidationError('The ID does not exist in the system...')

#Register Student to courses

def checkstudent_id(FlaskForm,field):
    checklist=[]
    for c in Student.query.all():
        checklist.append(c.id)
    
    if field.data not in checklist:
        raise ValidationError('The ID does not exist in the system...')


def checkcourse_id(FlaskForm,field):
    checklist=[]
    for c in Courses.query.all():
        checklist.append(c.id)
    
    if field.data not in checklist:
        raise ValidationError('The ID does not exist in the system...')

#Rate Notes
def checknote_id(FlaskForm,field):
    checklist=[]
    for c in Notes.query.all():
        checklist.append(c.id)
    
    if field.data not in checklist:
        raise ValidationError('The ID does not exist in the system...')

def checkRating(FlaskForm,field):
        if field.data>5 or field.data<0:
                raise ValidationError('Wrong rating entered. Be between 0 and 5')

#Feedback
def checkfeedback_length(FlaskForm,field):
        if len(field.data)>400:
                raise ValidationError('The length cannot be more than 400')

def checkNotes_ID_Fac(FlaskForm,field):
       NoteList=Notes.GetFacultyNotes(current_user.id)
       check=False
       for n in NoteList:
               if n.id==field.data:
                       check=True
       if check==False:
                raise ValidationError('You do not teach this course..')

#Upload Notes Validators-

def checkNote_ID_Stu(FlaskForm,field):
        print("It reaches here")
        CourseList=Student_Course.studentcourselist(current_user.id)
        check=False
        for n in CourseList:
               print(str(n.id))
               if n.id==field.data:
                       check=True
        if check==False:
                raise ValidationError('You do not take this course..')