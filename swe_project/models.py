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

    def GetUser(id):
        return User.query.filter_by(id=id).first()
    
    def GetUserOfUni(uni_admin_uni_id):
        return User.query.filter_by(university_id=uni_admin_uni_id)

class Uni_admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)#admin id
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)
    #academic_level=db.Column(db.String(30),nullable=False)           

    def getStudent(uni_id):#uni_id is admin id
        studentlist=[]
        for uzer in User.GetUserOfUni(uni_id):
            if Student.query.filter_by(user_id=uzer.id).first():    
                studentlist.append(Student.query.filter_by(user_id=uzer.id).first())
        return studentlist



class Faculty(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)

    def getFaculty(uni_id):#uni_id is admin id
        FacultyList=[]
        for uzer in User.GetUserOfUni(uni_id):
            if Faculty.query.filter_by(user_id=uzer.id).first():    
                FacultyList.append(Faculty.query.filter_by(user_id=uzer.id).first())
        return FacultyList


class University(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40),nullable=False,unique=True)
    country=db.Column(db.String(40),nullable=False)

class College(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uni_id=db.Column(db.Integer,db.ForeignKey('university.id'),nullable=False)
    name=db.Column(db.String(40),nullable=False,unique=True)

class Department(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uni_id=db.Column(db.Integer,db.ForeignKey('university.id'),nullable=False)
    name=db.Column(db.String(40),nullable=False,unique=True)

class Courses(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uni_id=db.Column(db.Integer,db.ForeignKey('university.id'),nullable=False)
    name=db.Column(db.String(40),nullable=False,unique=True)
    faculty_id=db.Column(db.Integer,db.ForeignKey('faculty.id'),nullable=False)

    def getCourse(uni_admin_id): #will also work for faculty-course table
        return Courses.query.filter_by(uni_id=uni_admin_id)
    
class Notes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    course_id=db.Column(db.Integer,db.ForeignKey('courses.id'),nullable=False)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)
    Note=db.Column(db.LargeBinary,nullable=False)

class Rating(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    note_id=db.Column(db.Integer,db.ForeignKey('notes.id'),nullable=False)
    rating=db.Column(db.Integer,nullable=False)

class Student_Course(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)
    course_id=db.Column(db.Integer,db.ForeignKey('courses.id'),nullable=False)

    def stucoget(uni_admin_id):
        student_course_list=[]
        students=Student.getStudent(uni_admin_id)
        for z in students:
            for stcr in Student_Course.query.all():
                if stcr.student_id==z.id:
                    student_course_list.append(stcr)

        return student_course_list

            
