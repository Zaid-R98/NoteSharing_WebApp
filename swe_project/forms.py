from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo




def Namecheck(FlaskForm,field): 
    if field.data.isdigit():
        raise ValidationError('First name and Last name cannot contain any Numbers.')
    

class UserRegistrationForm(FlaskForm):
    #Things to add- email,pass,university_id,firstname,lastname
    first_name= StringField('First Name',validators=[DataRequired(),Length(max=20),Namecheck])
    last_name= StringField('Last Name',validators=[DataRequired(),Length(max=20),Namecheck])
    email=StringField('Email ', validators=[Email(),DataRequired(),Length(max=40)])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Passoword', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    
    
    
    
    

