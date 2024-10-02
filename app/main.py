from fastapi import FastAPI, APIRouter, HTTPException, status
from app import models
from app.database import engine
from app.routers import post, user, auth


# Creates tables within postgresql
models.Base.metadata.create_all(bind=engine)


app=FastAPI()


# Calling the router objects
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


