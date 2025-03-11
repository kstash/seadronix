from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from responses import UploadResponse
from services import UploadService
from dependencies import get_upload_service

router = APIRouter(prefix="/upload", tags=["upload"])

# # 영상 일반 업로드
# @router.post("/")
# async def upload_video(file: UploadFile = File(...)):
#     try:
#         suffix = file.filename.split(".")[-1]
#         temp_file = NamedTemporaryFile(delete=False, suffix=f".{suffix}")
#         file_content = await file.read()
#         temp_file.write(file_content)
#         temp_file.flush()
#         metadata = file_service.get_file_metadata(temp_file.name)
#         file_id = slice_video_collection.put(file_content, **metadata)
#         return {"message": "file upload success", "file_id": str(file_id)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"file upload fail: {str(e)}")
#     finally:
#         temp_file.close()
#         if os.path.exists(temp_file.name):
#             os.remove(temp_file.name)


# 10초 간격으로 자른 업로드
@router.post(
    path="/sliced",
    summary="10초 간격으로 자른 영상을 업로드합니다.",
    description="업로드하려는 영상 파일을 10초 간격으로 잘라 각각 DB에 저장합니다. 마지막 10초 간격의 영상은 10초가 안되더라도 저장합니다.",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Upload Success"},
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
        500: {"description": "Upload Error"}
    }
)
async def upload_sliced_video(
    file: UploadFile = File(...),
    upload_service: UploadService = Depends(get_upload_service)
):
    try:
        info_id = await upload_service.upload_video(file)
        return UploadResponse(file_id=str(info_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"file upload fail: {str(e)}")
