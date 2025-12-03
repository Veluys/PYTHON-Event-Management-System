from dataclasses import dataclass

@dataclass
class Registration:
    event_id: int
    sr_code: str
    venue_id: str
    attended: str