from dataclasses import dataclass
from typing import Optional

@dataclass
class Registration:
    event_id: int
    sr_code: str
    attended: Optional[str] = None