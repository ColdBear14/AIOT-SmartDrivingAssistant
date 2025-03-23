from bson import ObjectId

from services.database import Database
from models.request import UserInfoRequest

class UserService:
    FEILD_NAME = 'name'
    FEILD_EMAIL = 'email'
    FEILD_PHONE = 'phone'
    FEILD_ADDRESS = 'address'
    ALL_FIELDS = [FEILD_NAME, FEILD_EMAIL, FEILD_PHONE, FEILD_ADDRESS]

    def _get_object_id(self, uid: str = None) -> ObjectId:
        '''
            Convert a user id string into an ObjectId for querying the database.
        '''
        try:
            return ObjectId(uid)
        except Exception as e:
            raise ValueError("Invalid string to ObjectId conversion") from e

    def _get_user_info(self, uid: str = None) -> dict:
        '''
            Get user info from the database by user id string but without the ObjectId "_id" field.
        '''
        user = Database()._instance.get_user_collection().find_one({'_id': self._get_object_id(uid)})
        if (user and '_id' in user):
            user.pop('_id', None)
        return user
    
    def _update_user_info(self, uid: str = None, user_info_request: UserInfoRequest = None):
        '''
            Update user info in the database by user id string and UserInfoRequest object.
        '''
        update_data = {}
        if user_info_request.name:
            update_data[UserService.FEILD_NAME] = user_info_request.name
        if user_info_request.email:
            update_data[UserService.FEILD_EMAIL] = user_info_request.email
        if user_info_request.phone:
            update_data[UserService.FEILD_PHONE] = user_info_request.phone
        if user_info_request.address:
            update_data[UserService.FEILD_ADDRESS] = user_info_request.address
        
        if update_data == {}:
            raise ValueError("No valid fields to update")
        
        result = Database()._instance.get_user_collection().update_one(
            {'_id': self._get_object_id(uid)},
            {'$set': update_data}
        )
        if result.modified_count == 0:
            raise ValueError("No user info updated")

    def _get_user_info_by_session_id(self, session_id: str = None):
        '''
            Get user info from the database by current user's session, included '_id' field.
        '''
        user = Database()._instance.get_user_collection().find_one({'session_id': session_id})
        return user

    def _delete_user_info(self, uid: str = None):
        '''
            Delete all user info from the database by user id string. 
        '''
        Database()._instance.get_user_collection().delete_one({'_id': self._get_object_id(uid)})
        Database()._instance.get_sensor_collection().delete_many({'uid': uid})

    def _update_avatar(self, uid: str = None, avatar: any = None):
        '''
            Update user avatar in the database by user id string and avatar file.
        '''
        pass

    def _get_avatar(self, uid: str = None):
        '''
            Get user avatar from the database by user id string.
        '''
        pass

    def _delete_avatar(self, uid: str = None):
        '''
            Delete user avatar from the database by user id string.
        '''
        pass
