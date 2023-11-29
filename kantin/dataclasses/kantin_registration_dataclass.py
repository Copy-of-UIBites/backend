from dataclasses import dataclass
from typing import Optional, List

@dataclass
class KantinRegistrationDataClass():
    nama: str
    lokasi: str
    deskripsi: str
    list_foto: Optional[List[str]] = None
    status_verifikasi: str = 'Pending'
