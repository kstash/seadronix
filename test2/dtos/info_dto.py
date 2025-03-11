from typing import List
from fastapi import UploadFile
from schemas import MetaData


class CreateInfo:
    filename: str
    suffix: str
    content_type: str
    generals: List
    videos: List
    audios: List
    
    def __init__(self, file: UploadFile, metadata: MetaData):
        self.filename = file.filename
        self.suffix = file.filename.split(".")[-1]
        self.content_type = file.content_type
        self.generals = [video.__dict__ for video in metadata.generals]
        self.videos = [video.__dict__ for video in metadata.videos]
        self.audios = [audio.__dict__ for audio in metadata.audios]
