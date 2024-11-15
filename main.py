from flask import Flask, render_template, request, redirect
from google.cloud import storage
import os

# Initialize the Flask app
app = Flask(__name__)

# Set up Google Cloud Storage client using your service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apare/git_repos/template/capable-gasket-438700-f2-1dd5ea7e9a1c.json"

# Define the Google Cloud Storage bucket
BUCKET_NAME = 'bkt-vendor-data'

def upload_to_gcs(file, bucket_name, destination_blob_name):
    """Uploads a file to the specified GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file)
    return f"File uploaded to {destination_blob_name}."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request"
    file = request.files['file']

    if file.filename == '':
        return "No file selected for uploading"
    
    # Upload to Google Cloud Storage
    destination_blob_name = file.filename  # Optionally, customize the name
    upload_to_gcs(file, BUCKET_NAME, destination_blob_name)

    return f"File {file.filename} uploaded successfully to Google Cloud Storage."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
