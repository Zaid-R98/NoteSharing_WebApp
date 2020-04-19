
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError,SelectField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from swe_project import db
from swe_project.models import *



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
    password=PasswordField('Password',validators=[DataRequired()])
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


class RegistrationForm(FlaskForm): #Register Student To Course to Student Course Table
    StudentID = StringField('Student ID: ',validators=[DataRequired()])
    CourseID = StringField('Course ID: ',validators=[DataRequired()])
    submit=SubmitField('Register Student')


class AddCollegeForm(FlaskForm):
    name= StringField('Enter the Name of the New College..',validators=[DataRequired()])
    submit=SubmitField('Add College')


class AddDepartmentForm(FlaskForm):
    name= StringField('Enter the Name of the New Department..',validators=[DataRequired()])
    college_id=IntegerField('Enter the College ID',validators=[DataRequired()])
    submit=SubmitField('Add Department')

class AddCourseForm(FlaskForm):
    name= StringField('Enter the Name of the Course..',validators=[DataRequired()])
    faculty_id=IntegerField('Enter the Faculty ID',validators=[DataRequired()])
    department_id=IntegerField('Enter the Department ID',validators=[DataRequired()])
    submit=SubmitField('Add Department')

