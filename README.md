## Placement Portal Application 

### Problem statement
Institutes require efficient systems to manage campus recruitment activities involving companies and students. Currently, many institutes rely on spreadsheets, emails, or manual coordination, which makes it difficult to manage company approvals, placement drives, student registrations, and application tracking.

### Folder structure

```text
PLACEMENT_PORTAL
├── Backend
│   ├── __pycache__/
│   ├── env/
│   ├── instance/
│   ├── templates/
│   ├── venv/
│   ├── apis.py
│   ├── app.py
│   ├── celery_worker.py
│   ├── celerybeat-schedule
│   ├── models.py
│   ├── requirement.txt
│   ├── tasks.py
│   └── wget
├── Frontend
│   ├── .vscode/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   ├── .gitignore
│   ├── index.html
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
└── README.md
```

### Technologies used
Flask for API
VueJS for UI
Jinja2 templates for sending monthly reports
Bootstrap for HTML generation and styling 
SQLite for databaseRedis for caching
Redis and Celery for batch jobs

### Roles & Functionalities
This platform has three roles:


Admin (Institute Placement Cell)

Admin is the pre-existing superuser of the application.
Can approve or reject company registrations.
Can approve or reject placement drives created by companies.
Can view and manage all students, companies, and placement drives.
Can search for students or companies.
Can blacklist or deactivate companies and students if required.
Can view reports and placement statistics.

Company

Can register their company profile on the platform.
Can create placement drives only after admin approval.
Can view student applications for their placement drives.
Can shortlist students and update application status.
Can schedule interviews and update final selection results.

Student

Can register, log in, and update their profile.
Can view approved placement drives.
Can apply for placement exams/drives created by companies.
Can view application status and placement history.

### Database schema
```## Database Schema

```text
                           +----------------------+
                           |   PlacementDrive     |
                           +----------------------+
                           | id (PK)              |
                           | company_id (FK)      |
                           | title               |
                           | description         |
                           | location            |
                           | eligibility         |
                           | salary              |
                           | drive_date          |
                           +----------^-----------+
                                      |
                                      | 1
                                      |
                                      | N
                           +----------+-----------+
                           |      Company         |
                           +----------------------+
                           | id (PK)              |
                           | user_id (FK)         |
                           | company_name         |
                           | website              |
                           | industry             |
                           | approved             |
                           +----------^-----------+
                                      |
                                      | 1
                                      |
                     +----------------+----------------+
                     |                                 |
                     |                                 |
               +-----+------+                   +------+------+
               |    User    |                   |   Student   |
               +------------+                   +-------------+
               | id (PK)    |                   | id (PK)     |
               | username   |                   | user_id(FK) |
               | email      |                   | first_name  |
               | password   |                   | last_name   |
               | role       |                   | cgpa        |
               | active     |                   | resume      |
               +------------+                   +------+------+
                                                       |
                                                       | 1
                                                       |
                                                       | N
                                           +-----------+-----------+
                                           |     Application        |
                                           +------------------------+
                                           | id (PK)                |
                                           | student_id (FK)        |
                                           | drive_id (FK)          |
                                           | status                 |
                                           | applied_on             |
                                           +-----------+------------+
                                                       |
                                                       | 1
                                                       |
                                                       | 0..1
                                           +-----------+-----------+
                                           |      Placement         |
                                           +------------------------+
                                           | id (PK)                |
                                           | application_id (FK)    |
                                           | joining_date           |
                                           | package                |
                                           | status                 |
                                           +------------------------+
```

## Relationships

| Parent Entity | Child Entity | Relationship |
|---------------|-------------|--------------|
| User | Company | One-to-One (A company account belongs to one user) |
| User | Student | One-to-One (A student profile belongs to one user) |
| Company | PlacementDrive | One-to-Many (A company can create multiple placement drives) |
| Student | Application | One-to-Many (A student can apply to multiple drives) |
| PlacementDrive | Application | One-to-Many (A placement drive can receive multiple applications) |
| Application | Placement | One-to-One (An application may result in one placement record) |