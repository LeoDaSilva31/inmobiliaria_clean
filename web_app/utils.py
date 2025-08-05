import boto3
from botocore.exceptions import ClientError
from django.conf import settings # <-- Agrega esta línea

def generar_url_firmada(bucket_name, object_key, expiracion=3600):
    # Asegúrate de que las credenciales están disponibles para boto3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID, # <-- Agrega esta línea
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, # <-- Agrega esta línea
        region_name=settings.AWS_S3_REGION_NAME # <-- Agrega esta línea
    )
    try:
        url_firmada = s3_client.generate_presigned_url('get_object',
                                                       Params={'Bucket': bucket_name,
                                                               'Key': object_key},
                                                       ExpiresIn=expiracion)
    except ClientError as e:
        print(f"Error generando URL firmada: {e}")
        return None
    return url_firmada