from pydantic import BaseModel, Field,field_validator
from typing import Optional
from datetime import datetime


class UserLoginSchema(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")



class UserRegisterSchema(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    confirm_password: str = Field(..., description="Confirm Password")


    @field_validator("confirm_password")
    def check_passwords_match(cls, confirm_password, validation):
        if confirm_password != validation.data.get("password"):
            raise ValueError("Passwords do not match")
        return confirm_password
