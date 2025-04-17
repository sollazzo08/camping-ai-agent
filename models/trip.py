from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

class Trip(BaseModel):
    location: str = Field(..., description="The location of the camping trip")
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")
    start_date: Optional[date] = Field(default=None, description="Start date of the trip")
    end_date: Optional[date] = Field(default=None, description="End date of the trip")
    group_size: Optional[int] = Field(default=1, description="Number of people going")
    activities: List[str] = Field(default_factory=list, description="Planned activities")
    include_weather: bool = Field(default=False, description="Whether to use weather data")
