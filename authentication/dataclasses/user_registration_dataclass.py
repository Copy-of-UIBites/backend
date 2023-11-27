from pydantic import BaseModel
from typing import Optional

class UserRegistrationEmailDataClass(BaseModel):
    # Base user model
    email: str
    password: str

    # User information model
    nama: str
    foto: Optional[str]
    nomor_telepon: str
    role: str
    is_admin: bool