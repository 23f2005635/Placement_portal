from celery_worker import celery_app
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from flask_mail import Message
import smtplib 
from flask import render_template
from models import User, Company,Student,PlacementDrive, Application, Placement

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS='23f2005635@ds.study.iitm.ac.in'
SENDER_PASSWORD='AaBbCcDd'

def send_email(to_address,subject,message,content="text",attachment=None):
    msg = MIMEMultipart()
    msg['To']=to_address
    msg['From']=SENDER_ADDRESS
    msg['Subject']=subject
    if content == "html":
        msg.attach(MIMEText(message,'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment,"rb") as a:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment: filename={attachment}")
        msg.attach(part)          

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT )
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

@celery_app.task
def send_monthly_report():
    # Logic to generate report and send email
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        return "No admin user found"
    ddata=[]
    adata=[]
    pdata=[]
    drive=PlacementDrive.query.all()
    application=Application.query.all()
    placement=Placement.query.all()
    for d in drive:
        ddata.append({
            'id':d.id,
            'company_id':d.company_id,
            'job_title':d.job_title,
        })
    for a in application:
        adata.append({
            'id':a.id,
            'student_id':a.student_id,
            'drive_id':a.drive_id,
            'status':a.status,
        })
    for p in placement:
        pdata.append({
            'id':p.id,
            'student_id':a.student_id,
            'drive_id':a.drive_id,

        })

    html= render_template('monthly_report.html',drive=ddata,application=adata,placement=pdata)
    send_email(admin.email, "Monthly Report", html, content="html")
    return "Monthly report sent to admin."
    
















    
@celery_app.task
def send_daily_reminder():
    now = datetime.utcnow()
    next_day = now + timedelta(days=1)

    applications = (
        Application.query.join(Student, Application.student_id == Student.id)
        .join(User, Student.user_id == User.id)
        .join(PlacementDrive, Application.drive_id == PlacementDrive.id)
        .join(Company, PlacementDrive.company_id == Company.id)
        .filter(User.role == "student")
        .filter(User.active == True)
        .filter(PlacementDrive.application_deadline >= now)
        .filter(PlacementDrive.application_deadline <= next_day)
        .all()
    )

    for app in applications:
        student = app.student
        user = student.user
        drive = app.drive
        company = drive.company

        html = render_template(
            "daily_reminder.html",
            student_name=student.name,
            company_name=company.company_name,
            job_title=drive.job_title,
            work_location=drive.work_location,
            deadline=drive.application_deadline,
        )

        msg = Message(
            subject="Placement Deadline Reminder",
            recipients=[user.email]
        )
        msg.body = f"""
Hello {student.name},

This is a reminder that the deadline for {company.company_name} - {drive.job_title}
is {drive.application_deadline.strftime('%d %b %Y %I:%M %p')}.

Please complete your application before the deadline.
"""
        msg.html = html
        mail.send(msg)
    

        