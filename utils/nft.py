import os
import json
import shutil
from tokenize import Number
from progressbar import progressbar
from PIL import Image

from utils.constants import HANDLE_DIR, OUTPUT_DIR, JSON_DIR, IMAGES_DIR, ASSETS_DIR
from utils.handle_file import extract_zip
from utils.metadata_helper import gen_metadata
from utils.firebase_helper import storage
from utils.email_helper import send_email_attachment

# handling location
handle_path = None
output_path = None
json_path = None
images_path = None

# make nesscessary paths for output
def make_paths(email_path):
  global handle_path
  global output_path
  global json_path
  global images_path
  handle_path = os.path.join(HANDLE_DIR, email_path)
  output_path = os.path.join(HANDLE_DIR, email_path, OUTPUT_DIR)
  json_path = os.path.join(output_path, JSON_DIR)
  images_path = os.path.join(output_path, IMAGES_DIR)
  os.makedirs(json_path, exist_ok=True)
  os.makedirs(images_path, exist_ok=True)

# download assets to handle path
def download_assets(email_path):
    zip_ref = email_path + '/input.zip'
    zip_path = os.path.join(handle_path, 'input.zip')
    storage.child(zip_ref).download(zip_path, zip_path)
    extract_zip('input.zip', email_path)

# save metadata to json folder
def save_metadata(
  metadata_list
):
  for index, meta in enumerate(metadata_list):
    item_json_path = os.path.join(handle_path, OUTPUT_DIR, JSON_DIR, str(index))
    with open(item_json_path, 'w') as f:
      json.dump(meta, f)

# generate single image from its metadata
def gen_single_image(
  metadata,
  img_name
):
  filepaths = []
  assets_path = os.path.join(handle_path, ASSETS_DIR)
  for attr in metadata["attributes"]:
    filepaths.append(
      os.path.join(assets_path,
      attr['trait_type'],
      attr['trait_value'] + '.png')
    )
  img_output_path = os.path.join(images_path, img_name)
  # Treat the first layer as the background
  bg = Image.open(os.path.join(filepaths[0]))
  
  
  # Loop through layers 1 to n and stack them on top of another
  for filepath in filepaths[1:]:
      if filepath.endswith('.png'):
          img = Image.open(os.path.join(filepath))
          bg.paste(img, (0,0), img)
  
  # Save the final image into desired location
  bg.save(img_output_path)

# archive result to zip file 
def archive_files(email_path):
    shutil.make_archive(output_path, 'zip', root_dir=output_path)
    storage.child(email_path + '/output.zip').put(os.path.join(handle_path, 'output.zip'))


# send result to receiver
def handle_send_email(receiver_email):
    file_path = os.path.join(handle_path, 'output.zip')
    subject = "Metadata result"
    body = "Metadata result from Nftiply"
    send_email_attachment(receiver_email, subject, body, file_path)

# save images and json metadata to folder, send zip file output to email receiver
def gen_images(
  email,
  email_path,
  quantityConfig,
  base_name,
  collection_description
):
  print("Download assets...")
  make_paths(email_path)

  download_assets()
  # init handle_path
  print("Generating metadata...")
  metadata_list = gen_metadata(
    quantityConfig,
    base_name,
    collection_description
  )
  # Create metadatas
  print("Saving metadata...")
  save_metadata(metadata_list)
  # Create the images
  print("Creating images...")
  meta_len = len(metadata_list)
  zfill_count = len(str(meta_len - 1))
  for i in progressbar(range(meta_len)):
    img_name = str(i).zfill(zfill_count) + '.png'
    gen_single_image(metadata_list[i], img_name)
  archive_files(email_path)
  print("Sending results...")
  handle_send_email(email)
  print("Task complete!")