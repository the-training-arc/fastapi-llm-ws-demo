from app.constants.wellness_profile import (
    ActivityLevel,
    DietaryPreference,
    Gender,
    SleepQuality,
    StressLevel,
)


def _create_enum_question(question: str, enum_class) -> str:
    """Helper function to create a question with enum options."""
    return f'{question}\n' '        Please select one of the following options:\n' + '\n'.join(
        f'        - {option.value}' for option in enum_class
    )


class WellnessProfileQuestions:
    INTRODUCTION = """
        Hello! I'm your digital wellness assistant, here to help you build a personalized health profile.

        To get started, could you please share the following details about yourself:
        - Your age
        - Your gender
        - How many hours you typically sleep each night
        - Your current activity level (e.g., sedentary, lightly active, very active)
        - Any specific dietary preferences or restrictions
        - Your main health goal at the moment (e.g., lose weight, reduce stress, build muscle)

        You can include as much information as you'd like in your reply. This will help me tailor my follow-up questions and support to you. Thank you!
    """

    AGE = """
        What is your age?
    """

    GENDER = _create_enum_question('What is your gender?', Gender)
    ACTIVITY_LEVEL = _create_enum_question('What is your activity level?', ActivityLevel)
    DIETARY_PREFERENCE = _create_enum_question(
        'What is your dietary preference?', DietaryPreference
    )
    SLEEP_QUALITY = _create_enum_question('What is your sleep quality?', SleepQuality)
    STRESS_LEVEL = _create_enum_question('What is your stress level?', StressLevel)
    HEALTH_GOALS = """
        What are your health goals?
    """
