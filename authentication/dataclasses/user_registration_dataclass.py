from dataclasses import dataclass
from typing import Optional
@dataclass
class UserRegistrationEmailDataClass():
    # Base user model
    email: str
    password: str

    # User information model
    nama: str
    foto: Optional[str]
    nomor_telepon: str
    role: str
    is_admin: bool