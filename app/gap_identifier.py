"""Gap Identifier: finds skill gaps between current profile and target role."""

from app.llm_client import call_llm_json
from app.models import GapReport, SkillGap, GapPriority

GAP_IDENTIFICATION_SYSTEM_PROMPT = """You are an expert career development analyst. Your job is to identify all skill gaps between a learner's current profile and their target role.

Return a JSON object with these exact keys:
{
  "critical_gaps": [
    {
      "skill_name": "Skill Name",
      "current_level": "beginner",
      "required_level": "advanced",
      "priority": "critical",
      "description": "Why this gap matters and impact on role readiness"
    }
  ],
  "important_gaps": [
    {
      "skill_name": "Skill Name",
      "current_level": "beginner",
      "required_level": "intermediate",
      "priority": "important",
      "description": "Why this gap should be addressed"
    }
  ],
  "nice_to_have_gaps": [
    {
      "skill_name": "Skill Name",
      "current_level": "beginner",
      "required_level": "intermediate",
      "priority": "nice_to_have",
      "description": "Would help but not essential"
    }
  ],
  "experience_gaps": ["Description of experience gap 1"],
  "gap_summary": "2-3 sentence overview of the learner's gap situation"
}

Guidelines:
- critical_gaps: Core skills required for the role where the learner has little or no proficiency. These MUST be learned first.
- important_gaps: Skills that are needed but the learner has some foundation. Should be prioritized after critical gaps.
- nice_to_have_gaps: Preferred/bonus skills that would make the candidate stronger but aren't blockers.
- experience_gaps: Hands-on experience the learner lacks (e.g., "No production deployment experience").
- Be specific about the gap and why it matters for the role.
- Order gaps by importance within each category."""


def identify_gaps(profile_text: str, target_role_text: str) -> GapReport:
    """Identify skill gaps between learner profile and target role."""
    user_prompt = f"""## Learner Profile
{profile_text}

## Target Role / Career Goal
{target_role_text}

Identify all skill gaps and prioritize them. Return JSON only."""

    result = call_llm_json(GAP_IDENTIFICATION_SYSTEM_PROMPT, user_prompt)

    priority_map = {
        "critical": GapPriority.CRITICAL,
        "important": GapPriority.IMPORTANT,
        "nice_to_have": GapPriority.NICE_TO_HAVE,
    }

    def parse_gaps(items: list, default_priority: str) -> list[SkillGap]:
        gaps = []
        for item in items:
            gaps.append(SkillGap(
                skill_name=item.get("skill_name", ""),
                current_level=item.get("current_level", "beginner"),
                required_level=item.get("required_level", "intermediate"),
                priority=priority_map.get(item.get("priority", default_priority), GapPriority.IMPORTANT),
                description=item.get("description", ""),
            ))
        return gaps

    critical = parse_gaps(result.get("critical_gaps", []), "critical")
    important = parse_gaps(result.get("important_gaps", []), "important")
    nice_to_have = parse_gaps(result.get("nice_to_have_gaps", []), "nice_to_have")

    return GapReport(
        critical_gaps=critical,
        important_gaps=important,
        nice_to_have_gaps=nice_to_have,
        experience_gaps=result.get("experience_gaps", []),
        total_gaps=len(critical) + len(important) + len(nice_to_have),
        gap_summary=result.get("gap_summary", ""),
    )
