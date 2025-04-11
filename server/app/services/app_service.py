from services.database import Database
from models.request import SensorDataRequest, ServiceConfigRequest
from models.mongo_doc import ServiceConfigDocument

class AppService:
    FIELD_UID = "uid"
    FIELD_SENSOR_TYPE = "sensor_type"
    FIELD_TIMESTAMP = "timestamp"
    FIELD_VAL = "val"

    def _create_init_service_config_data(self, uid: str = None):
        init_service_config_data = {}

        init_service_config_data[ServiceConfigDocument.FIELD_UID] = uid if uid else ""

        for field in ServiceConfigDocument.ALL_SEVICE_FIELDS:
            init_service_config_data[field] = "off"

        for field in ServiceConfigDocument.ALL_VALUE_FIELDS:
            init_service_config_data[field] = 0

        return init_service_config_data

    def _get_newest_sensor_data(self, uid: str = None, sensor_type: str = None) -> dict:
        """
        Get the newest sensor data for a specific user and sensor type.
        """
        data = Database()._instance.get_env_sensor_collection().find_one(
            {
                self.FIELD_UID: uid,
                self.FIELD_SENSOR_TYPE: sensor_type
            },
            sort=[(self.FIELD_TIMESTAMP, -1)]  # Sort by timestamp in descending order
        )

        if data and data['_id']:
            data['_id'] = str(data['_id'])

        return data

    def _get_sensor_data(self, uid: str = None, request: SensorDataRequest = None) -> list:
        """
        Get the newest sensor data for a specific user and multiple sensor types.
        """
        sensor_types = request.sensor_types

        data = []
        for sensor_type in sensor_types:
            newest_data = self._get_newest_sensor_data(uid, sensor_type)
            if newest_data:
                data.append(newest_data)

        return data
    
    def _get_service_config(self, uid: str = None):
        '''
            Get user config from the database by user id string.
        '''
        user_config = Database()._instance.get_service_config_collection().find_one({'uid': uid})
        
        if not user_config:
            raise Exception("Service config not find")
        
        data = {}
        for key in ServiceConfigDocument.ALL_SEVICE_FIELDS:
            data[key] = user_config[key]

        for key in ServiceConfigDocument.ALL_VALUE_FIELDS:
            data[key] = user_config[key]

        return data

    def _update_service_config(self, uid: str = None, user_config_request: ServiceConfigRequest = None):
        '''
            Update user config in the database by user id string and UserConfigRequest object.
        '''
        update_data = user_config_request.dict(exclude_unset=True)

        if update_data == {}:
            raise Exception("No data to update")
        
        result = Database()._instance.get_service_config_collection().update_one(
            {'uid': uid},
            {'$set': update_data}
        )
        if result.modified_count == 0:
            raise Exception("No service config updated")
        
    def _get_history(self, uid: str = None):
        pass