from classes.MotherClass import MotherClass
from typing import Optional
from datetime import datetime


class Session(MotherClass):
    ip_address: list
    user_agent: str
    login_time: datetime
    logout_time: Optional[datetime]
    token_expiration: datetime
