class UserDocument():
    FIELD_USERNAME = 'username'
    FIELD_PASSWORD = 'password'
    FIELD_SESSION = 'session_id'

    FIELD_NAME = 'name'
    FIELD_EMAIL = 'email'
    FIELD_PHONE = 'phone'
    FIELD_ADDRESS = 'address'
    FIELD_DOB = 'date_of_birth'
    FIELD_AVATAR = 'avatar'
    ALL_BASIC_FIELDS = [FIELD_NAME, FIELD_EMAIL, FIELD_PHONE, FIELD_ADDRESS, FIELD_DOB]

class UserConfigDocument():
    FIELD_UID = 'uid'
    FIELD_TEMP_SERVICE = 'temp_service'
    FIELD_HUMID_SERVICE = 'humid_service'
    FIELD_LUX_SERVICE = 'lux_service'
    FIELD_DIST_SERVICE = 'dist_service'
    ALL_SEVICE_FIELDS = [FIELD_TEMP_SERVICE, FIELD_HUMID_SERVICE, FIELD_LUX_SERVICE, FIELD_DIST_SERVICE]