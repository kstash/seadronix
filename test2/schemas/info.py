from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field

from schemas.custom import PyObjectId
from schemas.metadata import AudioData, GeneralData, VideoData


class Info(BaseModel):
    id: PyObjectId = Field(alias='_id')
    filename: str
    suffix: str
    content_type: str
    generals: List[GeneralData]
    videos: List[VideoData]
    audios: List[AudioData]
    upload_date: datetime = Field(default=datetime.now())

    model_config: dict = ConfigDict(
        extra='allow', 
        arbitrary_types_allowed=True
    )

    @classmethod
    def model_validate(cls, data):
        return cls(**data)

    @classmethod
    def to_cls(cls, data):
        return cls.model_validate(data)