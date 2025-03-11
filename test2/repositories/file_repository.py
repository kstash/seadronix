from bson import ObjectId
from database import slice_video_collection
from schemas.info import Info


class FileRepository:
    def create_slice_video(self, info: Info, slice_index: int, sliced_video_content: bytes):
        slice_video_id = slice_video_collection.put(
            sliced_video_content, 
            info_id=info.id,
            slice_index=slice_index, 
            filename=info.filename
        )
        return slice_video_id

    def get_slice_videos(self, info_id: str):
        sorted_slice_videos = slice_video_collection.find({"info_id": ObjectId(info_id)}).sort("slice_index", 1)
        return sorted_slice_videos
    
    def get_slice_video(self, info_id: str, slice_index: int):
        slice_video = slice_video_collection.find_one({"info_id": ObjectId(info_id), "slice_index": slice_index})
        return slice_video

    def get_slice_videos_by_index_range(self, info_id: str, start_index: int, end_index: int):
        slice_videos = slice_video_collection.find({
            "info_id": ObjectId(info_id), 
            "slice_index": { "$gte": start_index, "$lte": end_index }
        }).sort("slice_index", 1)
        return slice_videos