from tempfile import NamedTemporaryFile
from fastapi import UploadFile
from dtos import CreateInfo
from repositories import InfoRepository, FileRepository
from moviepy.editor import VideoFileClip
from utils import file_util


class UploadService:
    def __init__(self, info_repository: InfoRepository, file_repository: FileRepository):
        self.info_repository = info_repository
        self.file_repository = file_repository
        
    async def upload_video(self, file: UploadFile):
        suffix = file.filename.split(".")[-1]
        file_content = await file.read()
        temp = NamedTemporaryFile(delete=False, suffix=f".{suffix}")
        temp.write(file_content)
        metadata = file_util.get_file_metadata(temp.name)
        info = await self.info_repository.create_info(CreateInfo(file, metadata))
        video = VideoFileClip(temp.name)
        duration = video.duration
        temp.flush()
        temp.close()
        
        for start in range(0, int(duration), 10):
            end = min(start + 10, duration)
            slice_index = start // 10
            slice_video: VideoFileClip = video.subclip(start, end)

            slice_temp = NamedTemporaryFile(delete=False, suffix=f".{suffix}")
            # internet_media_type == "video/h264"
            slice_video.write_videofile(slice_temp.name)
            slice_video_content = slice_temp.read()
            self.file_repository.create_slice_video(info, slice_index, slice_video_content)
            slice_temp.flush()
            slice_temp.close()
        
        return info.id