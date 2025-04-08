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
    date_of_birth: Optional[str] = Field(None, pattern="^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-[0-9]{4}$")
    
class SensorDataRequest(BaseModel):
    sensor_types: list[Literal["temp", "humid", "lux", "dist"]] = Field(..., min_items=1, max_items=4)

class ServiceMode(str, Enum):
    AUTO = "auto"
    MANUAL = "manual"
    ON = "on"
    OFF = "off"

class ServiceConfigRequest(BaseModel):
    air_cond_service: Optional[ServiceMode] = None
    drowsiness_service: Optional[ServiceMode] = None
    headlight_service: Optional[ServiceMode] = None
    dist_service: Optional[ServiceMode] = None
    humid_service: Optional[ServiceMode] = None

class ControlServiceRequest(BaseModel):
    air_cond_temp: Optional[int] = None
    headlight_brightness: Optional[int] = None
    drowsiness_threshold: Optional[int] = None
    dist_threshold: Optional[int] = None
    humid_threshold: Optional[int] = None