"""Learning Recommender: suggests courses, certifications, and learning paths."""

from app.llm_client import call_llm_json
from app.models import LearningPlan, LearningPath, LearningResource, ResourceType

LEARNING_PATH_SYSTEM_PROMPT = """You are an expert learning advisor and career mentor. Your job is to create a personalized, step-by-step learning plan for a learner based on their skill gaps and target role.

Return a JSON object with these exact keys:
{
  "learning_paths": [
    {
      "phase": "Phase 1",
      "phase_title": "Foundation Building",
      "description": "What this phase covers and why",
      "resources": [
        {
          "title": "Course or Resource Name",
          "resource_type": "course" | "certification" | "lab" | "tutorial" | "book" | "project",
          "platform": "Coursera / Udemy / YouTube / AWS / Microsoft Learn / etc.",
          "skill_covered": "Skill this addresses",
          "difficulty": "beginner" | "intermediate" | "advanced",
          "estimated_duration": "2 weeks / 10 hours / etc.",
          "reason": "Why this resource is recommended"
        }
      ],
      "estimated_duration": "4 weeks"
    }
  ],
  "quick_wins": ["Quick actionable tip 1", "Quick tip 2"],
  "long_term_goals": ["6-month goal 1", "12-month goal 2"],
  "tips": ["Study tip 1", "Motivation tip 2"],
  "plan_summary": "2-3 sentence overview of the learning plan"
}

Guidelines:
- Create 3-4 phases: Foundation → Core Skills → Advanced/Specialization → Career Readiness
- Order resources from easy to hard within each phase
- Recommend REAL, well-known courses and platforms (Coursera, Udemy, YouTube, Microsoft Learn, AWS Training, freeCodeCamp, etc.)
- Include a mix of resource types: courses for theory, labs/projects for hands-on practice, certifications for validation
- Focus on FREE or affordable resources when possible
- quick_wins: Things the learner can do TODAY to start learning (e.g., "Watch a 30-min YouTube intro to Docker")
- long_term_goals: Milestones for 6-12 months out
- tips: Practical study strategies and motivation tips
- Keep the plan realistic and achievable for someone working full-time"""


def recommend_learning_path(profile_text: str, target_role_text: str, gaps_summary: str) -> LearningPlan:
    """Generate a personalized learning plan based on identified gaps."""
    user_prompt = f"""## Learner Profile
{profile_text}

## Target Role / Career Goal
{target_role_text}

## Identified Skill Gaps
{gaps_summary}

Create a personalized, phased learning plan to close these gaps. Return JSON only."""

    result = call_llm_json(LEARNING_PATH_SYSTEM_PROMPT, user_prompt)

    type_map = {
        "course": ResourceType.COURSE,
        "certification": ResourceType.CERTIFICATION,
        "lab": ResourceType.LAB,
        "tutorial": ResourceType.TUTORIAL,
        "book": ResourceType.BOOK,
        "project": ResourceType.PROJECT,
    }

    paths = []
    for path_data in result.get("learning_paths", []):
        resources = []
        for res in path_data.get("resources", []):
            resources.append(LearningResource(
                title=res.get("title", ""),
                resource_type=type_map.get(res.get("resource_type", "course"), ResourceType.COURSE),
                platform=res.get("platform", ""),
                skill_covered=res.get("skill_covered", ""),
                difficulty=res.get("difficulty", "beginner"),
                estimated_duration=res.get("estimated_duration", ""),
                reason=res.get("reason", ""),
            ))

        paths.append(LearningPath(
            phase=path_data.get("phase", ""),
            phase_title=path_data.get("phase_title", ""),
            description=path_data.get("description", ""),
            resources=resources,
            estimated_duration=path_data.get("estimated_duration", ""),
        ))

    return LearningPlan(
        learning_paths=paths,
        quick_wins=result.get("quick_wins", []),
        long_term_goals=result.get("long_term_goals", []),
        tips=result.get("tips", []),
        plan_summary=result.get("plan_summary", ""),
    )
