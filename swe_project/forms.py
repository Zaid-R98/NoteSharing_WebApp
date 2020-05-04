
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError,SelectField,IntegerField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,InputRequired
from swe_project import db
from swe_project.models import *
from flask import flash


def Namecheck(FlaskForm,field): 
    if field.data.isdigit():
        raise ValidationError('First name and Last name cannot contain any Numbers.')
    
def Emailcheck(FlaskForm,field):
    if(field.data.split('@')[1].split('.')[-1]=='edu'):
        return True
    else:
        raise ValidationError("The email does not end with .edu")

def EmailRepeatCheck(FlaskForm,field):
    user=User.query.filter_by(email=field.data)
    if user:
        raise ValidationError('The User email already exists in the system...')


class UserRegistrationForm(FlaskForm):
    #Things to add- email,pass,university_id,firstname,lastname
    first_name= StringField('First Name',validators=[DataRequired(),Length(max=20),Namecheck])
    last_name= StringField('Last Name',validators=[DataRequired(),Length(max=20),Namecheck])
    email=StringField('Email ', validators=[Email(),DataRequired(),Length(max=40),Emailcheck])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=3,max=40)])
    confirm_password=PasswordField('Confirm Passoword', validators=[DataRequired(),EqualTo('password')])
    university_chosen=SelectField(coerce=int)
    submit = SubmitField('Sign Up')


    # form.university_choices=[(University.id,University.name) for Uni in University.query.all()]

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')





class SearchForm(FlaskForm):
    choices=SelectField(coerce=int)
    submit = SubmitField('Search For Tables')


class addStudentCourseForm(FlaskForm): #Register Student To Course to Student Course Table
    student_id = IntegerField('Student ID')
    course_id = IntegerField('Course ID')
    submit=SubmitField('Register Student')


class AddCollegeForm(FlaskForm):
    name= StringField('Enter the Name of the New College..',validators=[DataRequired(),unicountry_check,checkUniname])
    submit=SubmitField('Add College')

def checkUniname(FlaskForm,field):
    if len(field.data)>40:
        raise ValidationError('The length cannot be more than 40...')

class AddDepartmentForm(FlaskForm):
    name= StringField('Enter the Name of the New Department..',validators=[DataRequired()])
    college_id=IntegerField('Enter the College ID',validators=[DataRequired()])
    submit=SubmitField('Add Department')

class AddCourseForm(FlaskForm):
    name= StringField('Enter the Name of the Course..',validators=[DataRequired()])
    faculty_id=IntegerField('Enter the Faculty ID',validators=[DataRequired()])
    department_id=IntegerField('Enter the Department ID',validators=[DataRequired()])
    submit=SubmitField('Add Course')

class UploadNotesForm(FlaskForm):
    course_id=IntegerField('Enter the course ID')
    submit=SubmitField('Add Note') #check this one...

class RateNoteForm(FlaskForm):
    NoteID=IntegerField('Enter the ID of the Note', validators=[DataRequired()])
    Rating=IntegerField('Enter your rating from 1 - 5', validators=[DataRequired()])
    submit=SubmitField('Rate Note')

class FeedBackForm(FlaskForm):
    feedback=TextAreaField('Enter feedback', validators=[DataRequired()])
    note_id=IntegerField('Enter the ID of the note', validators=[DataRequired()])
    submit=SubmitField('Give Feedback')


#Add Uni Validator
def unicountry_check(FlaskForm,field):
    if field.data.isdigit():
        raise ValidationError("The field cannot be a number")

class AddUniForm(FlaskForm):
    name=StringField('Enter University Name', validators=[DataRequired(),unicountry_check])
    country=StringField('Enter University Country', validators=[DataRequired(),unicountry_check])
    submit=SubmitField('Add uni')


#add Uni admin validators
def uni_id_check(FlaskForm,field):
    lsttocheck=University.query.get(field.data)
    if lsttocheck:
        pass
    else:
        flash('Check fields for error..!', 'danger')
        raise ValidationError('This university ID not exist')

def duplicate_id_check(FlaskForm,field):
    for un in User.query.all():
        if un.uni_admin_check==True and un.university_id==field.data:
            raise ValidationError("This university has already been assigned!")

def duplicate_useremail_check(FlaskForm,field):
    for un in User.query.all():
        if un.email==field.data:
            raise ValidationError("The ID already belongs to a user..!")

class AddUniAdminForm(FlaskForm):
    email=StringField('Email ', validators=[Email(),DataRequired(),Length(max=40),Emailcheck,duplicate_useremail_check])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=3,max=40)])
    confirm_password=PasswordField('Confirm Passoword', validators=[DataRequired(),EqualTo('password')])
    university_chosen=IntegerField('Enter University ID', validators=[DataRequired(),uni_id_check,duplicate_id_check])
    submit = SubmitField('Add Uni Admin')
