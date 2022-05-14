import os
from werkzeug.utils import secure_filename
from zipfile import ZipFile
from utils.constants import HANDLE_DIR, ASSETS_DIR

def save_to_path(path, file, file_name=None):
    save_path = os.path.join(HANDLE_DIR, path)
    os.makedirs(save_path, exist_ok=True)
    file.save(os.path.join(save_path, secure_filename(file.filename) if not file_name else file_name ))

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_zip(zip_name, email_path, asset_path=ASSETS_DIR):
    save_path = os.path.join(HANDLE_DIR, email_path)
    with ZipFile(os.path.join(save_path, zip_name)) as zip_ref:
        for zip_info in zip_ref.infolist():
            filename = os.path.basename(zip_info.filename)
            # skip directories
            if not filename:
                continue
            zip_info.filename = '/'.join(zip_info.filename.split('/')[1:])
            asset_dir = os.path.join(save_path, asset_path)
            zip_ref.extract(zip_info, asset_dir)