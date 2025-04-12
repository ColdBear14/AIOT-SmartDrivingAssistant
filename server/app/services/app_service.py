from utils.custom_logger import CustomLogger
from services.database import Database
from models.request import ActionHistoryRequest, SensorDataRequest, ServicesStatusRequest
from models.mongo_doc import ServicesStatusDocument

class AppService:
    FIELD_UID = "uid"
    FIELD_SENSOR_TYPE = "sensor_type"
    FIELD_TIMESTAMP = "timestamp"
    FIELD_VAL = "val"

    def _create_init_service_config_data(self, uid: str = None):
        init_service_config_data = {}

        init_service_config_data[ServicesStatusDocument.FIELD_UID] = uid if uid else ""

        for field in ServicesStatusDocument.ALL_SEVICE_FIELDS:
            init_service_config_data[field] = "off"

        for field in ServicesStatusDocument.ALL_VALUE_FIELDS:
            init_service_config_data[field] = 0

        return init_service_config_data

    def _get_newest_sensor_data(self, uid: str = None, sensor_type: str = None) -> dict:
        """Get the newest sensor data for a specific user and sensor type."""
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

    def _get_sensors_data(self, uid: str = None, request: SensorDataRequest = None) -> list:
        """Get the newest sensor data for multiple sensor types."""
        sensor_types = request.sensor_types

        data = []
        for sensor_type in sensor_types:
            newest_data = self._get_newest_sensor_data(uid, sensor_type)
            if newest_data:
                data.append(newest_data)

        return data
    
    def _get_services_status(self, uid: str = None):
        """Get services status from the database by user id."""
        services_status = Database()._instance.get_services_status_collection().find_one({'uid': uid})
        
        if not services_status:
            raise Exception("Service config not find")
        
        data = {}
        for key in ServicesStatusDocument.ALL_SEVICE_FIELDS:
            data[key] = services_status[key]

        for key in ServicesStatusDocument.ALL_VALUE_FIELDS:
            data[key] = services_status[key]

        return data
        
    def _get_action_history(self, request: ActionHistoryRequest = None, uid: str = None):
        service_type = request.service_type
        amt = request.amt

        action_history = Database()._instance.get_action_history_collection().find(
            {
                "uid": uid,
                "service_type": service_type
            },
            sort=[(self.FIELD_TIMESTAMP, -1)],  # Sort by timestamp in descending order
            limit=amt
        )

        data = []
        for action in action_history:
            data.append(action)

        return data