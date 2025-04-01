from enum import Enum
from pydantic import BaseModel, Field
from typing import Literal, Optional
    
class UserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]*$")
    password: str = Field(..., min_length=8, max_length=128)

class UserInfoRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]*$")
    email: Optional[str] = Field(None, email=True)
    phone: Optional[str] = Field(None, min_length=10, max_length=10, pattern="^[0-9]*$")
    address: Optional[str] = Field(None, min_length=3, max_length=100)
    date_of_birth: Optional[str] = Field(None, pattern="^\d{2}-\d{2}-\d{4}$")


class ServiceMode(str, Enum):
    AUTO = "auto"
    MANUAL = "manual"
    OFF = "off"

class UserConfigRequest(BaseModel):
    temp_service: Optional[ServiceMode] = None
    humid_service: Optional[ServiceMode] = None
    lux_service: Optional[ServiceMode] = None
    dist_service: Optional[ServiceMode] = None
    
class SensorRequest(BaseModel):
    sensor_type: Literal["temp","humid","lux","dist"]
    amt: int = Field(...,ge=1, le=100)