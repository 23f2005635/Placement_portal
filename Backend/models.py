from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

from flask_security import UserMixin
from datetime import datetime

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True)
    email=db.Column(db.String(255),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    role=db.Column(db.String(50),nullable=False)
    active=db.Column(db.Boolean,default=True)
    approved=db.Column(db.String(50),default="pending")
    company=db.relationship("Company",backref="user",uselist=False)
    student=db.relationship("Student",backref="user",uselist=False)


class Company(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    company_name=db.Column(db.String(100))
    profile=db.Column(db.String(255))
    industry=db.Column(db.String(100))
    location=db.Column(db.String(100))
    hr_contact=db.Column(db.String(100))
    website=db.Column(db.String(255))
    drives=db.relationship("PlacementDrive",backref="company")


class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    name=db.Column(db.String(100))
    branch=db.Column(db.String(100))
    education=db.Column(db.String(200))
    cgpa=db.Column(db.Float)
    year=db.Column(db.Integer)
    skills=db.Column(db.String(255))
    resume=db.Column(db.String(255))
    applications=db.relationship("Application",backref="student")





class PlacementDrive(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    company_id=db.Column(db.Integer,db.ForeignKey("company.id"))
    job_title=db.Column(db.String(100))
    salary=db.Column(db.Integer)
    job_description=db.Column(db.Text)
    work_location=db.Column(db.String(100))
    eligibility_cgpa=db.Column(db.Float)
    application_deadline=db.Column(db.DateTime)
    approved=db.Column(db.String(50),default="pending")
    applications=db.relationship("Application",backref="drive")


from datetime import datetime

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drive.id"), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Applied")

    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_student_drive'),
    )


class Placement(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey("student.id"))
    company_id=db.Column(db.Integer,db.ForeignKey("company.id"))
    drive_id=db.Column(db.Integer,db.ForeignKey("placement_drive.id"))
    position=db.Column(db.String(100))
    salary=db.Column(db.Integer)
    joining_date=db.Column(db.DateTime)