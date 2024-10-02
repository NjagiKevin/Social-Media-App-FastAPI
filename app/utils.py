from passlib.context import CryptContext



# hashing algorithm we should use
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)



# comparing the two passwords
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

