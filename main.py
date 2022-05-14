import os
from flask import Flask, flash, request, redirect, jsonify
import json
from datetime import datetime

from utils.handle_file import save_to_path
from utils.nft import gen_images
from tasks import task_gen_images

from utils.firebase_helper import storage
from utils.constants import HANDLE_DIR
# from utils.email_helper import send_email_text

app = Flask(__name__)

# TODO test
@app.route('/generate-nft', methods=['POST'])
def gen_nft():
    # get form data
    asset_zip = request.files['assetZip']
    quantityConfigStr = request.form.get('quantityConfig')
    quantityConfig = json.loads(quantityConfigStr)
    email = request.form.get('email')
    base_name = request.form.get('baseName')
    collection_description = request.form.get('collectionDescription')
    # save processing path
    now = datetime.now()
    email_path = email + now.strftime("%m-%d-%Y-%H-%M-%S")
    save_to_path(email_path, asset_zip, 'input.zip')
    storage.child(email_path + '/input.zip').put(os.path.join(HANDLE_DIR, email_path, 'input.zip'))
    # add job gen images
    task_gen_images.delay(email, email_path, quantityConfig, base_name, collection_description)
    # remove testing
    # testing only
    # gen_images(email, email_path, quantityConfig, base_name, collection_description)
    

    response.headers.add('Access-Control-Allow-Origin', '*')
    print('asset files saved')
    response = jsonify({
        'result': 'done'
    })

    return response

# TODO complete
# @app.route('/add-contact', methods=['POST'])
# def index():
#     json_data = request.json
#     user_email = json_data['email']
#     send_email_text('hello@nftiply.co', '{user_email} interested in nft metadata generator'.format(user_email=user_email), user_email)
#     return jsonify({
#         'result': 'okok'
#     })

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
