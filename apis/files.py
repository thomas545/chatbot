from typing import Annotated
from fastapi import APIRouter, Header, UploadFile, File, Response
from core.upload_files import upload_bytes_to_s3

CoreRouters = APIRouter(prefix="/files", tags=["auth"])


@CoreRouters.post("/upload/")
async def upload_file_api(
    file: UploadFile = File(...), user: Annotated[str | None, Header()] = None
):
    # Upload file to S3
    file_bytes = await file.read()
    response = upload_bytes_to_s3(file_bytes, file.filename, f"users_files/{user}")
    return response
