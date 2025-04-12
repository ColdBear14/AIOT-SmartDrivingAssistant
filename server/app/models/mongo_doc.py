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

class ServicesStatusDocument():
    FIELD_UID = 'uid'

    FIELD_AIR_COND_SERVICE = 'air_cond_service'
    FIELD_HEADLIGHT_SERVICE = 'headlight_service'
    FIELD_DROWSINESS_SERVICE = 'drowsiness_service'
    FIELD_HUMID_SERVICE = 'humid_service'
    FIELD_DIST_SERVICE = 'dist_service'

    ALL_SEVICE_FIELDS = [FIELD_AIR_COND_SERVICE, FIELD_HEADLIGHT_SERVICE, FIELD_DROWSINESS_SERVICE, FIELD_HUMID_SERVICE, FIELD_DIST_SERVICE]

    FIELD_AIR_COND_TEMP = 'air_cond_temp'
    FIELD_HEADLIGHT_BRIGHTNESS = 'headlight_brightness'
    FIELD_DROWSINESS_THRESHOLD = 'drowsiness_threshold'
    FIELD_HUMID_THRESHOLD = 'humid_threshold'
    FIELD_DIST_THRESHOLD = 'dist_threshold'

    ALL_VALUE_FIELDS = [FIELD_AIR_COND_TEMP, FIELD_HEADLIGHT_BRIGHTNESS, FIELD_DROWSINESS_THRESHOLD, FIELD_HUMID_THRESHOLD, FIELD_DIST_THRESHOLD]