from pydantic import BaseModel


class PhoneSchema(BaseModel):
    """Schema for Phone"""
    phone: int


class SendMessageSchema(BaseModel):
    """Schema for POST /messages"""

    message_text: str
    from_phone: str
    username: str
