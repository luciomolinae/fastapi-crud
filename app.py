from fastapi import FastAPI, HTTPException
# pydantic es una bibliteca que nos permite darle forma a los datos
from pydantic import BaseModel # describimos un schema inicial
from typing import Text, Optional # importa el tipo de dato
from datetime import datetime
from uuid import uuid4 as uuid


app = FastAPI()

posts = [] # arrays de posts --- sin db

# Post Model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False


@app.get('/')
def read_root():
    return{"welcome":"Bienvenido a mi API"}

@app.get('/posts') # cuando pidan atraves de la app la ruta get / quiero que utilices la siguiente funcion
def get_post(): # esto returna el array de posts
    return posts

@app.post('/posts')
def save_post(post: Post): # voy a estar recibiendo un post y tiene el schema Post
    post.id = str(uuid())
    posts.append(post.dict()) # .dict lo convierte a dicciorio y .append lo guarda en posts
    return posts[-1] # comienza el retorn con el final

@app.get('/posts/{post_id}') # te lee el post
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail = 'post no encontrado')

@app.delete("/posts/{post_id}") # te elimina el post
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index) # pop elimina el id que coincida
            return{"message": "Post Eliminado!"}
    raise HTTPException(status_code=404, detail = 'post no encontrado')


@app.put("/posts/{post_id}")
def update_post(post_id: str, updatePost: Post): # te actualiza el post
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]['title'] = updatePost.title # reemplazamos la propiedad title con el post.title
            posts[index]['content'] = updatePost.content # si encontraste la propiedad content entonces actualizalo
            posts[index]['author'] = updatePost.author
            return{"message": "Post Actualizao!"}
    raise HTTPException(status_code=404, detail = 'post no encontrado')