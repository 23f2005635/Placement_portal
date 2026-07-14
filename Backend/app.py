from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Company, Student,Application, PlacementDrive,Placement
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt

from flask_caching import Cache


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'


CORS(app, resources={
    r"/api/*": {
        "origins": "http://localhost:5173",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

db.init_app(app)

jwt = JWTManager(app)

cache = Cache(app)





@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first() or User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],        
        password=generate_password_hash(data['password']),
        role=data['role'],
        approved="approved" if data['role'] == 'student' else "pending"
    )
    if data['role'] == 'company':
        company = Company(
            company_name=data['company_name'],
            profile=data['profile'],
            industry=data['industry'],
            location=data['company_address'],
            hr_contact=data['hr_contact'],
            website=data.get('website', '')
        )
        user.company = company
        db.session.add(company)
        
        
    db.session.add(user)

    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 200











@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']) and user.role == 'student' and user.approved=='approved':
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Login successful', 'data': {'username': user.username, 'email': user.email, 'role': user.role, 'access_token': access_token}}), 200
    
    elif user and check_password_hash(user.password, data['password']) and user.role == 'company' and user.approved=='approved':
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'message': 'Login successful', 'data': {'username': user.username, 'email': user.email, 'role': user.role, 'access_token': access_token}}), 200
        
    else:
        return jsonify({'message': 'Invalid username or password or not approved'}), 401











@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']) and user.role == 'admin':
        access_token = create_access_token(identity= str(user.id), additional_claims={'role': user.role})
        return jsonify({'message': 'Admin login successful', 'data': {'username': user.username, 'email': user.email, 'role': user.role, 'access_token': access_token}}), 200
    else:
        return jsonify({'message': 'Invalid admin credentials'}), 401
    









