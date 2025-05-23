import os

class Config:
    UPLOAD_FOLDER = '/tmp/uploads'
    LOG_FILE = 'logs/dms.log'

    # S3 Bucket
    S3_BUCKET = 'dms-bucket-22bsa10275-academy'

    # RDS Parameters
    DB_PARAMS = {
        'host': 'dms-postgres-db.cw7bhkj9zzgf.us-east-1.rds.amazonaws.com',
        'database': 'dmsdb',  # replace with your DB name
        'user': 'dmsadmin',
        'password': 'YourStrongPassword123!'  # replace this securely
    }

    # AWS Region and KMS
    AWS_REGION = 'us-east-1'
    AWS_KMS_KEY_ID = 'b6583454-4cd3-4b9d-99de-c70123a2d620'
    #AWS_ENDPOINT_URL = None  # Only needed for localstack or local development
