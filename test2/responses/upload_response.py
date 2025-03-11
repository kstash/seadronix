from .base_response import BaseResponse


class UploadResponse(BaseResponse):
    status: int = 201
    message: str = "file upload success"
    file_id: str