from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.constants.wellness_profile import (
    ActivityLevel,
    Confidence,
    DietaryPreference,
    Gender,
    SleepQuality,
    StressLevel,
)


class WellnessProfile(BaseModel):
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


class WellnessProfileConfidence(BaseModel):
    """
    Wellness profile confidence model
    """

    age: Confidence = Field(default=Confidence.LOW, description='Confidence of the age')
    gender: Confidence = Field(default=Confidence.LOW, description='Confidence of the gender')
    activityLevel: Confidence = Field(
        default=Confidence.LOW, description='Confidence of the activity level'
    )
    dietaryPreference: Confidence = Field(
        default=Confidence.LOW, description='Confidence of the dietary preference'
    )
    sleepQuality: Confidence = Field(
        default=Confidence.LOW, description='Confidence of the sleep quality'
    )
    stressLevel: Confidence = Field(
        default=Confidence.LOW, description='Confidence of the stress level'
    )
    healthGoals: Confidence = Field(
        default=Confidence.LOW, description='Confidence of the health goals'
    )


class WellnessProfileResponse(BaseModel):
    """
    Wellness profile measured model
    """

    model_config = ConfigDict(use_enum_values=True, extra='forbid')

    wellnessProfile: WellnessProfile = Field(
        default=None, description='Wellness profile of the user'
    )
    confidence: WellnessProfileConfidence = Field(
        default=None, description='Confidence of the wellness profile'
    )
    followUpQuestion: Optional[Annotated[str, StringConstraints(min_length=1, max_length=1000)]] = (
        Field(default=None, description='Follow up question to the user')
    )
