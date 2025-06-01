from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.models.constants.wellness_profile import (
    ActivityLevel,
    DietaryPreference,
    Gender,
    SleepQuality,
    StressLevel,
)


class WellnessProfileIn(BaseModel):
    """
    Wellness profile input model
    """

    model_config = ConfigDict(use_enum_values=True, extra='forbid')

    age: Optional[Annotated[int, Field(ge=1, le=100)]] = Field(
        default=None, description='Age of the user'
    )
    gender: Optional[Gender] = Field(default=None, description='Gender of the user')
    activityLevel: Optional[ActivityLevel] = Field(
        default=None, description='Activity level of the user'
    )
    dietaryPreference: Optional[DietaryPreference] = Field(
        default=None, description='Dietary preference of the user'
    )
    sleepQuality: Optional[SleepQuality] = Field(
        default=None, description='Sleep quality of the user'
    )
    stressLevel: Optional[StressLevel] = Field(default=None, description='Stress level of the user')
    healthGoals: Optional[Annotated[str, StringConstraints(min_length=1, max_length=100)]] = Field(
        default=None, description='Health goals of the user'
    )
