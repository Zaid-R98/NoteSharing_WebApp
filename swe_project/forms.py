from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from swe_project import db



def Namecheck(FlaskForm,field): 
    if field.data.isdigit():
        raise ValidationError('First name and Last name cannot contain any Numbers.')
    
def Emailcheck(FlaskForm,field):
    if(field.data.split('@')[1].split('.')[-1]=='edu'):
        return True
    else:
        raise ValidationError("The email does not end with .edu")


class UserRegistrationForm(FlaskForm):
    #Things to add- email,pass,university_id,firstname,lastname
    first_name= StringField('First Name',validators=[DataRequired(),Length(max=20),Namecheck])
    last_name= StringField('Last Name',validators=[DataRequired(),Length(max=20),Namecheck])
    email=StringField('Email ', validators=[Email(),DataRequired(),Length(max=40),Emailcheck])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Passoword', validators=[DataRequired(),EqualTo('password')])
    university_chosen=SelectField('university_chosen',choices=[('POP','POOP'),('PP','PEE')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    
    
    
    
    

