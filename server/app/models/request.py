from pydantic import BaseModel, Field
from typing import Literal
    
class UserRequest(BaseModel):
    username: str = Field(...,min_length=3,max_length=50, pattern="^[a-zA-Z0-9_]*$")
    password: str = Field(...,min_length=8,max_length=128)

class UserInfoRequest(BaseModel):
    name: str
    email: str = Field(..., email=True)
    phone: str = Field(...,min_length=10,max_length=10, pattern="^[0-9]*$")
    address: str = Field(...,max_length=100)
    
class SensorRequest(BaseModel):
    sensor_type: Literal["temp","humid","lux","dist"]
    amt: int = Field(...,ge=1, le=100)