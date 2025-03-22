class User:
    FIELD_USERNAME = "username"
    FIELD_PASSWORD = "password"
    FIELD_NAME = "name"
    FIELD_EMAIL = "email"
    FIELD_PHONE = "phone"
    FIELD_ADDRESS = "address"
    FIELD_AVATAR = "avatar"

    ALL_FIELDS = [FIELD_USERNAME, FIELD_PASSWORD, FIELD_NAME, FIELD_EMAIL, FIELD_PHONE, FIELD_ADDRESS, FIELD_AVATAR]

    def __init__(
            self,
            username: str = None,
            name: str = None,
            email: str = None,
            phone: str = None,
            address: str = None,
            avatar: str = None
    ):
        self.username = username
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.avatar = avatar

    def _dict_to_user(self, user_dict: dict = None):
        if not user_dict:
            return None
        
        for key in user_dict:
            if key not in self.ALL_FIELDS:
                raise Exception(f"Invalid user field at field: {key}")
            
        return User(
            username=user_dict.get(self.FIELD_USERNAME),
            name=user_dict.get(self.FIELD_NAME),
            email=user_dict.get(self.FIELD_EMAIL),
            phone=user_dict.get(self.FIELD_PHONE),
            address=user_dict.get(self.FIELD_ADDRESS),
            avatar=user_dict.get(self.FIELD_AVATAR)
        )
    
    def _user_to_dict(self):
        user_dict = {}
        for key in self.ALL_FIELDS:
            if hasattr(self, key):
                user_dict[key] = getattr(self, key)
        
        return user_dict