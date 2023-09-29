from pydantic import BaseModel

class CollegePreferences(BaseModel):
    field_of_study: str
    location_preference: str
    # Add other fields as needed
