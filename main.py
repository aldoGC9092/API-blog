from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional


app = FastAPI()

# Modelo de datos para una publicación del blog
class BlogPost(BaseModel):
    id: int
    title: str
    content: str
    author: str
    published: Optional[bool] = True

# Base de datos en memoria (solo para este ejemplo)
blog_posts = []


@app.get("/")
async def root():
    return {"message": "Para probar el API ingresa a /docs y para ver publicaciones ingresa a /posts"}

# Endpoint para obtener todas las publicaciones
@app.get("/posts", response_model=List[BlogPost])
def get_posts():
    return blog_posts

# Endpoint para obtener una publicación específica por su ID
@app.get("/posts/{post_id}", response_model=BlogPost)
def get_post(post_id: int):
    for post in blog_posts:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

# Endpoint para crear una nueva publicación
@app.post("/posts", response_model=BlogPost)
def create_post(post: BlogPost):
    # Verificamos que el ID no esté duplicado
    for existing_post in blog_posts:
        if existing_post.id == post.id:
            raise HTTPException(status_code=400, detail="Post with this ID already exists")
    blog_posts.append(post)
    return post

# Endpoint para actualizar una publicación existente
@app.put("/posts/{post_id}", response_model=BlogPost)
def update_post(post_id: int, updated_post: BlogPost):
    for index, post in enumerate(blog_posts):
        if post.id == post_id:
            blog_posts[index] = updated_post
            return updated_post
    raise HTTPException(status_code=404, detail="Post not found")

# Endpoint para eliminar una publicación
@app.delete("/posts/{post_id}", response_model=BlogPost)
def delete_post(post_id: int):
    for index, post in enumerate(blog_posts):
        if post.id == post_id:
            deleted_post = blog_posts.pop(index)
            return deleted_post
    raise HTTPException(status_code=404, detail="Post not found")
