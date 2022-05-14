import pyrebase
from utils.app_config import app_environment

config = {
  "apiKey": app_environment["firebase_api_key"],
  "authDomain": app_environment["firebase_auth_domain"],
  "projectId": app_environment["firebase_projectId"],
  "storageBucket": app_environment["firebase_storageBucket"],
  "databaseURL": ""
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()
