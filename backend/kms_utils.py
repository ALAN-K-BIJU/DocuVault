import boto3
from config import Config

kms_client = boto3.client('kms', endpoint_url=Config.AWS_ENDPOINT_URL)

def encrypt_data(plaintext):
    response = kms_client.encrypt(
        KeyId=Config.AWS_KMS_KEY_ID,
        Plaintext=plaintext
    )
    return response['CiphertextBlob']

def decrypt_data(ciphertext):
    response = kms_client.decrypt(
        CiphertextBlob=ciphertext
    )
    return response['Plaintext']