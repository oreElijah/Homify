from pydantic import BaseModel

class PriceInputData(BaseModel):
    bedrooms: int
    bathrooms: int
    toilets: int
    parking_space: int
    title: str
    town: str
    state: str