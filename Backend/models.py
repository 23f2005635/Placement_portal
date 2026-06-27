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
    approved=db.Column(db.Boolean,default=False)
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
    approval_status=db.Column(db.String(50),default="Pending")
    jobs=db.relationship("JobPosition",backref="company")
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


class JobPosition(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    company_id=db.Column(db.Integer,db.ForeignKey("company.id"))
    title=db.Column(db.String(100))
    salary=db.Column(db.Integer)
    skills_required=db.Column(db.String(255))
    description=db.Column(db.Text)


class PlacementDrive(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    company_id=db.Column(db.Integer,db.ForeignKey("company.id"))
    job_title=db.Column(db.String(100))
    job_description=db.Column(db.Text)
    eligibility_branch=db.Column(db.String(100))
    eligibility_cgpa=db.Column(db.Float)
    eligibility_year=db.Column(db.Integer)
    application_deadline=db.Column(db.DateTime)
    status=db.Column(db.String(50),default="Pending")
    applications=db.relationship("Application",backref="drive")


class Application(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey("student.id"))
    drive_id=db.Column(db.Integer,db.ForeignKey("placement_drive.id"))
    job_id=db.Column(db.Integer,db.ForeignKey("job_position.id"))
    application_date=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String(50),default="Applied")


class Placement(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey("student.id"))
    company_id=db.Column(db.Integer,db.ForeignKey("company.id"))
    drive_id=db.Column(db.Integer,db.ForeignKey("placement_drive.id"))
    position=db.Column(db.String(100))
    salary=db.Column(db.Integer)
    joining_date=db.Column(db.DateTime)