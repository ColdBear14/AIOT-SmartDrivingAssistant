from services.database import Database
from models.request import SensorRequest

class IOTService:
    FIELD_METADATA = "metadata"
    FIELD_UID = "metadata.uid"
    FIELD_SENSOR_TYPE = "metadata.sensor_type"
    FIELD_TIMESTAMP = "timestamp"
    FIELD_VAL = "val"

    def _get_sensor_data(self, uid: str = None, request: SensorRequest = None):
        """
        Fetch sensor data for a specific user and sensor type, limited by the amount requested.
        """
        sensor_type = request.sensor_type
        amt = request.amt

        # Query updated to access nested fields in 'metadata'
        data = Database()._instance.get_sensor_collection().find(
            {
                self.FIELD_UID: uid,
                self.FIELD_SENSOR_TYPE: sensor_type
            },
            limit=amt,
            sort=[(self.FIELD_TIMESTAMP, -1)]  # Sort by timestamp in descending order
        )
        return list(data)  # Convert cursor to list for easier handling

    def _get_all_sensors_data(self, uid: str = None):
        """
        Fetch all sensor data for a specific user.
        """
        # Query updated to access nested 'uid' field in 'metadata'
        data = Database()._instance.get_sensor_collection().find(
            {self.FIELD_UID: uid}
        )
        return list(data)  # Convert cursor to list for easier handling