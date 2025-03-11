from fastapi import HTTPException
from dtos import CreateInfo
from schemas import Info
from database import info_collection
from bson import ObjectId


class InfoRepository:
    def __init__(self):
        self.collection = info_collection

    async def create_info(self, dto: CreateInfo) -> Info:
        result = self.collection.insert_one(dto.__dict__)
        info = self.get_info_by_id(result.inserted_id)
        return info

    def get_info_by_id(self, info_id: str) -> Info:
        doc = self.collection.find_one({"_id": ObjectId(info_id)})
        if not doc:
            raise HTTPException(status_code=404, detail=f"info_id: {info_id} not found")
        info = Info.model_validate(doc)
        return info
