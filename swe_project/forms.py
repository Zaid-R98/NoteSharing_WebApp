
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError,SelectField,IntegerField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,InputRequired
from swe_project import db
from swe_project.models import *
from flask import flash
from swe_project.validators import *

class UserRegistrationForm(FlaskForm):
    #Things to add- email,pass,university_id,firstname,lastname
    first_name= StringField('First Name',validators=[DataRequired(),Length(max=20),Namecheck])
    last_name= StringField('Last Name',validators=[DataRequired(),Length(max=20),Namecheck])
    email=StringField('Email ', validators=[Email(),DataRequired(),Length(max=40),Emailcheck])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=3,max=40)])
    confirm_password=PasswordField('Confirm Passoword', validators=[DataRequired(),EqualTo('password')])
    university_chosen=SelectField(coerce=int)
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    choices=SelectField(coerce=int)
    submit = SubmitField('Search For Tables')


class addStudentCourseForm(FlaskForm): #Register Student To Course to Student Course Table
    student_id = IntegerField('Student ID',validators=[DataRequired(),checkstudent_id])
    course_id = IntegerField('Course ID',validators=[DataRequired(),checkcourse_id])
    submit=SubmitField('Register Student')


class AddCollegeForm(FlaskForm):
    name= StringField('Enter the Name of the New College..',validators=[DataRequired(),unicountry_check,checkUniname])
    submit=SubmitField('Add College')

class AddDepartmentForm(FlaskForm):
    name= StringField('Enter the Name of the New Department..',validators=[DataRequired(),checkUniname])
    college_id=IntegerField('Enter the College ID',validators=[DataRequired(),checkCollege_id])
    submit=SubmitField('Add Department')

class AddCourseForm(FlaskForm):
    name= StringField('Enter the Name of the Course..',validators=[DataRequired()])
    faculty_id=IntegerField('Enter the Faculty ID',validators=[DataRequired(),checkfaculty_id])
    department_id=IntegerField('Enter the Department ID',validators=[DataRequired(),checkdepartment_id])
    submit=SubmitField('Add Course')

class UploadNotesForm(FlaskForm):
    course_id=IntegerField('Enter the course ID',validators=[DataRequired(),checkNote_ID_Stu])
    submit=SubmitField('Add Note') #check this one...

class RateNoteForm(FlaskForm):
    NoteID=IntegerField('Enter the ID of the Note', validators=[DataRequired(),checknote_id])
    Rating=IntegerField('Enter your rating from 1 - 5', validators=[DataRequired(),checkRating])
    submit=SubmitField('Rate Note')

class FeedBackForm(FlaskForm):
    feedback=TextAreaField('Enter feedback', validators=[DataRequired(),checkfeedback_length])
    note_id=IntegerField('Enter the ID of the note', validators=[DataRequired(),checkNotes_ID_Fac])
    submit=SubmitField('Give Feedback')

class AddUniForm(FlaskForm):
    name=StringField('Enter University Name', validators=[DataRequired(),unicountry_check])
    country=StringField('Enter University Country', validators=[DataRequired(),unicountry_check])
    submit=SubmitField('Add uni')


class AddUniAdminForm(FlaskForm):
    email=StringField('Email ', validators=[Email(),DataRequired(),Length(max=40),Emailcheck,duplicate_useremail_check])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=3,max=40)])
    confirm_password=PasswordField('Confirm Passoword', validators=[DataRequired(),EqualTo('password')])
    university_chosen=IntegerField('Enter University ID', validators=[DataRequired(),uni_id_check,duplicate_id_check])
    submit = SubmitField('Add Uni Admin')
