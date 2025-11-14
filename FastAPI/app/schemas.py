# Pydantic Models
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
import re

# URL schemas
class URLBase(BaseModel):
    long_url: str

class URLCreate(URLBase):
    pass

class URLInfo(URLBase):
    short_code: str
    short_url: str
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True)

# User schemas
class UserBase(BaseModel):
    email: str

    @field_validator('email')
    def isValidEmail(cls, mail: str):
        # cls -> like self
        if not re.match(r'[^@]+@+(gmail.com|cvr.ac.in)', mail):
            raise ValueError('Invalid email or not supported')
        return mail

class UserCreate(UserBase):
    password: str

class UserInfo(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class UserWithLinks(UserInfo):
    urls: list[URLInfo] = []

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None