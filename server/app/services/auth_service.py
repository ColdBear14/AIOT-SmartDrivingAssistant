# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from utils.custom_logger import CustomLogger

from bson import ObjectId
from passlib.context import CryptContext
import secrets

from services.database import Database
from models.request import UserRequest

import redis
from datetime import datetime, timedelta

# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class AuthService:
    __pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    
    FIELD_USERNAME = 'username'
    FIELD_PASSWORD = 'password'
    FIELD_SESSION = 'session_id'

    # def __init__(self, username:str, password:str):
    #     self.username = username
    #     self.password = password
        
    def _hash_pw(self, password: str = None) -> str:
        if not password:
            return None
        else:
            return AuthService.__pwd_context.hash(password)
    
    def _verify_pw(self, hashed_pw: str = None, password:str = None) -> bool:
        if not hashed_pw or not password:
            return False
        else:
            return AuthService.__pwd_context.verify(password, hashed_pw)
    
    def _register(self, user_request: UserRequest = None) -> str:
        '''
        Save new user to database. Return the inserted document's id.
        Exception is raised if the username already exists or if the user_request object is not provided.
        '''
        if Database()._instance.get_user_collection().find_one({AuthService.FIELD_USERNAME: user_request.username}):
            raise Exception("Username already exists")
        
        hashed_pw = self._hash_pw(user_request.password)
        result = Database()._instance.get_user_collection().insert_one({
            AuthService.FIELD_USERNAME: user_request.username,
            AuthService.FIELD_PASSWORD: hashed_pw
        })

        return result.inserted_id
    
    def _authenticate(self, user_request: UserRequest = None) -> tuple[str, str]:
        '''
        Authenticate user.
        Parameters: user_request (UserRequest object with username and password)
        Return the session id.
        Exception is raised if the credentials are invalid or if the user_request object is not provided.
        '''
        user = Database()._instance.get_user_collection().find_one({AuthService.FIELD_USERNAME: user_request.username})
        if not (user and self._verify_pw(user[AuthService.FIELD_PASSWORD], user_request.password)):
            raise Exception("Invalid credentials")
        
        session_id = AuthService()._create_session(user['_id'])
        return (session_id, str(user['_id']))
    
    def _create_session(self, uid: ObjectId = None) -> str:
        '''
        Create a new session for the user.
        Parameters: uid (ObjectId of user id)
        Return the session id.

        Exception is raised if the user id is not provided or if the session creation fails for any reason.

        Optional: store the session id in Redis.
        '''
        if not uid:
            raise Exception("User ID is required")
        
        session_id = secrets.token_hex(32)
        expiration_time = datetime.now() + timedelta(hours=1)

        # redis_client.hmset(session_id, {
        #     'user_id': uid,
        #     'expiration_time': expiration_time.isoformat()
        # })
        # redis_client.expire(session_id, 3600)

        result = Database()._instance.get_user_collection().update_one(
            {'_id': uid},
            {'$set': {
                AuthService.FIELD_SESSION: session_id,
                'session_expiration': expiration_time
            }}
        )
        if result.modified_count == 0:
            raise Exception("Session creation failed: User not found")
        
        return session_id
    
    def _del_session(self, session_id: str = None) -> bool:
        '''
        Delete the session from the database. Return True if the session is deleted successfully.
        '''
        result = Database()._instance.get_user_collection().update_one(
            {AuthService.FIELD_SESSION: session_id},
            {'$unset': {
                AuthService.FIELD_SESSION: '',
                'session_expiration': ''
            }}
        )
        return result.modified_count > 0
    
    def _add_cookie(self, response, session_id: str = None) -> dict:
        '''
        Create a cookie with the session id and attach it to the response object.
        '''
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=False,
            samesite="None",
            path="/",
            max_age=3600
        )
        return response