@app.route('/api/admin/fetchtotaldetails', methods=['GET'])
@jwt_required()
@cache.cached(timeout=5)
def fetch_total_details():
    if get_jwt()['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    total_students = User.query.filter_by(role='student').count()
    total_companies = User.query.filter_by(role='company', approved='approved').count()
    total_placements = Placement.query.count()
    pending_companies = User.query.filter_by(role='company', approved='pending').all()
    approved_companies = Company.query.join(User).filter(
    User.role == "company",
    User.approved == "approved"
).all()
    pending_companies_data = []
    studentapplication = []
    applications = Application.query.all()
    placements = Placement.query.all()
    # approved_company = Company.query.filter_by(approved='approved').all()
    students=Student.query.join(User).filter(
    User.role == "student",
    User.approved == "approved"
).all()
    companya=[]
    student=[]
    pending_drive=[]
    placement=[]
    drive = PlacementDrive.query.filter_by(approved='pending').all()

    for company in pending_companies:
        pending_companies_data.append({
            'id': company.id,
            'username': company.username,
            'email': company.email,
        })
    for p in placements:
        placement.append({
            'id':p.id,
            "student_name": Student.query.get(p.student_id).name,
            "company_name": Company.query.get(p.company_id).company_name,
            'drive_id':p.drive_id,
            'salary':p.salary,
        })
    for prdrive in drive:
        pending_drive.append({
            'id':prdrive.id,
            'company_id':prdrive.company_id,
            'job_title':prdrive.job_title,
            'job_description':prdrive.job_description,
            'work_location':prdrive.work_location,
            'eligibility_cgpa':prdrive.eligibility_cgpa,
            'application_deadline':prdrive.application_deadline,
            'company_name':prdrive.company.company_name,
            'hr_contact':prdrive.company.hr_contact,
        })
        # print(pending_drive)

    for application in applications:
        
        studentapplication.append({
            'id': application.student.user_id,
            'username': application.student.user.username,
            'email': application.student.user.email,
            'drive_id': application.drive.id,
            'job_title': application.drive.job_title,
            'status' : application.status,
                
        })
    for company in approved_companies:
        companya.append({
            'id':company.id,
            'user_id':company.user_id,
            'name':company.company_name,
            'profile':company.profile,
            'industry':company.industry,
            'location':company.location,
            'hr_contact':company.hr_contact,
            'website':company.website,
        })

    for studenti in students:
        student.append({
            'id' :studenti.id,
            'user_id':studenti.user_id,
            'name':studenti.name,
            'branch':studenti.branch,
            'education':studenti.education,
            'cgpa':studenti.cgpa,
            'year':studenti.year,
            'skills':studenti.skills,
            'resume':studenti.resume,
        })
        

    return jsonify({
        'total_students': total_students,
        'total_companies': total_companies,
        'total_placements': total_placements,
        'pending_companies': pending_companies_data,
        'studentapplication':studentapplication,
        'pending_drive':pending_drive,
        'company': companya,
        'student':student,
        'placements':placement
        
    }), 200





@app.route('/api/updatestudent',methods=['POST'])
@jwt_required()
def updatestudent():
    current_user_id = get_jwt_identity()

    current_user = User.query.get(int(current_user_id))

    if not current_user or current_user.role != 'student':
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    
    student1 = Student.query.filter_by(user_id=current_user.id).first()

    if not student1:
        student1 = Student(user_id=current_user.id)
        db.session.add(student1)

    student1.name = data.get('student_name')
    student1.branch = data.get('branch')
    student1.education = data.get('education')
    student1.cgpa = data.get('cgpa')
    student1.year = data.get('year')
    student1.skills = data.get('skills')

    db.session.commit()
    return jsonify({'message': 'Student Profile successfully'}), 201





@app.route('/api/admin/approve_company', methods=['POST'])
@jwt_required()
def approve_company():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    company_id = request.get_json().get('company_id')
    company = Company.query.filter_by(user_id=company_id).first()
    if not company:
        return jsonify({'message': 'company not found'}), 404

    company.user.approved = "approved"
    db.session.commit()

    return jsonify({'message': 'user removed successfully'}), 200












@app.route('/api/admin/remove_company', methods=['POST'])
@jwt_required()
def remove_company():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    company_id = request.get_json().get('company_id')
    user = User.query.filter_by(id=company_id).first()
    if not user:
        return jsonify({'message': 'user not found'}), 404

    user.approved = "removed"
    db.session.commit()

    return jsonify({'message': 'user removed successfully'}), 200









@app.route('/api/create_placement_drive', methods=['POST'])
@jwt_required()
def create_placement_drive():
    current_user_id = get_jwt_identity()

    current_user = User.query.get(int(current_user_id))

    if not current_user or current_user.role != 'company':
        return jsonify({'message': 'Unauthorized access'}), 403

    company = Company.query.filter_by(user_id=current_user.id).first()

    if not company:
        return jsonify({'message': 'Company profile not found'}), 404

    data = request.get_json()
    placement_drive = PlacementDrive(
    company_id=company.id,
    job_title=data.get('jobTitle'),
    job_description=data.get('jobDescription'),
    work_location=data.get('workLocation'),
    eligibility_cgpa=data.get('eligibilityCgpa'),
    application_deadline=datetime.strptime(
            data.get('applicationDeadline'),
            '%Y-%m-%d'
        ).date(),
    approved="pending",
    salary=data.get('salary')
    )
    db.session.add(placement_drive)
    db.session.commit()

    return jsonify({'message': 'Placement drive created successfully'}), 201













@app.route('/api/admin/approve_drive', methods=['POST'])
@jwt_required()
def approve_placement_drive():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    drive_id = request.get_json().get('drive_id')
    placement_drive = PlacementDrive.query.get(drive_id)
    if not placement_drive:
        return jsonify({'message': 'Placement drive not found'}), 404

    placement_drive.approved = "approved"
    db.session.commit()

    return jsonify({'message': 'Placement drive approved successfully'}), 200





@app.route('/api/admin/remove_drive', methods=['POST'])
@jwt_required()
def remove_placement_drive():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    drive_id = request.get_json().get('drive_id')
    placement_drive = PlacementDrive.query.get(drive_id)
    if not placement_drive:
        return jsonify({'message': 'Placement drive not found'}), 404

    placement_drive.approved = "removed"
    db.session.commit()

    return jsonify({'message': 'Placement drive approved successfully'}), 200















@app.route('/api/companies', methods=['GET'])
@jwt_required()
def get_companies():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'student':
        return jsonify({'message': 'Unauthorized access'}), 403

    companies = Company.query.filter(
    Company.user.has(approved="approved")
).all()
    companies_data = []
    for company in companies:
        companies_data.append({
            'id': company.id,
            'company_name': company.company_name,
            'profile': company.profile,
            'industry': company.industry,
            'location': company.location,
            'hr_contact': company.hr_contact,
            'website': company.website
        })

    return jsonify(companies_data), 200









@app.route('/api/show_current_user', methods=['GET'])
@jwt_required()
def show_current_user():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(int(current_user_id))

    if not current_user:
        return jsonify({'message': 'User not found'}), 404
    
    print("User ID:", current_user.id)

    print("Student object:", current_user.student)
    
    if current_user.role == 'student':
        student = current_user.student
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'role': current_user.role,
            'active': current_user.active,
            'approved': current_user.approved,
            'name': student.name,
            'branch': student.branch,
            'education': student.education,
            'cgpa': student.cgpa,
            'year': student.year,
            'skills': student.skills,
            'resume': student.resume
        }

    elif current_user.role == 'company':
        company = current_user.company
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'role': current_user.role,
            'active': current_user.active,
            'approved': current_user.approved,
            'company_name': company.company_name,
            'profile': company.profile,
            'industry': company.industry,
            'location': company.location,
            'hr_contact': company.hr_contact,
            'website': company.website
        }

    return jsonify(user_data), 200





















