import os
from dotenv import load_dotenv
load_dotenv()

app_environment = {
  "firebase_api_key": os.environ.get('FIREBASE_API_KEY'),
  "firebase_auth_domain": os.environ.get('FIREBASE_AUTH_DOMAIN'),
  "firebase_projectId": os.environ.get('FIREBASE_PROJECT_ID'),
  "firebase_storageBucket": os.environ.get('FIREBASE_STORAGE_BUCKET'),
  "smtp_server": os.environ.get('SMTP_SERVER'),
  "smtp_port": os.environ.get('SMTP_PORT'),
  "smtp_user_name": os.environ.get('SMTP_USER_NAME'),
  "smtp_password": os.environ.get('SMTP_PASSWORD'),
  "sender_email": os.environ.get('SENDER_EMAIL'),
  "celery_broker": os.environ.get('CELERY_BROKER')

} 