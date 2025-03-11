from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class UploadValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        form = await request.form()
        if "file" not in form:
            raise HTTPException(status_code=400, detail="파일이 필요합니다.")
        response = await call_next(request)
        return response