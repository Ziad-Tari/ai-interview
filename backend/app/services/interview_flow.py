from app.models.session import InterviewSession, InterviewStage


class InterviewFlow:
    """
    Controls how an interview evolves.
    """

    STAGE_ORDER = [
        InterviewStage.WARMUP,
        InterviewStage.TECHNICAL,
        InterviewStage.DEEP_DIVE,
        InterviewStage.BEHAVIORAL,
        InterviewStage.SUMMARY,
    ]

    # -----------------------------
    # NEXT STAGE DECISION
    # -----------------------------
    def should_advance_stage(self, session: InterviewSession, score: float) -> bool:
        if score >= 4.0:
            return True
        return False

    # -----------------------------
    # GET NEXT STAGE
    # -----------------------------
    def next_stage(self, session: InterviewSession) -> InterviewStage:
        current_index = self.STAGE_ORDER.index(session.current_stage)

        if current_index < len(self.STAGE_ORDER) - 1:
            return self.STAGE_ORDER[current_index + 1]

        return InterviewStage.SUMMARY

    # -----------------------------
    # ADAPT DIFFICULTY LOGIC
    # -----------------------------
    def adjust_difficulty(self, score: float) -> str:
        if score >= 4.5:
            return "hard"
        elif score >= 3.0:
            return "medium"
        return "easy"