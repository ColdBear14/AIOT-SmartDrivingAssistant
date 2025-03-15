from passlib.context import CryptContext
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import secrets


class User:
    __pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
    
    FIELD_USERNAME = 'username'
    FIELD_PASSWORD = 'password'
    FIELD_SESSION = 'session_id'
    def __init__(self,username:str,password:str):
        self.username = username
        self.password = password
        
    def _hash_pw(self) -> str:
        return User.__pwd_context.hash(self.password)
    
    def _verify_pw(self,hashed_pw:str) -> bool:
        return User.__pwd_context.verify(self.password,hashed_pw)
    
    def save(self,user_collection):
        if user_collection.find_one({User.FIELD_USERNAME: self.username}):
            raise HTTPException(status_code=400,detail="Username already exists")
        
        hashed_pw = self._hash_pw()
        user_collection.insert_one({
            User.FIELD_USERNAME: self.username,
            User.FIELD_PASSWORD: hashed_pw
        })
        return {'message': 'User registered successful'}
    
    def authenticate(self,user_collection):
        user = user_collection.find_one({User.FIELD_USERNAME: self.username})
        if not (user and self._verify_pw(user[User.FIELD_PASSWORD])):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        session_id = secrets.token_hex(32)
        user_collection.update_one(
            {User.FIELD_USERNAME: self.username},
            {'$set': {User.FIELD_SESSION: session_id}}
        )
        return session_id
    
class UserRequest(BaseModel):
    username: str
    password: str
    
class SensorRequest(BaseModel):
    sensor_type: Literal["temp","humid","lux","dist"]
    amt: int = Field(...,ge=1)