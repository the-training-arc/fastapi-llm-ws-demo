from enum import StrEnum


class Gender(StrEnum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'


class ActivityLevel(StrEnum):
    SEDENTARY = 'sedentary'
    MODERATE = 'moderate'
    ACTIVE = 'active'


class DietaryPreference(StrEnum):
    VEGETARIAN = 'vegetarian'
    VEGAN = 'vegan'
    KETO = 'keto'
    PALEO = 'paleo'
    OMNIVORE = 'omnivore'
    NO_PREFERENCE = 'no_preference'


class SleepQuality(StrEnum):
    GOOD = 'good'
    AVERAGE = 'average'
    POOR = 'poor'


class StressLevel(StrEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class Confidence(StrEnum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'
