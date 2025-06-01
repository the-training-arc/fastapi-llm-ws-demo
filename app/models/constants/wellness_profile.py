from enum import Enum


class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'


class ActivityLevel(Enum):
    SEDENTARY = 'sedentary'
    MODERATE = 'moderate'
    ACTIVE = 'active'


class DietaryPreference(Enum):
    VEGETARIAN = 'vegetarian'
    VEGAN = 'vegan'
    KETO = 'keto'
    PALEO = 'paleo'
    OMNIVORE = 'omnivore'
    NO_PREFERENCE = 'no_preference'


class SleepQuality(Enum):
    GOOD = 'good'
    AVERAGE = 'average'
    POOR = 'poor'


class StressLevel(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
