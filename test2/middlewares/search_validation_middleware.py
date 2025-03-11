from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import re

class SearchValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/search"):
            return await call_next(request)
        try:
            query_params = request.query_params
            if set(query_params.keys()) != {"start", "end"}:
                raise HTTPException(status_code=400, detail="허용되지 않은 쿼리 파라미터")
            for key, value in query_params.items():
                if key in ["start", "end"]:
                    if not re.match(r"^[0-9]+$", value):
                        raise HTTPException(status_code=400, detail=f"'{key}' 값은 양의 정수여야 합니다.")
                    if key == "start" and int(value) % 10 != 0:
                        raise HTTPException(status_code=422, detail=f"'{key}' 시작시간 값은 10의 배수여야 합니다.")
                    if key == "end" and int(value) % 10 != 0:
                        raise HTTPException(status_code=422, detail=f"'{key}' 종료시간 값은 10의 배수여야 합니다.")
                if int(query_params["start"]) >= int(query_params["end"]):
                    raise HTTPException(status_code=422, detail="시작시간은 종료시간보다 작아야 합니다.")
            response = await call_next(request)
            return response
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})