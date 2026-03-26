"""Skill Analyzer: assesses a learner's current skill levels against a target role."""

from app.llm_client import call_llm_json
from app.models import SkillProfile, SkillAssessment, ProficiencyLevel

SKILL_ANALYSIS_SYSTEM_PROMPT = """You are an expert career coach and skill assessor. Your job is to analyze a learner's current skills based on their profile and assess their proficiency against what a target role requires.

Return a JSON object with these exact keys:
{
  "assessed_skills": [
    {
      "skill_name": "Python",
      "current_level": "beginner" | "intermediate" | "advanced" | "expert",
      "required_level": "beginner" | "intermediate" | "advanced" | "expert",
      "confidence": <0-100>
    }
  ],
  "strongest_skills": ["skill1", "skill2", "skill3"],
  "weakest_skills": ["skill1", "skill2"],
  "overall_readiness": <0-100>,
  "summary": "A 2-3 sentence summary of the learner's readiness for the target role"
}

Guidelines:
- assessed_skills: Evaluate ALL skills mentioned in the target role (required + preferred). For each, estimate the learner's current level based on their profile.
- current_level: Infer from experience, projects, certifications mentioned. "beginner" if no evidence, "intermediate" if mentioned but limited context, "advanced" if clearly demonstrated, "expert" if deep expertise shown.
- required_level: What the target role typically demands for this skill.
- confidence: How confident you are in the assessment (higher if clear evidence in profile).
- strongest_skills: Top 3-5 skills where the learner is closest to or exceeds the required level.
- weakest_skills: Skills with the largest gap between current and required level.
- overall_readiness: 0-100 percentage of how ready the learner is for the target role.

Be encouraging but honest. Base assessment on evidence from the profile."""


def analyze_skills(profile_text: str, target_role_text: str) -> SkillProfile:
    """Analyze a learner's skills against a target role."""
    user_prompt = f"""## Learner Profile
{profile_text}

## Target Role / Career Goal
{target_role_text}

Assess this learner's current skills against the target role requirements. Return JSON only."""

    result = call_llm_json(SKILL_ANALYSIS_SYSTEM_PROMPT, user_prompt)

    level_map = {
        "beginner": ProficiencyLevel.BEGINNER,
        "intermediate": ProficiencyLevel.INTERMEDIATE,
        "advanced": ProficiencyLevel.ADVANCED,
        "expert": ProficiencyLevel.EXPERT,
    }

    assessments = []
    for item in result.get("assessed_skills", []):
        assessments.append(SkillAssessment(
            skill_name=item.get("skill_name", ""),
            current_level=level_map.get(item.get("current_level", "beginner"), ProficiencyLevel.BEGINNER),
            required_level=level_map.get(item.get("required_level", "intermediate"), ProficiencyLevel.INTERMEDIATE),
            confidence=item.get("confidence", 50),
        ))

    return SkillProfile(
        assessed_skills=assessments,
        strongest_skills=result.get("strongest_skills", []),
        weakest_skills=result.get("weakest_skills", []),
        overall_readiness=result.get("overall_readiness", 0),
        summary=result.get("summary", ""),
    )
