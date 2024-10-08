import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase): # creating/updating post
    pass

class PostResponse(PostBase): # response model
    id:int
    created_at:datetime.datetime
    owner_id: int
    
    class Config:
        from_attributes = True



class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime.datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    





