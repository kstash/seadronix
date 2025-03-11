from typing import List
from pydantic import BaseModel, model_validator
from pymediainfo import MediaInfo, Track


class GeneralData(BaseModel):
    internet_media_type: str
    file_extension: str
    duration: int
    file_size: int

    @classmethod
    def to_cls(cls, general_track: Track):
        data = {
            "internet_media_type": str(getattr(general_track, "internet_media_type", None)),
            "file_extension": str(getattr(general_track, "file_extension", None)),
            "duration": int(getattr(general_track, "duration", 0)),
            "file_size": int(getattr(general_track, "file_size", 0))
        }
        return cls.model_validate(data)
    
    @model_validator(mode="after")
    def validate_general(self):
        if self.internet_media_type == None:
            raise ValueError("파일 미디어 타입 오류")
        if self.file_extension == None:
            raise ValueError("파일 확장자 오류")
        if self.duration <= 0:
            raise ValueError("파일 길이 오류")
        if self.file_size <= 0:
            raise ValueError("파일 크기 오류")
        return self


class VideoData(BaseModel):
    internet_media_type: str
    width: int
    height: int
    frame_rate: float
    duration: int

    @classmethod
    def to_cls(cls, video_track: Track):
        data = {
            "internet_media_type": getattr(video_track, "internet_media_type", None),
            "duration": int(getattr(video_track, "duration", 0)),
            "frame_rate": float(getattr(video_track, "frame_rate", 0)),
            "width": int(getattr(video_track, "width", 0)),
            "height": int(getattr(video_track, "height", 0))
        }
        return cls.model_validate(data)

    @model_validator(mode="after")
    def validate_general(self):
        if self.internet_media_type == None:
            raise ValueError("파일 영상 미디어 타입 오류")
        if self.duration <= 0:
            raise ValueError("파일 영상 길이 오류")
        return self


class AudioData(BaseModel):
    format: str
    duration: int

    @classmethod
    def to_cls(cls, audio_track: Track):
        data = {
            "format": str(getattr(audio_track, "format", None)),
            "duration": int(getattr(audio_track, "duration", 0)),
        }
        return cls.model_validate(data)

    @model_validator(mode="after")
    def validate_general(self):
        if self.format == None:
            raise ValueError("파일 오디오 포맷 오류")
        if self.duration <= 0:
            raise ValueError("파일 오디오 길이 오류")
        return self


class MetaData(BaseModel):
    generals: List[GeneralData]
    videos: List[VideoData]
    audios: List[AudioData]

    @classmethod
    def to_cls(cls, media_info: MediaInfo):
        general_track_list = [GeneralData.to_cls(g) for g in media_info.general_tracks] if media_info.general_tracks else []
        video_track_list = [VideoData.to_cls(v) for v in media_info.video_tracks] if media_info.video_tracks else []
        audio_track_list = [AudioData.to_cls(a) for a in media_info.audio_tracks] if media_info.audio_tracks else []

        metadata_dict = {
            "generals": general_track_list,
            "videos": video_track_list,
            "audios": audio_track_list
        }

        return cls.model_validate(metadata_dict)