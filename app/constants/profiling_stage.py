from enum import StrEnum

from app.constants.questions import WellnessProfileQuestions


class ProfilingStage(StrEnum):
    INTRODUCTION = 'introduction'
    AGE = 'age'
    GENDER = 'gender'
    ACTIVITY_LEVEL = 'activity_level'
    DIETARY_PREFERENCE = 'dietary_preference'
    SLEEP_QUALITY = 'sleep_quality'
    STRESS_LEVEL = 'stress_level'
    HEALTH_GOALS = 'health_goals'


class ProfilingStageMapping:
    mapping = {
        ProfilingStage.INTRODUCTION: WellnessProfileQuestions.INTRODUCTION,
        ProfilingStage.AGE: WellnessProfileQuestions.AGE,
        ProfilingStage.GENDER: WellnessProfileQuestions.GENDER,
        ProfilingStage.ACTIVITY_LEVEL: WellnessProfileQuestions.ACTIVITY_LEVEL,
        ProfilingStage.DIETARY_PREFERENCE: WellnessProfileQuestions.DIETARY_PREFERENCE,
        ProfilingStage.SLEEP_QUALITY: WellnessProfileQuestions.SLEEP_QUALITY,
        ProfilingStage.STRESS_LEVEL: WellnessProfileQuestions.STRESS_LEVEL,
        ProfilingStage.HEALTH_GOALS: WellnessProfileQuestions.HEALTH_GOALS,
    }

    sequencing = {
        1: ProfilingStage.INTRODUCTION,
        2: ProfilingStage.AGE,
        3: ProfilingStage.GENDER,
        4: ProfilingStage.ACTIVITY_LEVEL,
        5: ProfilingStage.DIETARY_PREFERENCE,
        6: ProfilingStage.SLEEP_QUALITY,
        7: ProfilingStage.STRESS_LEVEL,
        8: ProfilingStage.HEALTH_GOALS,
    }

    @classmethod
    def get_next_stage(cls, current_stage: ProfilingStage) -> ProfilingStage | None:
        """
        Get the next profiling stage in the sequence.

        Args:
            current_stage: The current ProfilingStage

        Returns:
            The next ProfilingStage in sequence, or None if at the last stage
        """
        # Create reverse mapping to find current stage number
        reverse_sequencing = {stage: num for num, stage in cls.sequencing.items()}

        current_num = reverse_sequencing.get(current_stage)
        if current_num is None:
            return None

        next_num = current_num + 1
        return cls.sequencing.get(next_num)

    @classmethod
    def is_final_stage(cls, stage: ProfilingStage) -> bool:
        """
        Check if the given stage is the final stage in the profiling sequence.

        Args:
            stage: The ProfilingStage to check

        Returns:
            True if it's the final stage, False otherwise
        """
        return stage == ProfilingStage.HEALTH_GOALS
