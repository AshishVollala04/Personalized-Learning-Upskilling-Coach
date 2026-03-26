"""Data models for the Personalized Learning & Upskilling Coach."""

from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class GapPriority(str, Enum):
    CRITICAL = "critical"
    IMPORTANT = "important"
    NICE_TO_HAVE = "nice_to_have"


class ResourceType(str, Enum):
    COURSE = "course"
    CERTIFICATION = "certification"
    LAB = "lab"
    TUTORIAL = "tutorial"
    BOOK = "book"
    PROJECT = "project"


class LearnerProfile(BaseModel):
    """Parsed learner profile structure."""
    name: str = ""
    current_role: str = ""
    experience_years: Optional[float] = None
    current_skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    raw_text: str = ""


class TargetRole(BaseModel):
    """Target role / career goal structure."""
    title: str = ""
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    min_experience_years: Optional[int] = None
    responsibilities: list[str] = Field(default_factory=list)
    raw_text: str = ""


class SkillAssessment(BaseModel):
    """Assessment of a learner's current skill levels."""
    skill_name: str = ""
    current_level: ProficiencyLevel = ProficiencyLevel.BEGINNER
    required_level: ProficiencyLevel = ProficiencyLevel.INTERMEDIATE
    confidence: float = Field(0, ge=0, le=100, description="Confidence in this assessment")


class SkillProfile(BaseModel):
    """Complete skill profile of the learner."""
    assessed_skills: list[SkillAssessment] = Field(default_factory=list)
    strongest_skills: list[str] = Field(default_factory=list)
    weakest_skills: list[str] = Field(default_factory=list)
    overall_readiness: float = Field(0, ge=0, le=100, description="Overall readiness for target role")
    summary: str = ""


class SkillGap(BaseModel):
    """A single identified skill gap."""
    skill_name: str = ""
    current_level: str = ""
    required_level: str = ""
    priority: GapPriority = GapPriority.IMPORTANT
    description: str = ""


class GapReport(BaseModel):
    """Complete gap analysis report."""
    critical_gaps: list[SkillGap] = Field(default_factory=list)
    important_gaps: list[SkillGap] = Field(default_factory=list)
    nice_to_have_gaps: list[SkillGap] = Field(default_factory=list)
    experience_gaps: list[str] = Field(default_factory=list)
    total_gaps: int = 0
    gap_summary: str = ""


class LearningResource(BaseModel):
    """A single recommended learning resource."""
    title: str = ""
    resource_type: ResourceType = ResourceType.COURSE
    platform: str = ""
    skill_covered: str = ""
    difficulty: str = ""
    estimated_duration: str = ""
    reason: str = ""


class LearningPath(BaseModel):
    """Structured learning path with ordered steps."""
    phase: str = ""
    phase_title: str = ""
    description: str = ""
    resources: list[LearningResource] = Field(default_factory=list)
    estimated_duration: str = ""


class LearningPlan(BaseModel):
    """Complete learning plan with multiple phases."""
    learning_paths: list[LearningPath] = Field(default_factory=list)
    quick_wins: list[str] = Field(default_factory=list)
    long_term_goals: list[str] = Field(default_factory=list)
    tips: list[str] = Field(default_factory=list)
    plan_summary: str = ""


class CoachingResult(BaseModel):
    """Complete coaching result combining all analysis."""
    learner_name: str = ""
    current_role: str = ""
    target_role: str = ""
    skill_profile: SkillProfile = Field(default_factory=SkillProfile)
    gap_report: GapReport = Field(default_factory=GapReport)
    learning_plan: LearningPlan = Field(default_factory=LearningPlan)
    motivational_message: str = ""
