from bson import ObjectId

from services.database import Database

from models.request import UserConfigRequest, UserInfoRequest
from models.mongo_doc import UserDocument, UserConfigDocument

class UserService:
    def _get_object_id(self, uid: str = None) -> ObjectId:
        '''
            Convert a user id string into an ObjectId for querying the database.
        '''
        try:
            return ObjectId(uid)
        except Exception as e:
            raise Exception("Invalid string to ObjectId conversion") from e
        
    def _create_init_user_data(self, username: str = None, hashed_password: str = None) -> tuple[dict, dict]:
        '''
            Create 2 dict for initial user's data and user config data for register operation.
        '''
        init_data = {}
        for field in UserDocument.ALL_BASIC_FIELDS:
            init_data[field] = ""

        init_data[UserDocument.FIELD_USERNAME] = username
        init_data[UserDocument.FILED_PASSWORD] = hashed_password
        init_data[UserDocument.FIELD_AVATAR] = ""

        init_config_data = {}
        for field in UserConfigDocument.ALL_SEVICE_FIELDS:
            init_config_data[field] = False

        return (init_data, init_config_data)

    def _get_user_info(self, uid: str = None) -> dict:
        '''
            Get user info from the database by user id string.

            Args:
                uid: The user id string.

            Returns:
                A dictionary containing the user's basic info.
        '''
        user = Database()._instance.get_user_collection().find_one({'_id': self._get_object_id(uid)})

        if not user:
            raise Exception("User not find")

        data = {}
        for key in UserDocument.ALL_BASIC_FIELDS:
            if key in user:
                data[key] = user[key]

        return data
    
    def _update_user_info(self, uid: str = None, user_info_request: UserInfoRequest = None):
        '''
            Update user info in the database by user id string and UserInfoRequest object.
        '''
        update_data = user_info_request.dict(exclude_unset=True)
        
        if update_data == {}:
            raise Exception("No data to update")
        
        print(f"update_data: {update_data}")
        
        result = Database()._instance.get_user_collection().update_one(
            {'_id': self._get_object_id(uid)},
            {'$set': update_data}
        )
        if result.modified_count == 0:
            raise Exception("No user info updated")

    def _get_user_info_by_session_id(self, session_id: str = None):
        '''
            Get user info from the database by current user's session, included '_id' field.
        '''
        if not session_id:
            return None
        
        user = Database()._instance.get_user_collection().find_one({'session_id': session_id})
        return user

    def _delete_user_account(self, uid: str = None):
        '''
            Delete all user info from the database by user id string. 
        '''
        session = Database()._instance.client.start_session()
        try:
            with session.start_transaction():
                Database()._instance.get_user_collection().delete_one({'_id': self._get_object_id(uid)}, session=session)
                Database()._instance.get_user_config_collection().delete_one({'uid': uid}, session=session)
                # Database()._instance.get_env_sensor_collection().delete_many({'uid': uid})
        except Exception as e:
            session.abort_transaction()
            raise Exception("Delete user account failed")
        finally:
            session.end_session()

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
        
        if not user_config:
            raise Exception("User config not find")
        
        data = {}
        for key in UserConfigDocument.ALL_SEVICE_FIELDS:
            data[key] = user_config[key]

        return data

    def _update_user_config(self, uid: str = None, user_config_request: UserConfigRequest = None):
        '''
            Update user config in the database by user id string and UserConfigRequest object.
        '''
        update_data = user_config_request.dict(exclude_unset=True)

        if update_data == {}:
            raise Exception("No data to update")
        
        result = Database()._instance.get_user_config_collection().update_one(
            {'uid': uid},
            {'$set': update_data}
        )
        if result.modified_count == 0:
            raise Exception("No user config updated")