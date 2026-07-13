from celery import Celery, Task
from celery.schedules import crontab
from app import app

celery_app = Celery('tasks', broker='redis://localhost:6379/1', backend='redis://localhost:6379/2' , include=['tasks'])


class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
            
celery_app.Task = FlaskTask      
celery_app.conf.enable_utc = False
celery_app.conf.timezone = 'Asia/Kolkata'


celery_app.conf.beat_schedule = {
    # 'monthly-user-report': {
    #     'task': 'tasks.send_monthly_report',  
    #     'schedule': crontab(hour=16, minute=59, day_of_month=13),
    # },
    
    



    'monthly-user-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(minute='*/1'),
    },
    'daily-reminder':{
        'task': 'tasks.send_daily_reminder',
        'schedule': crontab(minute='*/1'),
    },
}