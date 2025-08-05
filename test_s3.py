import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
BUCKET = os.environ.get('AWS_STORAGE_BUCKET_NAME')
REGION = os.environ.get('AWS_S3_REGION_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

file_name = 'test_file.txt'
with open(file_name, 'w') as f:
    f.write('Este es un archivo de prueba.')

try:
    s3_client.upload_file(file_name, BUCKET, file_name)
    print(f"Archivo '{file_name}' subido exitosamente.")
except Exception as e:
    print(f"Error al subir el archivo: {e}")

os.remove(file_name)