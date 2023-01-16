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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(Oauth2.get_current_user),
):
    
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # title=post.title, content=post.content, published=post.published

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Just like RETURNING in SQL
    return new_post

 

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

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(Oauth2.get_current_user),
):
  
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
