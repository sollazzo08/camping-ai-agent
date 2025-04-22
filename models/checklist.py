from typing import List
from pydantic import BaseModel, Field

class Checklist(BaseModel):
    Shelter: List[str] = Field(..., description="Items related to shelter, such as tents and sleeping bags")
    Clothing: List[str] = Field(..., description="Clothing items appropriate for the weather and trip duration")
    Cooking: List[str] = Field(..., description="Items needed for cooking, eating, and food preparation")
    Hygiene: List[str] = Field(..., description="Personal hygiene items like toothbrushes, soap, etc.")
    Safety: List[str] = Field(..., description="Safety and emergency gear like first aid kits, flashlights, etc.")
    Miscellaneous: List[str] = Field(..., description="Other items that don't fit into the main categories")
