"""Coach: Agentic orchestrator that runs the full learning assessment and recommendation pipeline."""

from app.models import CoachingResult
from app.skill_analyzer import analyze_skills
from app.gap_identifier import identify_gaps
from app.learning_recommender import recommend_learning_path
from app.llm_client import call_llm


MOTIVATION_SYSTEM_PROMPT = """You are a warm, encouraging learning mentor. Based on the learner's current situation and learning plan, provide a short motivational message.

The message should:
- Be 3-4 sentences
- Acknowledge where they are now
- Highlight that the gaps are achievable
- Encourage them to start with the first step
- Be genuine and specific to their situation (not generic)

Return ONLY the motivational message text, nothing else."""


def coach_learner(profile_text: str, target_role_text: str) -> CoachingResult:
    """Run the full coaching pipeline for a learner.

    This is the main agentic workflow that orchestrates:
    1. Analyzing current skills
    2. Identifying skill gaps
    3. Recommending a learning path
    4. Generating a motivational message
    """
    # Step 1: Analyze current skills
    skill_profile = analyze_skills(profile_text, target_role_text)

    # Step 2: Identify gaps
    gap_report = identify_gaps(profile_text, target_role_text)

    # Step 3: Build gap summary for the recommender
    gaps_summary = _build_gaps_summary(gap_report)

    # Step 4: Recommend learning path
    learning_plan = recommend_learning_path(profile_text, target_role_text, gaps_summary)

    # Step 5: Generate motivational message
    motivational_message = _get_motivation(skill_profile, gap_report, learning_plan)

    # Extract learner info
    learner_name = skill_profile.summary.split(",")[0] if skill_profile.summary else "Learner"

    return CoachingResult(
        learner_name=learner_name,
        current_role="",
        target_role="",
        skill_profile=skill_profile,
        gap_report=gap_report,
        learning_plan=learning_plan,
        motivational_message=motivational_message,
    )


def _build_gaps_summary(gap_report) -> str:
    """Build a text summary of gaps for the learning recommender."""
    lines = []

    if gap_report.critical_gaps:
        lines.append("CRITICAL GAPS (must learn):")
        for g in gap_report.critical_gaps:
            lines.append(f"  - {g.skill_name}: {g.current_level} → {g.required_level} — {g.description}")

    if gap_report.important_gaps:
        lines.append("\nIMPORTANT GAPS (should learn):")
        for g in gap_report.important_gaps:
            lines.append(f"  - {g.skill_name}: {g.current_level} → {g.required_level} — {g.description}")

    if gap_report.nice_to_have_gaps:
        lines.append("\nNICE-TO-HAVE GAPS (bonus):")
        for g in gap_report.nice_to_have_gaps:
            lines.append(f"  - {g.skill_name}: {g.current_level} → {g.required_level} — {g.description}")

    if gap_report.experience_gaps:
        lines.append("\nEXPERIENCE GAPS:")
        for eg in gap_report.experience_gaps:
            lines.append(f"  - {eg}")

    return "\n".join(lines) if lines else "No significant gaps identified."


def _get_motivation(skill_profile, gap_report, learning_plan) -> str:
    """Generate a motivational message from the LLM."""
    user_prompt = f"""## Learner's Current State
Readiness for target role: {skill_profile.overall_readiness}%
Strongest skills: {', '.join(skill_profile.strongest_skills) or 'None identified'}
Summary: {skill_profile.summary}

## Gaps Found
Total gaps: {gap_report.total_gaps}
Critical gaps: {len(gap_report.critical_gaps)}
Gap summary: {gap_report.gap_summary}

## Learning Plan
{learning_plan.plan_summary}
Quick wins to start: {', '.join(learning_plan.quick_wins[:3]) if learning_plan.quick_wins else 'See learning plan'}

Write a personalized motivational message for this learner."""

    return call_llm(MOTIVATION_SYSTEM_PROMPT, user_prompt)
