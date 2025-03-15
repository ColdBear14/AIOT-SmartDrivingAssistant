from dataclasses import dataclass, field

AIO_USER_NAME = "NopeHy14"
AIO_KEY = "aio_GiIc74cdAMPt214e6umJWC5MHNnS"
@dataclass
class Config:
    mongo_url: str = "mongodb://localhost:27017"
    aio_user: str = AIO_USER_NAME
    aio_key: str = AIO_KEY
    aio_url: str = field(init=False)
    db_name: str = 'va_database'
    def __post_init__(self):
        self.aio_url = f'https://io.adafruit.com/{self.aio_user}/feeds/'
    
config = Config()   