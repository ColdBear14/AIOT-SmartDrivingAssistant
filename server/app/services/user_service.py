from bson import ObjectId

from services.database import Database

from models.request import UserConfigRequest, UserInfoRequest

class UserService:
    FIELD_USERNAME = 'username'
    FILED_PASSWORD = 'password'

    FIELD_NAME = 'name'
    FIELD_EMAIL = 'email'
    FIELD_PHONE = 'phone'
    FIELD_ADDRESS = 'address'
    FIELD_AVATAR = 'avatar'
    ALL_TEXT_FIELDS = [FIELD_NAME, FIELD_EMAIL, FIELD_PHONE, FIELD_ADDRESS]

    FILED_UID = 'uid'
    FIELD_TEMP_SERVICE = 'temp_service'
    FIELD_HUMID_SERVICE = 'humid_service'
    FIELD_LUX_SERVICE = 'lux_service'
    FIELD_DIST_SERVICE = 'dist_service'
    ALL_BOOL_FIELDS = [FIELD_TEMP_SERVICE, FIELD_HUMID_SERVICE, FIELD_LUX_SERVICE, FIELD_DIST_SERVICE]

    def _get_object_id(self, uid: str = None) -> ObjectId:
        '''
            Convert a user id string into an ObjectId for querying the database.
        '''
        try:
            return ObjectId(uid)
        except Exception as e:
            raise ValueError("Invalid string to ObjectId conversion") from e
        
    def _create_init_user_data(self, username: str = None, hashed_password: str = None) -> tuple[dict, dict]:
        '''
            Create 2 dict for initial user's data and user config data for register operation.
        '''
        init_data = {}
        for field in self.ALL_TEXT_FIELDS:
            init_data[field] = ""

        init_data[self.FIELD_USERNAME] = username
        init_data[self.FILED_PASSWORD] = hashed_password
        init_data[self.FIELD_AVATAR] = ""

        init_config_data = {}
        for field in self.ALL_BOOL_FIELDS:
            init_config_data[field] = False

        return (init_data, init_config_data)

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
            update_data[UserService.FIELD_NAME] = user_info_request.name
        if user_info_request.email:
            update_data[UserService.FIELD_EMAIL] = user_info_request.email
        if user_info_request.phone:
            update_data[UserService.FIELD_PHONE] = user_info_request.phone
        if user_info_request.address:
            update_data[UserService.FIELD_ADDRESS] = user_info_request.address
        
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
        Database()._instance.get_env_sensor_collection().delete_many({'uid': uid})

    def _get_avatar(self, uid: str = None):
        '''
            Get user avatar from the database by user id string.
        '''
        pass

    def _update_avatar(self, uid: str = None, avatar: any = None):
        '''
            Update user avatar in the database by user id string and avatar file.
        '''
        pass

    def _delete_avatar(self, uid: str = None):
        '''
            Delete user avatar from the database by user id string.
        '''
        pass

    def _get_user_config(self, uid: str = None):
        '''
            Get user config from the database by user id string.
        '''
        user_config = Database()._instance.get_user_config_collection().find_one({'uid': uid})
        if (user_config and '_id' in user_config):
            user_config.pop('_id', None)
        return user_config

    def _update_user_config(self, uid: str = None, user_config_request: UserConfigRequest = None):
        '''
            Update user config in the database by user id string and UserConfigRequest object.
        '''
        update_data = {}
        if user_config_request.temp_service is not None:
            update_data[self.FIELD_TEMP_SERVICE] = user_config_request.temp_service
        if user_config_request.humid_service is not None:
            update_data[self.FIELD_HUMID_SERVICE] = user_config_request.humid_service
        if user_config_request.lux_service is not None:
            update_data[self.FIELD_LUX_SERVICE] = user_config_request.lux_service
        if user_config_request.dist_service is not None:
            update_data[self.FIELD_DIST_SERVICE] = user_config_request.dist_service

        if update_data == {}:
            raise ValueError("No valid fields to update")
        
        result = Database()._instance.get_user_config_collection().update_one(
            {'uid': uid},
            {'$set': update_data}
        )
        if result.modified_count != 0:
            return result.upserted_id
        
        update_data['uid'] = uid
        result = Database()._instance.get_user_config_collection().insert_one(
            update_data
        )

        return result.inserted_id