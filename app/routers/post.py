from fastapi import FastAPI, Response, APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db
from typing import List, Optional


router=APIRouter(
    prefix='/posts',
    tags=['Posts']
)

## Get all posts
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session=Depends(get_db),
              current_user:int=Depends(oauth2.get_current_user)):
    posts=db.query(models.Post).all()
    return posts

## Create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, 
                db: Session=Depends(get_db),
                current_user: int=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post) #adding to db
    db.commit()
    db.refresh(new_post) #refreshing the new post
    return new_post


## Get one post
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_post(id:int, 
             db: Session=Depends(get_db),
             current_user: int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with  id: {id} not found")

    return post


# delete post
@router.delete("/{id}", response_model=schemas.PostResponse)
def delete_post(id:int, 
                db: Session=Depends(get_db),
                current_user: int=Depends(oauth2.get_current_user)):
    
    # Retrieve the post to delete
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    # Check if post exists
    if post == None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"Post with id {id} not found")
    
    # check if user logged in is the owner of the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    # Delete the post
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


## Updating a post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, 
                updated_post: schemas.PostCreate, 
                db: Session=Depends(get_db),
                current_user: int=Depends(oauth2.get_current_user)):
    
    # Retrieve the post to update
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    # Check if post exists
    if post == None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id {id} not found")

    # check if user is the owner of the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    # Update the post
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first() 

