from services.database import Database
from models.request import SensorRequest
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from iotsystem.services.iot import IOTSystem

class IOTService:
    FIELD_UID = "uid"
    FIELD_SENSOR_TYPE = "sensor_type"
    FIELD_TIMESTAMP = "timestamp"
    FIELD_VAL = "val"

    def _get_sensor_data(self, uid: str = None, request: SensorRequest = None):
        """
        Fetch sensor data for a specific user and sensor type, limited by the amount requested.
        """
        sensor_type = request.sensor_type
        amt = request.amt

        # Query updated to access nested fields in 'metadata'
        data = Database()._instance.get_env_sensor_collection().find(
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
        data = Database()._instance.get_env_sensor_collection().find(
            {self.FIELD_UID: uid},
            sort=[(self.FIELD_TIMESTAMP, -1)],
            limit=20
        )
        data = list(data)
        for doc in data:
            doc["_id"] = str(doc["_id"])

        return list(data)  # Convert cursor to list for easier handling
    
    def _send_slider_data(self, uid: str = None, value: str = None):
        """
        Send slider data to iotsystem.
        """        
        try:
            # Send slider data to IOTSystem
            IOTSystem().recieveData(uid, value)
        except Exception as e:
            return None

