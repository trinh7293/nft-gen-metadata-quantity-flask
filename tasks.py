import celery
from utils.nft import gen_images
from utils.app_config import app_environment

app = celery.Celery('tasks', broker=app_environment["celery_broker"])

@app.task
def task_gen_images(email, email_path, quantityConfig, base_name, collection_description):
    gen_images(email, email_path, quantityConfig, base_name, collection_description)
