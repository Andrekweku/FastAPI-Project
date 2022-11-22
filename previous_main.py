from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import time

import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


while True:

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="19hrs - Tutorial",
            user="postgres",
            password="GOOGLE4LYF",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print("Connecting to Database failed")
        print("Error: ", error)
        time.sleep(2)

# my_posts = [
#     {"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "favorite foods", "content": "I love Pizza", "id": 2},
# ]


@app.get("/")
async def root():
    return {"message": "Hello World !"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM public."Posts" """)
    posts = cursor.fetchall()
    return {"data": posts}


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i


@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO "Posts" (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}
    # post_dict = post.dict()
    # post_dict["id"] = randrange(0, 1000000)
    # my_posts.append(post_dict)


@app.get("/posts/{id}")
def get_post(id: int):  # , response: Response

    cursor.execute(""" SELECT * FROM public."Posts" WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found.",
        )
    return {"post_detail": post}


# in if statement..
# response.status_code = status.HTTP_404_NOT_FOUND
# return {"Message": f"Post with id: {id} was not found."}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """ DELETE FROM public."Posts" WHERE id = %s RETURNING * """, (str(id),)
    )
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # index = find_index_post(id)
    cursor.execute(
        """ UPDATE public."Posts" SET title= %s, content= %s, published=%s WHERE id = %s RETURNING * """,
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist.",
        )

    return {"message": updated_post}
