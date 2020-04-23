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
        return User.query.filter_by(id=id).all()
    
    def GetUserOfUni(uni_admin_uni_id):
        return User.query.filter_by(university_id=uni_admin_uni_id).all()

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

    def getStudent(uni_id):#uni_id is admin uni id
        studentlist=[]
        for uzer in User.GetUserOfUni(uni_id):
            if Student.query.filter_by(user_id=uzer.id).first():    
                studentlist.append(Student.query.filter_by(user_id=uzer.id).first())
        return studentlist
    
    def getStudentUserID(userid):
        return Student.query.filter_by(user_id=userid).first()



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

    def getCollege(uni_admin_id):
        return College.query.filter_by(uni_id=uni_admin_id).all()

class Department(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uni_id=db.Column(db.Integer,db.ForeignKey('university.id'),nullable=False)
    name=db.Column(db.String(40),nullable=False,unique=True)
    college_id=db.Column(db.Integer,db.ForeignKey('college.id'),nullable=False)

    def getDepartment(uni_admin_id):
        return Department.query.filter_by(uni_id=uni_admin_id).all()

class Courses(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uni_id=db.Column(db.Integer,db.ForeignKey('university.id'),nullable=False)
    name=db.Column(db.String(40),nullable=False,unique=True)
    faculty_id=db.Column(db.Integer,db.ForeignKey('faculty.id'),nullable=False)
    department_id=db.Column(db.Integer,db.ForeignKey('department.id'),nullable=False)

    def getCourse(uni_admin_id): #will also work for faculty-course table
        return Courses.query.filter_by(uni_id=uni_admin_id).all()
    
class Notes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    course_id=db.Column(db.Integer,db.ForeignKey('courses.id'),nullable=False)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)
    Note=db.Column(db.LargeBinary,nullable=False)
    approve=db.Column(db.Boolean,nullable=False)


class Rating(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    note_id=db.Column(db.Integer,db.ForeignKey('notes.id'),nullable=False)
    rating=db.Column(db.Integer,nullable=False)

    def getRatingNote(noteid):
        return int(Rating.query.filter_by(note_id=noteid).first())

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

    def studentcourselist(user_id): #Get all the courses for which a student is registered for...
        student=Student.query.filter_by(user_id=user_id).first()# Get The Student
        studentcourseList=[]#Add Courses he is registered for to this list
        print("THE TEST ID OF THE STUDENT IS ")
        print(student.id)
        StudentCourses=Student_Course.query.filter_by(student_id=student.id).all()#check if this works.

        print("TEST-2 VIEW ALL COURSE")
        for sc in StudentCourses:
            print("Student id is "+str(sc.student_id))
            print("Course id is "+str(sc.course_id))

        for courses in Courses.query.all():
            for studentcourse in StudentCourses:
                if studentcourse.course_id==courses.id:
                    studentcourseList.append(courses)
        
        return studentcourseList


    def ReturnApproveNotesStudent(user_id): #Returns Notes which have been approved by the professor for the courses the student is in
        student=Student.query.get(user_id)
        courseidlist=[]
        FilterStudent=Student_Course.query.filter_by(student_id=student.id).all()
        approveNotes=[]
        for fs in FilterStudent:
            courseidlist.append(fs.course_id)
        
        print("The courses for which this student has registered are- RANS function")
        for course in courseidlist:
            print(course)

        for note in Notes.query.all():
            if note.approve==True and note.course_id in courseidlist:
                approveNotes.append(note)
        
        return approveNotes


