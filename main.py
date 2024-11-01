# main.py
from fastapi import FastAPI, HTTPException, status, Depends
from bson import ObjectId
from schemas import BlogPost, BlogPostUpdate
from models import MongoDBHandler

app = FastAPI()

# MongoDB configuration
db_handler = MongoDBHandler("mongodb://localhost:27017", "school_blog_db")

# Dependency to inject the database handler
def get_db_handler():
    return db_handler

@app.get("/posts", response_model=list[BlogPost])
async def get_all_posts(db_handler=Depends(get_db_handler)):
    return await db_handler.get_all_posts()

@app.get("/posts/{post_id}", response_model=BlogPost)
async def get_post(post_id: str, db_handler=Depends(get_db_handler)):
    post = await db_handler.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/posts", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_post(post: BlogPost, db_handler=Depends(get_db_handler)):
    return await db_handler.create_post(post)

@app.put("/posts/{post_id}", response_model=int)
async def update_post(post_id: str, post_data: BlogPostUpdate, db_handler=Depends(get_db_handler)):
    result = await db_handler.update_post(post_id, post_data)
    if result == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return result

@app.delete("/posts/{post_id}", response_model=int)
async def delete_post(post_id: str, db_handler=Depends(get_db_handler)):
    result = await db_handler.delete_post(post_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return result
