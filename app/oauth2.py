from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


# tokenurl will be our endpoint
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY="hello"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# create access token fnx
def create_access_token(data: dict):
    to_encode=data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
    


# This function decodes the JWT token to verify its authenticity and validity. 
# If the token is valid, it extracts the user_id from the payload.
def verify_access_token(token: str, credentials_exception):

    try:
        payload=jwt.decode(token, SECRET_KEY, ALGORITHM)

        # to extract the data
        id: str=payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=str(id)) #validate that it matches our token schema #convert id to a string

    except JWTError:
        raise credentials_exception
    
    return token_data
    


# This function uses the JWT token to fetch the current user from the database.
# once the verify access token returns the token(id), get current user fnx fetches the user from the db

def get_current_user(token: str =Depends(oauth2_scheme),
                     db: Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"Could not validate credentials",
                                        headers={"WWW-Authenticate": "Bearer"})
    
    token=verify_access_token(token, credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    
    return user






