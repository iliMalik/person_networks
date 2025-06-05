from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional, List

from pydantic import BaseModel, PositiveInt, Field, ConfigDict
from uuid import UUID, uuid4


# Mixin for shared config (DO NOT inherit BaseModel here)
class ConfigMixin:
    model_config = ConfigDict(
        str_max_length=500,
        str_min_length=2,
        str_strip_whitespace=True,
        from_attributes=True
    )


class Gender(Enum):
    male = "male"
    female = "female"
    other = "other"


class PersonCreate(BaseModel):
    person_name:  str = Field(..., max_length=100, description="person title text")
    person_phone: Optional[List[str]] = Field(
        default=None,
        description="Optional list of phone numbers"
    )

class Person(PersonCreate):
    person_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the person")

class OrganizationCreate(BaseModel):
    organization_name: str = Field(..., max_length=100, description="Name of the organization")

class Organization(OrganizationCreate):
    organization_id: UUID = Field(default_factory=uuid4, description="UUID of the organization")

class CountryCreate(BaseModel):
    country_name: str = Field(..., max_length=100, description="Name of the country")

class Country(CountryCreate):
    country_id: UUID = Field(default_factory=uuid4, description="UUID of the country")