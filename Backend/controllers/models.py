from controllers.database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=True)

    roles = db.relationship('Role', secondary='user_roles')
    company = db.relationship("Company", backref="user", uselist=False)
    student = db.relationship("Student", backref="user", uselist=False)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(255), nullable=False)
    profile = db.Column(db.String(255), nullable=True)
    industry = db.Column(db.String(255), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    blacklisted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    branch = db.Column(db.String(50))
    cgpa = db.Column(db.Float)
    resume = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    title = db.Column(db.String(255))
    salary = db.Column(db.Integer)
    skills_required = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.Date)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    status = db.Column(db.String(255), default="applied")
    date = db.Column(db.Date, default=datetime.utcnow)


class Placement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    position = db.Column(db.String(255))
    salary = db.Column(db.Integer)
    joining_date = db.Column(db.Date)