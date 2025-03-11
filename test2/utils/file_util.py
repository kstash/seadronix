from fastapi import HTTPException
from pymediainfo import MediaInfo
from schemas import MetaData


def get_file_metadata(file_path: str) -> MetaData:
    try:
        media_info = MediaInfo.parse(file_path)
        metadata = MetaData.to_cls(media_info)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"file metadata extract fail: {str(e)}")
