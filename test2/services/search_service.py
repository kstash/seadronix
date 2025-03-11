import io
import os
from tempfile import NamedTemporaryFile
from repositories import InfoRepository, FileRepository
from schemas import Info
from gridfs.grid_file import GridOut
from pymongo.cursor import Cursor
from moviepy.editor import VideoFileClip, concatenate_videoclips


class SearchService:
    def __init__(self, info_repository: InfoRepository, file_repository: FileRepository):
        self.info_repository = info_repository
        self.file_repository = file_repository
    
    def get_slice_file(self, info_id: str, slice_index: int):
        self.info_repository.get_info_by_id(info_id)
        slice_file = self.file_repository.get_slice_video(info_id, slice_index)
        return slice_file

    def get_slice_files(self, info_id: str, start: int, end: int):
        start_index = start // 10
        end_index = (end - 1) // 10
        self.info_repository.get_info_by_id(info_id)
        slice_files = self.file_repository.get_slice_videos_by_index_range(info_id, start_index, end_index)
        return slice_files
    
    def get_info(self, info_id: str):
        info = self.info_repository.get_info_by_id(info_id)
        return info
    
    def get_composed_file(self, info: Info, slice_files: Cursor[GridOut]):
        temp_slice_file_paths = []
        for slice_file in slice_files:
            temp_slice_file = NamedTemporaryFile(delete=False, suffix=f".{info.suffix}")
            temp_slice_file.write(slice_file.read())
            temp_slice_file.flush()
            temp_slice_file_paths.append(temp_slice_file.name)
        
        slice_videos = [VideoFileClip(temp_slice_file_path) for temp_slice_file_path in temp_slice_file_paths]
        search_video = concatenate_videoclips(slice_videos, method="compose")

        for temp_file in temp_slice_file_paths:
            os.remove(temp_file) if os.path.exists(temp_file) else None

        return search_video
    
    def get_stream_by_video(self, info: Info, search_video: VideoFileClip):
        stream = io.BytesIO()
        temp_file = NamedTemporaryFile(suffix=f".{info.suffix}")
        search_video.write_videofile(temp_file.name)
        with open(temp_file.name, "rb") as f:
            stream.write(f.read())
        stream.seek(0)
        temp_file.close()

        return stream