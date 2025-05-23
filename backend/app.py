from flask import Flask, request, jsonify, Blueprint, send_from_directory
from werkzeug.utils import secure_filename
import os
import boto3
import psycopg2
from routes.documents import doc_bp
from routes.user import user_bp
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Register API routes
app.register_blueprint(doc_bp, url_prefix='/documents')
app.register_blueprint(user_bp, url_prefix='/users')
# Load environment variables
load_dotenv()

UPLOAD_FOLDER = '/tmp/uploads'  # Temporary folder for local file storage
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# AWS S3 setup (using environment variable for bucket name)
s3 = boto3.client('s3', region_name=os.getenv('AWS_DEFAULT_REGION'))
BUCKET = os.getenv('S3_BUCKET', 'dms-bucket')  # Use environment variable for bucket name

# PostgreSQL RDS setup (using environment variables for RDS connection details)
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),          # RDS endpoint
    database=os.getenv('DB_NAME', 'dms'),  # Database name
    user=os.getenv('DB_USER', 'dmsadmin'),  # DB user
    password=os.getenv('DB_PASSWORD')  # DB password
)
cur = conn.cursor(cursor_factory=RealDictCursor)

# Document routes
doc_bp = Blueprint('documents', __name__)

@doc_bp.route('/documents/upload', methods=['POST'])
def upload():
    file = request.files['file']
    username = request.form.get('username')
    comment = request.form.get('comment', '')
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Upload to S3 with encryption using AWS KMS
    s3.upload_file(
        file_path, BUCKET, filename,
        ExtraArgs={"ServerSideEncryption": "aws:kms", "SSEKMSKeyId": os.getenv('AWS_KMS_KEY_ID')}
    )

    # Get latest version ID from S3
    versions = s3.list_object_versions(Bucket=BUCKET, Prefix=filename).get('Versions', [])
    version_id = versions[0]['VersionId'] if versions else None

    # Insert document details into PostgreSQL (documents table) and versions table
    cur.execute("SELECT id FROM documents WHERE filename = %s", (filename,))
    row = cur.fetchone()
    if row:
        doc_id = row['id']
    else:
        cur.execute(
            "INSERT INTO documents (filename, owner) VALUES (%s, %s) RETURNING id",
            (filename, username)
        )
        doc_id = cur.fetchone()['id']

    cur.execute("""
        INSERT INTO versions (document_id, s3_version_id, comment, uploaded_by)
        VALUES (%s, %s, %s, %s)
    """, (doc_id, version_id, comment, username))
    conn.commit()

    return jsonify({"message": "Upload successful", "version_id": version_id})

@doc_bp.route('/documents/versions/<filename>', methods=['GET'])
def list_versions(filename):
    versions = s3.list_object_versions(Bucket=BUCKET, Prefix=filename).get('Versions', [])
    return jsonify([
        {
            'VersionId': v['VersionId'],
            'IsLatest': v['IsLatest'],
            'LastModified': v['LastModified'].isoformat()
        } for v in versions
    ])

# Serve frontend (static files)
@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('frontend', path)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
