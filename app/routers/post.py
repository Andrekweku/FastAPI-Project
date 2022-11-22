from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, Oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(Oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute("""SELECT * FROM public."Posts" """)
    # posts = cursor.fetchall()

    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )  # .all() to return all the results
    # To get only posts for a specific logged in user USE ->
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(Oauth2.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO "Posts" (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # title=post.title, content=post.content, published=post.published

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Just like RETURNING in SQL
    return new_post

    # post_dict = post.dict()
    # post_dict["id"] = randrange(0, 1000000)
    # my_posts.append(post_dict)


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(Oauth2.get_current_user),
):  # , response: Response

    # cursor.execute(""" SELECT * FROM public."Posts" WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found.",
        )

    # if post.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to perform requested action",
    #     ) # Checking if the logged in user owns this post

    return post


# in if statement..
# response.status_code = status.HTTP_404_NOT_FOUND
# return {"Message": f"Post with id: {id} was not found."}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(Oauth2.get_current_user),
):
    # cursor.execute(
    #     """ DELETE FROM public."Posts" WHERE id = %s RETURNING * """, (str(id),)
    # )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(
        models.Post.id == id
    )  # Were defining the query here

    post = post_query.first()  # Then we find the particular post here

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist.",
        )  # And here we're checking to see if the post is not there

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )  # Checking if the logged in user owns this post

    post_query.delete(
        synchronize_session=False
    )  # We grab the query from above and delete it
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(Oauth2.get_current_user),
):
    # index = find_index_post(id)
    # cursor.execute(
    #     """ UPDATE public."Posts" SET title= %s, content= %s, published=%s WHERE id = %s RETURNING * """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist.",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
