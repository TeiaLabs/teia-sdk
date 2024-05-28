from typing import Literal, Optional

from pydantic import BaseModel, EmailStr


class Creator(BaseModel):
    client_name: str
    token_name: str
    user_email: EmailStr
    user_ip: str = "127.0.0.1"


class Connection(BaseModel):
    name: str
    type: Literal["milvus", "atlas"]
    uri: str
    secret: Optional[str] = None
    service_name: str
    entity_name: str
    created_by: Creator
