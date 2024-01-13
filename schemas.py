from pydantic import BaseModel


class PhoneSchema(BaseModel):
    """Schema for Phone"""
    phone: int
