from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from s3_utils import upload_file, list_versions
from models import get_cursor, commit

doc_bp = Blueprint('documents', __name__)

@doc_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    username = request.form.get('username')
    comment = request.form.get('comment', '')
    filename = secure_filename(file.filename)

    # ✅ Pass file stream directly to upload_file
    upload_file(file, filename)

    versions = list_versions(filename)
    version_id = versions[0]['VersionId'] if versions else None

    cur = get_cursor()
    cur.execute("SELECT id FROM documents WHERE filename = %s", (filename,))
    row = cur.fetchone()
    doc_id = row['id'] if row else None

    if not doc_id:
        cur.execute(
            "INSERT INTO documents (filename, owner) VALUES (%s, %s) RETURNING id",
            (filename, username)
        )
        doc_id = cur.fetchone()['id']

    cur.execute("""
        INSERT INTO versions (document_id, s3_version_id, comment, uploaded_by)
        VALUES (%s, %s, %s, %s)
    """, (doc_id, version_id, comment, username))
    
    commit()
    return jsonify({"message": "Upload successful", "version_id": version_id})


@doc_bp.route('/versions/<filename>', methods=['GET'])
def get_versions(filename):
    versions = list_versions(filename)
    return jsonify([{
        'VersionId': v['VersionId'],
        'IsLatest': v['IsLatest'],
        'LastModified': v['LastModified'].isoformat()
    } for v in versions])
