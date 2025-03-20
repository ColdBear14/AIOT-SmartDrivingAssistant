from services.database import Database
from models.request import UserInfoRequest

class UserService:
    FEILD_NAME = 'name'
    FEILD_EMAIL = 'email'
    FEILD_PHONE = 'phone'
    FEILD_ADDRESS = 'address'

    def _get_user_info(self, uid: str = None):
        user = Database()._instance.get_user_collection().find_one({'_id': uid})
        return user
    
    def _update_user_info(self, uid: str = None, user_info_request: UserInfoRequest = None):
        update_data = {}
        if user_info_request.name:
            update_data[UserService.FEILD_NAME] = user_info_request.name
        if user_info_request.email:
            update_data[UserService.FEILD_EMAIL] = user_info_request.email
        if user_info_request.phone:
            update_data[UserService.FEILD_PHONE] = user_info_request.phone
        if user_info_request.address:
            update_data[UserService.FEILD_ADDRESS] = user_info_request.address
        
        if update_data:
            Database()._instance.get_user_collection().update_one(
                {'_id': uid},
                {'$set': update_data}
            )

    def _get_user_info_by_session_id(self, session_id: str = None):
        user = Database()._instance.get_user_collection().find_one({'session_id': session_id})
        return user
