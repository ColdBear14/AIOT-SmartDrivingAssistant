from pydantic import BaseModel, Field
from typing import Literal
    
class UserRequest(BaseModel):
    username: str
    password: str
    
class SensorRequest(BaseModel):
    sensor_type: Literal["temp","humid","lux","dist"]
    amt: int = Field(...,ge=1)