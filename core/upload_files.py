from fastapi import FastAPI, File, UploadFile, HTTPException
import boto3
from .environment import get_environ
from .files import get_file_content_type, get_s3_file_path

# S3 Configuration
AWS_REGION = get_environ("AWS_REGION")
AWS_ACCESS_KEY_ID = get_environ("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_environ("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = get_environ("AWS_S3_BUCKET_NAME")
AWS_S3_HOST = get_environ("AWS_S3_HOST")


# Initialize S3 client
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def upload_bytes_to_s3(
    file_content: bytes, file_name: str, folder_name: str = "uploaded"
) -> dict:
    """Upload a file to Amazon S3"""
    file_path = f"{folder_name}/{file_name}"

    try:
        s3_client.put_object(
            Bucket=AWS_S3_BUCKET_NAME,
            Key=file_path,
            Body=file_content,
            ACL="public-read",
            ContentType=get_file_content_type(file_name),
        )
        return {
            "url": get_s3_file_path(AWS_S3_BUCKET_NAME, file_path),
            "file_name": file_name,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
