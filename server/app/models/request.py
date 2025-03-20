from pydantic import BaseModel, Field
from typing import Literal
    
class UserRequest(BaseModel):
    username: str = Field(...,min_length=3,max_length=50, pattern="^[a-zA-Z0-9_]*$")
    password: str = Field(...,min_length=8,max_length=128)

class UserInfoRequest(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    
class SensorRequest(BaseModel):
    sensor_type: Literal["temp","humid","lux","dist"]
    amt: int = Field(...,ge=1)