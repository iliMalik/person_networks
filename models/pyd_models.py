from datetime import datetime, timezone
from enum import Enum


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

class PersonCreate(BaseModel, ConfigMixin):
    person_age: PositiveInt = Field(..., description="Age")
    person_first_name: str = Field(..., max_length=100, description="First name of person")
    person_last_name: str = Field(...,max_length=100,  description="Last name of person")
    person_gender: Gender = Field(..., description="Gender of person")

class Person(PersonCreate):
    person_id: UUID = Field(default_factory=uuid4, description="person_id of the person taking session")

class QuestionCreate(ConfigMixin, BaseModel):
    question_text: str = Field(..., description="Question text")

class Question(QuestionCreate):
    question_id: UUID = Field(default_factory=uuid4, description="Unique question ID")

class SectionCreate(ConfigMixin,BaseModel):
    section_text: str = Field(..., max_length=100, description="Section text")

class Section(SectionCreate):
     section_id: UUID = Field(default_factory=uuid4, description="Unique section ID")

class SessionCreate(ConfigMixin,BaseModel):
    person_id: UUID = Field(..., description="Unique user ID")

class Session(SessionCreate):
    session_id: UUID = Field(default_factory=uuid4, description="Unique session ID")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp"
    )

