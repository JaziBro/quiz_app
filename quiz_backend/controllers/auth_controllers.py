from datetime import timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext   
from quiz_backend.settings import algorithm, secretKey
from typing import TypedDict, Union, Any
from datetime import timedelta

TokenType = TypedDict(
    "TokenType",
    {
        "user_name": str, 
        "user_email": str,
        "access_expiry_time": timedelta,
        "refresh_expiry_time": timedelta
    }
)

pwd_context = CryptContext(schemes="bcrypt")

def generateToken(data: dict, expiry_time: timedelta):
    try:
        encoded_data = data.copy()
        encoded_data.update({
            "exp": expiry_time
        })
        token = jwt.encode(
            encoded_data, secretKey, algorithm=algorithm)
        return token
    except JWTError as e:
       raise e
        
def decodeToken(token: str):
    try:
        decodedData = jwt.decode(token, secretKey, algorithms=algorithm)
        return decodedData
    except JWTError as e:
        raise e


def generateHashedPassword(plaintext: str):
   hashedPassword = pwd_context.hash(plaintext)    
   return hashedPassword


# verifies if hashedpassword present in db is same as the one provided by user
def verifyPassword(hashPass: str, plaintext: str):
    verify_password = pwd_context.verify(plaintext, hash=hashPass)
    return verify_password 

    
def generateAccesAndRefreshToken(userDetais: dict[str, Any]):
    data = {
        "user_name": userDetais["user_name"],
        "user_email": userDetais["user_email"]
    }
    accessToken = generateToken(data, userDetais["access_expiry_time"].total_seconds())
    refreshToken = generateToken(data, userDetais["refresh_expiry_time"].total_seconds())
    accessExpiryTime = userDetais["access_expiry_time"]
    refreshExpiryTime = userDetais["refresh_expiry_time"]

    return {
        "accessToken": {
            "token": accessToken, 
            "access_expiry_time": accessExpiryTime
        },
        "refreshToken": {
            "token": refreshToken, 
            "RefreshTokenExpiryTime": refreshExpiryTime
    }
    }


def tokenService():
    ...

