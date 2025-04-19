import os

from bson import ObjectId
from passlib.context import CryptContext
import secrets

from pymongo.errors import PyMongoError
from services.app_service import AppService
from services.database import Database

from services.user_service import UserService

from models.request import UserRequest
from models.mongo_doc import UserDocument

from datetime import datetime, timedelta
# import redis

# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class AuthService:
    __pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

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
    
    def _register(self, user_request: UserRequest = None) -> dict:
        '''
        Register a new user in the database.

        Args:
            user_request: An instance of UserRequest containing the username and password.

        Returns:
            A dictionary containing the document IDs of the newly created user and user configuration.

        Raises:
            Exception: If the username already exists.
            PyMongoError: If there is an error during the database transaction.
        '''

        if Database()._instance.get_user_collection().find_one({UserDocument.FIELD_USERNAME: user_request.username}):
            raise Exception("Username already exists")
        
        hashed_pw = self._hash_pw(user_request.password)
        
        init_user_data = UserService()._create_init_user_data(user_request.username, hashed_pw)

        session = Database()._instance.client.start_session()
        try:
            with session.start_transaction():
                user_result = Database()._instance.get_user_collection().insert_one(
                    init_user_data,
                    session=session
                )
                
                init_service_config_data = AppService()._create_init_services_status_data(str(user_result.inserted_id))

                service_config_result = Database()._instance.get_services_status_collection().insert_one(
                    init_service_config_data,
                    session=session
                )
            
            return {
                "user_doc_id": str(user_result.inserted_id),
                "service_config_doc_id": str(service_config_result.inserted_id)
            }

        except PyMongoError as e:
            session.abort_transaction()
            raise e
    
    def _authenticate(self, user_request: UserRequest = None) -> tuple[str, str]:
        '''
        Authenticate a user using the provided UserRequest object.

        Args:
            user_request: An instance of UserRequest containing the username and password.

        Returns:
            A tuple containing the session id and user id as strings.

        Raises:
            Exception: If the credentials are invalid or if the user_request object is not provided.
        '''

        user = Database()._instance.get_user_collection().find_one({UserDocument.FIELD_USERNAME: user_request.username})
        if not (user and self._verify_pw(user[UserDocument.FIELD_PASSWORD], user_request.password)):
            raise Exception("Invalid credentials")
        
        session_id = self._create_session(user['_id'])
        return (session_id, str(user['_id']))
    
    def _create_session(self, uid: ObjectId = None) -> str:
        '''
        Create a new session for the given user id.

        Args:
            uid: The ObjectId of the user.

        Returns:
            The session id as a string.

        Raises:
            Exception: If the user id is not provided or if the session creation fails.
        '''
        if not uid:
            raise Exception("User ID is required")
        
        session_id = secrets.token_hex(32)
        expiration_time = datetime.now() + timedelta(hours=1)

    # Store session in Redis
        # redis_client.hmset(session_id, {
        #     'user_id': uid,
        #     'expiration_time': expiration_time.isoformat()
        # })
        # redis_client.expire(session_id, 3600)

        result = Database()._instance.get_user_collection().update_one(
            {'_id': uid},
            {'$set': {
                UserDocument.FIELD_SESSION: session_id,
                'session_expiration': expiration_time
            }}
        )
        if result.modified_count == 0:
            raise Exception("Session creation failed: User not found")
        
        return session_id
    
    def _del_session(self, session_id: str = None) -> bool:
        '''
        Delete a session for the given session id.

        Args:
            session_id: The session id as a string.

        Returns:
            True if the session is deleted successfully, False otherwise.

        Raises:
            Exception: If the session id is not provided or if the session does not exist.
        '''
        result = Database()._instance.get_user_collection().update_one(
            {UserDocument.FIELD_SESSION: session_id},
            {'$unset': {
                UserDocument.FIELD_SESSION: '',
                'session_expiration': ''
            }}
        )
        return result.modified_count > 0
    
    def _add_cookie_session(self, response, session_id: str = None) -> dict:
        '''
        Add a session id cookie to the given response.

        Args:
            response: The Response object to add the cookie to.
            session_id: The session id as a string.

        Returns:
            The Response object with the added cookie.
        '''
        secure_mode: bool
        if os.getenv("SECURE") == "False":
            secure_mode = False
        else:
            secure_mode = True

        samesite_mode: str = os.getenv("SAME_SITE")

        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=secure_mode, # False to test api with postman
            samesite=samesite_mode,
            path="/",
            max_age=3600
        )
        return response
    
    def _del_cookie_session(self, response) -> dict:
        '''
        Del the session id in cookie of the request.

        Args:
            response: The Response object to delete session in cookie.

        Returns:
            The Response object with the delete cookie option.
        '''
        secure_mode: bool
        if os.getenv("SECURE") == "False":
            secure_mode = False
        else:
            secure_mode = True

        samesite_mode: str = os.getenv("SAME_SITE")

        response.delete_cookie(
            key="session_id",
            httponly=True,
            secure=secure_mode, # False to test api with postman
            samesite=samesite_mode,
            path="/"
        )
        return response