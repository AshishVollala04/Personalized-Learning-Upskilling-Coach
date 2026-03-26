"""CLI entry point for Personalized Learning & Upskilling Coach."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.coach import coach_learner


def print_result(result):
    """Print the coaching result to console."""
    print(f"\n{'='*70}")
    print(f"  🎓 PERSONALIZED LEARNING & UPSKILLING REPORT")
    print(f"{'='*70}")

    # Motivational message
    print(f"\n💬 YOUR COACH SAYS:")
    print(f"  {result.motivational_message}")

    # Skill Assessment
    print(f"\n{'='*70}")
    print(f"📊 SKILL ASSESSMENT (Readiness: {result.skill_profile.overall_readiness}%)")
    print(f"{'='*70}")
    print(f"  {result.skill_profile.summary}")

    if result.skill_profile.assessed_skills:
        print(f"\n  {'Skill':<25} {'Your Level':<15} {'Required':<15}")
        print(f"  {'-'*55}")
        for s in result.skill_profile.assessed_skills:
            print(f"  {s.skill_name:<25} {s.current_level.value:<15} {s.required_level.value:<15}")

    if result.skill_profile.strongest_skills:
        print(f"\n  💪 Strongest: {', '.join(result.skill_profile.strongest_skills)}")
    if result.skill_profile.weakest_skills:
        print(f"  📈 Needs Work: {', '.join(result.skill_profile.weakest_skills)}")

    # Gap Analysis
    print(f"\n{'='*70}")
    print(f"⚠️  GAP ANALYSIS ({result.gap_report.total_gaps} gaps found)")
    print(f"{'='*70}")
    print(f"  {result.gap_report.gap_summary}")

    if result.gap_report.critical_gaps:
        print(f"\n  🔴 CRITICAL (Learn First):")
        for g in result.gap_report.critical_gaps:
            print(f"    - {g.skill_name}: {g.current_level} → {g.required_level}")
            print(f"      {g.description}")

    if result.gap_report.important_gaps:
        print(f"\n  🟡 IMPORTANT (Learn Next):")
        for g in result.gap_report.important_gaps:
            print(f"    - {g.skill_name}: {g.current_level} → {g.required_level}")
            print(f"      {g.description}")

    if result.gap_report.nice_to_have_gaps:
        print(f"\n  🟢 NICE-TO-HAVE (Learn Later):")
        for g in result.gap_report.nice_to_have_gaps:
            print(f"    - {g.skill_name}: {g.current_level} → {g.required_level}")

    if result.gap_report.experience_gaps:
        print(f"\n  📋 Experience Gaps:")
        for eg in result.gap_report.experience_gaps:
            print(f"    - {eg}")

    # Learning Plan
    print(f"\n{'='*70}")
    print(f"📚 YOUR PERSONALIZED LEARNING PLAN")
    print(f"{'='*70}")
    print(f"  {result.learning_plan.plan_summary}")

    if result.learning_plan.quick_wins:
        print(f"\n  ⚡ Quick Wins (Start Today!):")
        for qw in result.learning_plan.quick_wins:
            print(f"    - 🚀 {qw}")

    for path in result.learning_plan.learning_paths:
        print(f"\n  📖 {path.phase}: {path.phase_title}")
        print(f"     {path.description}")
        print(f"     ⏱️  Duration: {path.estimated_duration}")
        for res in path.resources:
            type_emoji = {
                "course": "🎬", "certification": "🏆", "lab": "🧪",
                "tutorial": "📝", "book": "📕", "project": "💻",
            }.get(res.resource_type.value, "📦")
            print(f"       {type_emoji} {res.title} ({res.platform}) - {res.estimated_duration}")
            print(f"         Skill: {res.skill_covered} | Difficulty: {res.difficulty}")

    if result.learning_plan.long_term_goals:
        print(f"\n  🎯 Long-Term Goals:")
        for goal in result.learning_plan.long_term_goals:
            print(f"    - {goal}")

    if result.learning_plan.tips:
        print(f"\n  💡 Learning Tips:")
        for tip in result.learning_plan.tips:
            print(f"    - {tip}")

    print(f"\n{'='*70}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <profile_file> <target_role_file>")
        print("\nExample:")
        print("  python main.py sample_data/profile_junior.txt sample_data/target_devops.txt")
        sys.exit(1)

    profile_path = sys.argv[1]
    target_path = sys.argv[2]

    # Read profile
    print("👤 Reading learner profile...")
    with open(profile_path, "r", encoding="utf-8") as f:
        profile_text = f.read()

    # Read target role
    print("🎯 Reading target role...")
    with open(target_path, "r", encoding="utf-8") as f:
        target_role_text = f.read()

    # Run coaching pipeline
    print("🔍 Analyzing skills and building your learning plan...")
    result = coach_learner(profile_text, target_role_text)
    print_result(result)


if __name__ == "__main__":
    main()