@app.route('/api/company/update_profile', methods=['PUT'])
@jwt_required()
def update_company_profile():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'company':
        return jsonify({'message': 'Unauthorized access'}), 403

    company = current_user.company
    if not company:
        return jsonify({'message': 'Company not found'}), 404

    data = request.get_json()
    company.company_name = data.get('company_name', company.company_name)
    company.profile = data.get('profile', company.profile)
    company.industry = data.get('industry', company.industry)
    company.location = data.get('location', company.location)
    company.hr_contact = data.get('hr_contact', company.hr_contact)
    company.website = data.get('website', company.website)

    db.session.commit()

    return jsonify({'message': 'Company profile updated successfully'}), 200


























@app.route('/api/company/details', methods=['POST'])
def company_details():
    data = request.get_json()
    
    company_id = data.get("company_id")

    company = Company.query.get(company_id)
    drives = PlacementDrive.query.filter_by(company_id=company_id,approved='approved').all()
    
    return jsonify({
        "company": {
            "id": company.id,
            "name": company.company_name,
            "industry": company.industry,
            "location": company.location
        },
        "placement_drives": [
            {
                "id": d.id,
                "title": d.job_title
                
            } for d in drives
        ]
    })








@app.route('/api/ApplyPlacement',methods=['POST'])
@jwt_required()
def ApplyPlacement():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'student':
        return jsonify({'message': 'Unauthorized access'}), 403

    student = current_user.student
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    data = request.get_json()

    drive_id = data.get("drive_id")

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({'message': 'Placement drive not found'}), 404

    
    if student.cgpa < drive.eligibility_cgpa:
        return jsonify({'message': 'Student is not eligible for this placement drive'}), 400
    
    # Create a new application
    application = Application(
        student_id=student.id,
        drive_id=drive.id
    )
    db.session.add(application)
    db.session.commit()

    return jsonify({'message': 'Application submitted successfully'}), 201







@app.route('/api/fetch_drive',methods=['GET'])
@jwt_required()
def fetch_drive():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'company':
        return jsonify({'message': 'Unauthorized access'}), 403
    drives=[]
    application=[]
    companyy=current_user.company
    drivess=companyy.drives
    for drive in drivess:
        if drive.approved=='approved':
            drives.append({
                'id':drive.id,
                'job_title':drive.job_title,
                'eligibility':drive.eligibility_cgpa
            })
        appls=drive.applications
        for appl in appls:
            if appl.status=='Applied':
                application.append({
                    'id':appl.id,
                    'drive_id':appl.drive_id,
                    'student_id':appl.student_id,
                    'student_name':appl.student.name,
                    'cgpa':appl.student.cgpa,
                    'application_date':appl.application_date,
                })

   
    return jsonify({
    "drives": drives,
    "applications": application
})







@app.route('/api/approveappl',methods=['POST'])
@jwt_required()
def approveappl():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    data=request.get_json()
    appl_id=data.get('id')
    if current_user.role != 'company':
        return jsonify({'message': 'Unauthorized access'}), 403

    appl=Application.query.get(appl_id)
    appl.status="Placed"

    placement=Placement(
        student_id=appl.student_id,
        company_id = current_user.company.id,
        drive_id=appl.drive_id,
        position=appl.drive.job_title,
        salary=appl.drive.salary,
        joining_date=datetime.utcnow()

    )
    db.session.add(placement)
    db.session.commit()
    return jsonify({"message": "Application approved successfully"})






@app.route('/api/removeappl',methods=['POST'])
@jwt_required()
def removeappl():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    data=request.get_json()
    appl_id=data.get('id')
    if current_user.role != 'company':
        return jsonify({'message': 'Unauthorized access'}), 403

    appl=Application.query.get(appl_id)
    appl.status="Not placed"

    # placement=Placement(
    #     student_id=appl.student_id,
    #     company_id = current_user.company.id,
    #     drive_id=appl.drive_id,
    #     position=appl.drive.job_title,
    #     salary=appl.drive.salary,
    #     joining_date=datetime.utcnow()

    # )
    db.session.commit()
    return jsonify({"message": "Application removed successfully"})












@app.route('/api/applhist',methods=['GET'])
@jwt_required()
def applhist():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    student=current_user.student
    applications=Application.query.filter_by(student_id=student.id).all()
    applicationhist=[]
    for a in applications:
        applicationhist.append({
            'id':a.id,
            'student_id':a.student_id,
            'drive_id':a.drive_id,
            'application_date':a.application_date,
            'status':a.status
        })
    return jsonify({'applicationhist':applicationhist})










if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@gmail.com', password=generate_password_hash('admin'), role='admin',
            approved="approved")
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)