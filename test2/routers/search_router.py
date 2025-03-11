from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from services import SearchService
from dependencies import get_search_service


router = APIRouter(prefix="/search", tags=["search"])


# 영상 범위 검색하여 stream으로 반환
@router.get(
    "/stream/{info_id}", 
    summary="영상 범위 검색하여 stream으로 반환합니다.",
    description="저장한 파일의 start(초) ~ end(초)까지의 영상을 스트림으로 반환합니다. 이때 시작시간은 종료시간보다 작아야 하고, 시작시간과 종료시간은 각각 10의 배수의 정수이어야 합니다.",
    response_class=StreamingResponse
)
async def search_video_by_time_as_stream(
    info_id: str,
    start: int = Query(...), 
    end: int = Query(...),
    search_service: SearchService = Depends(get_search_service)
):
    try:
        info = search_service.get_info(info_id)
        slice_files = search_service.get_slice_files(info_id, start, end)
        if not slice_files:
            raise HTTPException(status_code=404, detail="검색 영상 범위 내 영상 없음")

        search_video = search_service.get_composed_file(info, slice_files)
        video_stream = search_service.get_stream_by_video(info, search_video)

        headers = {
            "Content-Disposition": f"attachment; filename={info.filename}",
            "Content-Type": info.content_type
        }
        return StreamingResponse(
            video_stream,
            media_type=info.content_type,
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"search video fail: {str(e)}")