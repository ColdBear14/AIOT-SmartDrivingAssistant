from services.database import Database
from models.request import SensorRequest

class SensorService:
    FIELD_UID = "uid"
    FIELD_SENSOR_TYPE = "sensor_type"

    def _get_sensor_data(self, uid: str = None, request: SensorRequest = None):
        sensor_type = request.sensor_type
        amt = request.amt

        data = Database()._instance.get_sensor_collection().find(
            {
                self.FIELD_UID: uid,
                self.FIELD_SENSOR_TYPE: sensor_type
            }, 
            limit=amt,
            sort=[('timestamp', -1)]
        )
        return data
    
    def _get_all_sensors_data(self, uid: str = None):
        data = Database()._instance.get_sensor_collection().find({self.FIELD_UID: uid})
        return data
