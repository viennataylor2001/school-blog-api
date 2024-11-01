# models.py
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Union
from schemas import BlogPost, BlogPostUpdate

class MongoDBHandler:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db['blog_posts']

    async def get_all_posts(self) -> List[dict]:
        return await self.collection.find().to_list(100)

    async def get_post(self, post_id: str) -> Union[dict, None]:
        return await self.collection.find_one({"_id": ObjectId(post_id)})

    async def create_post(self, post: BlogPost) -> str:
        result = await self.collection.insert_one(post.dict(by_alias=True))
        return str(result.inserted_id)

    async def update_post(self, post_id: str, post_data: BlogPostUpdate) -> Union[int, None]:
        result = await self.collection.update_one(
            {"_id": ObjectId(post_id)}, {"$set": post_data.dict(exclude_unset=True)}
        )
        return result.modified_count

    async def delete_post(self, post_id: str) -> int:
        result = await self.collection.delete_one({"_id": ObjectId(post_id)})
        return result.deleted_count
