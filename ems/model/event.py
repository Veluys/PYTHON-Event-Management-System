from dataclasses import dataclass
from datetime import date, time
from typing import Optional

@dataclass
class Event:
    event_name: str
    event_date: date
    start_time: time
    end_time: time
    venue_id: int
    event_id: Optional[int] = -1