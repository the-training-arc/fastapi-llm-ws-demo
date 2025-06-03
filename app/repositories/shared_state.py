from typing import Dict, List

from app.constants.profiling_stage import ProfilingStage
from app.models.wellness_profile import WellnessProfile, WellnessProfileConfidence

session_messages: Dict[str, List[dict]] = {}
session_status: Dict[str, ProfilingStage] = {}
session_wellness_profiles: Dict[str, WellnessProfile] = {}
session_wellness_confidence: Dict[str, WellnessProfileConfidence] = {}
session_assistant_replies: Dict[str, int] = {}
session_has_pending_generation: Dict[str, bool] = {}


def get_connection_manager():
    """Get the singleton ConnectionManager instance"""
    from app.usecases.session_manager_usecase import ConnectionManager

    return ConnectionManager(session_messages)
