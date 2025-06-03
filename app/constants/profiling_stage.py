from enum import StrEnum


class ProfilingStage(StrEnum):
    INIT = 'init'
    PROFILING = 'profiling'
    COMPLETED = 'completed'


class ProfilingStageMapping:
    sequencing = {
        1: ProfilingStage.INIT,
        2: ProfilingStage.PROFILING,
        3: ProfilingStage.COMPLETED,
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
