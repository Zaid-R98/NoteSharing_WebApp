from swe_project import db, login_manager
from datetime import datetime
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    #username=db.Column(db.String(25),nullable=False,unique=True)
    password=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(40),nullable=False,unique=True)
    university_id=db.Column(db.Integer,db.ForeignKey('university.id'),nullable=False)
    st_fa=db.Column(db.Boolean,nullable=False) #True if Faculty
    uni_admin_check=db.Column(db.Boolean,nullable=False)#True if Uniadmin

class Uni_admin(db.Model):
    uni_ad_id=db.Column(db.Integer,primary_key=True)#admin id
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)

class Student(db.Model):
    student_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)
    #academic_level=db.Column(db.String(30),nullable=False)
    

class Faculty(db.Model):
    faculty_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)

class University(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40),nullable=False,unique=True)
    country=db.Column(db.String(40),nullable=False)

class College(db.Model):
    college_id=db.Column(db.Integer,primary_key=True)
    uni_id=db.Column(db.Integer,db.ForeignKey('university.id'),nullable=False)
    name=db.Column(db.String(40),nullable=False,unique=True)

class Department(db.Model):
    department_id=db.Column(db.Integer,primary_key=True)
    uni_id=db.Column(db.Integer,db.ForeignKey('university.id'),nullable=False)
    name=db.Column(db.String(40),nullable=False,unique=True)

class Courses(db.Model):
    course_id=db.Column(db.String(20),primary_key=True)
    uni_id=db.Column(db.Integer,db.ForeignKey('university.id'),nullable=False)
    name=db.Column(db.String(40),nullable=False,unique=True)
    faculty_id=db.Column(db.Integer,db.ForeignKey('faculty.faculty_id'),nullable=False)
    
class Notes(db.Model):
    note_id=db.Column(db.Integer,primary_key=True)
    course_id=db.Column(db.Integer,db.ForeignKey('courses.course_id'),nullable=False)
    student_id=db.Column(db.Integer,db.ForeignKey('student.student_id'),nullable=False)
    Note=db.Column(db.LargeBinary,nullable=False)

class Rating(db.Model):
    rating_id=db.Column(db.Integer,primary_key=True)
    note_id=db.Column(db.Integer,db.ForeignKey('notes.note_id'),nullable=False)
    rating=db.Column(db.Integer,nullable=False)

class Student_Course(db.Model):
    student_course_id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('student.student_id'),nullable=False)
    course_id=db.Column(db.Integer,db.ForeignKey('courses.course_id'),nullable=False)