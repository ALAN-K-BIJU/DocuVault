from config import Config
import boto3

# Create the S3 client
s3 = boto3.client(
    "s3",
    region_name=Config.AWS_REGION
)

BUCKET = Config.S3_BUCKET

def upload_file(file_stream, filename):
    """
    Uploads a file to S3 with server-side encryption using the specified KMS key.
    """
    s3.upload_fileobj(
        Fileobj=file_stream,  # ✅ file_stream now implements .read()
        Bucket=BUCKET,
        Key=filename,
        ExtraArgs={
            "ServerSideEncryption": "aws:kms",
            "SSEKMSKeyId": Config.AWS_KMS_KEY_ID
        }
    )

def list_versions(filename):
    """
    Lists all versions of a file stored in S3.
    """
    response = s3.list_object_versions(Bucket=BUCKET, Prefix=filename)
    return response.get("Versions", [])
