import os
import requests
import tempfile
import mimetypes
from typing import Tuple, Any


def get_url_extension(url: str) -> Tuple[Any, Any]:
    file_type, encoding = mimetypes.guess_type(url, strict=True)
    extension = mimetypes.guess_extension(file_type, strict=False)
    return file_type, extension


def delete_files(file_paths: list) -> bool:
    for file_path in file_paths:
        if not file_path:
            continue

        try:
            os.remove(file_path)
        except Exception as e:
            pass
            # TODO add logger

    return True


def save_url_to_local_file(url: str) -> Tuple[str, str]:
    response = requests.get(
        url, headers={"User-Agent": "Mozilla/5.0"}, stream=True, timeout=300
    )

    file_type, extension = get_url_extension(url)
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tf:
        local_path = tf.name
        for chunk in response.iter_content(chunk_size=512 * 1024):
            if chunk:
                tf.write(chunk)

    return file_type, local_path
