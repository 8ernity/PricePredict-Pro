from pydantic import BaseModel

class PropertyData(BaseModel):
    area: float
    bedrooms: int
    floor: int
    parking: float
    facing: str
    city_tier: str
    property_type: str
    is_new_construction: bool
    age: int
    furnishing: str
    bathrooms: int
    balconies: int
    city_preset: str
    has_pool: bool
    has_gym: bool
    has_security: bool
    has_backup: bool
