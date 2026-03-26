"""Streamlit Web UI for Personalized Learning & Upskilling Coach."""

import streamlit as st
from app.coach import coach_learner

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Learning Coach",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Personalized Learning & Upskilling Coach")
st.markdown("*AI-powered skill gap analysis and personalized learning path recommendations*")
st.divider()

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ How It Works")
    st.markdown("""
    1. **Describe yourself** — your current role, skills, experience
    2. **Set your goal** — the role or skills you want to achieve
    3. **Get coached** — AI analyzes gaps and builds a learning plan
    
    ---
    
    **The AI Coach will:**
    - ✅ Check what skills you already know
    - ✅ Find what skills you need to improve
    - ✅ Suggest beginner-friendly learning paths
    - ✅ Recommend what to learn **first, next, and later**
    - ✅ Give reminders and learning tips
    """)

# --- Learner Profile Input ---
st.header("1️⃣ Your Profile")
st.markdown("*Tell us about your current role, skills, and experience*")

profile_input_method = st.radio("Input method:", ["Paste Text", "Use Sample"], horizontal=True, key="profile_method")

profile_text = ""
if profile_input_method == "Paste Text":
    profile_text = st.text_area(
        "Describe your background:",
        height=200,
        placeholder=(
            "Example:\n"
            "I'm a fresher with a B.Tech in Computer Science. I know Python basics, "
            "HTML/CSS, and some SQL. I've done a mini project on a student management system "
            "using Flask. I have no industry experience yet but I'm eager to learn cloud and DevOps."
        ),
    )
else:
    sample_profiles = {
        "Junior Developer (Fresher)": """Name: Priya Sharma
Current Role: Fresh Graduate / Intern
Experience: 0 years (just completed B.Tech in Computer Science)
Skills: Python (basic), HTML/CSS, SQL (basic), Git (basic)
Education: B.Tech in Computer Science from XYZ University (2025), CGPA: 7.8
Certifications: None
Projects: Student Management System (Flask + SQLite), Simple Portfolio Website
Interests: Cloud computing, web development, AI/ML""",

        "Mid-Level Developer": """Name: Rahul Verma
Current Role: Junior Software Developer at TechCorp (2 years)
Experience: 2 years in backend development
Skills: Python (intermediate), Java (basic), REST APIs, PostgreSQL, Git, Docker (basic), Linux
Education: B.Tech in IT from ABC College (2023), CGPA: 8.2
Certifications: AWS Cloud Practitioner
Projects: Built internal REST API for inventory management, contributed to microservices migration
Interests: System design, cloud architecture, DevOps""",
    }
    selected_profile = st.selectbox("Choose a sample profile:", list(sample_profiles.keys()))
    profile_text = sample_profiles[selected_profile]
    st.text_area("Profile preview:", value=profile_text, height=200, disabled=True)

# --- Target Role Input ---
st.header("2️⃣ Your Career Goal")
st.markdown("*What role or skill set do you want to achieve?*")

target_input_method = st.radio("Input method:", ["Paste Text", "Use Sample"], horizontal=True, key="target_method")

target_role_text = ""
if target_input_method == "Paste Text":
    target_role_text = st.text_area(
        "Describe your target role or learning goal:",
        height=200,
        placeholder=(
            "Example:\n"
            "I want to become a Cloud DevOps Engineer. The role requires:\n"
            "- Strong Python and scripting skills\n"
            "- AWS or Azure cloud services\n"
            "- Docker and Kubernetes\n"
            "- CI/CD pipelines (Jenkins, GitHub Actions)\n"
            "- Infrastructure as Code (Terraform)\n"
            "- Linux administration\n"
            "- Monitoring and logging tools"
        ),
    )
else:
    sample_targets = {
        "Cloud DevOps Engineer": """Target Role: Cloud DevOps Engineer
Required Skills:
- Python or Bash scripting (advanced)
- AWS services (EC2, S3, Lambda, IAM, VPC, CloudFormation)
- Docker and container orchestration
- Kubernetes (deployment, services, scaling)
- CI/CD pipelines (Jenkins, GitHub Actions, or GitLab CI)
- Infrastructure as Code (Terraform or CloudFormation)
- Linux system administration
- Networking fundamentals
Preferred Skills:
- Monitoring tools (Prometheus, Grafana, CloudWatch)
- Configuration management (Ansible)
- Security best practices
- Agile/Scrum methodology
Experience: 1-3 years in software development or IT operations
Education: B.Tech/B.E. in CS/IT or equivalent""",

        "Full Stack Developer": """Target Role: Full Stack Web Developer
Required Skills:
- JavaScript/TypeScript (advanced)
- React.js or Angular (frontend framework)
- Node.js with Express.js (backend)
- SQL and NoSQL databases (PostgreSQL, MongoDB)
- REST API design and development
- Git version control
- HTML5/CSS3 and responsive design
Preferred Skills:
- Docker basics
- Cloud deployment (AWS/Azure/GCP)
- Testing frameworks (Jest, Cypress)
- GraphQL
- Redis caching
Experience: 0-2 years
Education: B.Tech/B.E. in CS/IT or equivalent""",

        "Data Engineer": """Target Role: Data Engineer
Required Skills:
- Python (advanced) with data libraries (Pandas, PySpark)
- SQL (advanced) - complex queries, optimization, stored procedures
- ETL/ELT pipeline design and development
- Apache Spark or similar big data framework
- Cloud data services (AWS Redshift/Glue or Azure Data Factory)
- Data warehousing concepts
- Airflow or similar workflow orchestration
Preferred Skills:
- Kafka or event streaming
- dbt (data build tool)
- Data modeling and schema design
- Docker and Kubernetes basics
- CI/CD for data pipelines
Experience: 1-3 years in software or data roles
Education: B.Tech/B.E. in CS/IT or equivalent""",
    }
    selected_target = st.selectbox("Choose a sample target role:", list(sample_targets.keys()))
    target_role_text = sample_targets[selected_target]
    st.text_area("Target role preview:", value=target_role_text, height=200, disabled=True)

# --- Coach Button ---
st.header("3️⃣ Get Coached")

if st.button("🚀 Analyze & Build My Learning Plan", type="primary", use_container_width=True):
    if not profile_text.strip():
        st.error("❌ Please describe your profile first.")
    elif not target_role_text.strip():
        st.error("❌ Please describe your target role or learning goal.")
    else:
        with st.spinner("🔍 Analyzing your skills and building a personalized learning plan..."):
            try:
                result = coach_learner(profile_text, target_role_text)
            except Exception as e:
                st.error(f"❌ Coaching failed: {e}")
                st.stop()

        # --- Display Results ---
        st.header("4️⃣ Your Personalized Coaching Report")

        # Motivational message
        st.info(f"💬 **Your Coach Says:** {result.motivational_message}")

        # --- Skill Assessment ---
        st.subheader("📊 Skill Assessment")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Readiness", f"{result.skill_profile.overall_readiness}%")
        with col2:
            st.metric("Total Gaps Found", result.gap_report.total_gaps)
        with col3:
            st.metric("Critical Gaps", len(result.gap_report.critical_gaps))

        st.markdown(f"**Summary:** {result.skill_profile.summary}")

        # Skill level chart
        if result.skill_profile.assessed_skills:
            level_values = {"beginner": 25, "intermediate": 50, "advanced": 75, "expert": 100}
            skill_data = []
            for s in result.skill_profile.assessed_skills:
                skill_data.append({
                    "Skill": s.skill_name,
                    "Your Level": s.current_level.value.title(),
                    "Required Level": s.required_level.value.title(),
                    "Your %": level_values.get(s.current_level.value, 25),
                    "Required %": level_values.get(s.required_level.value, 50),
                })
            st.table(skill_data)

        # Strengths
        str_col1, str_col2 = st.columns(2)
        with str_col1:
            if result.skill_profile.strongest_skills:
                st.markdown("**💪 Your Strongest Skills:**")
                for s in result.skill_profile.strongest_skills:
                    st.markdown(f"- ✅ {s}")
        with str_col2:
            if result.skill_profile.weakest_skills:
                st.markdown("**📈 Skills to Improve:**")
                for s in result.skill_profile.weakest_skills:
                    st.markdown(f"- 🔶 {s}")

        st.divider()

        # --- Gap Analysis ---
        st.subheader("⚠️ Skill Gap Analysis")
        st.markdown(f"**{result.gap_report.gap_summary}**")

        if result.gap_report.critical_gaps:
            st.markdown("### 🔴 Critical Gaps (Learn First)")
            for g in result.gap_report.critical_gaps:
                with st.expander(f"🔴 {g.skill_name} — {g.current_level} → {g.required_level}"):
                    st.write(g.description)

        if result.gap_report.important_gaps:
            st.markdown("### 🟡 Important Gaps (Learn Next)")
            for g in result.gap_report.important_gaps:
                with st.expander(f"🟡 {g.skill_name} — {g.current_level} → {g.required_level}"):
                    st.write(g.description)

        if result.gap_report.nice_to_have_gaps:
            st.markdown("### 🟢 Nice-to-Have (Learn Later)")
            for g in result.gap_report.nice_to_have_gaps:
                with st.expander(f"🟢 {g.skill_name} — {g.current_level} → {g.required_level}"):
                    st.write(g.description)

        if result.gap_report.experience_gaps:
            st.markdown("### 📋 Experience Gaps")
            for eg in result.gap_report.experience_gaps:
                st.markdown(f"- {eg}")

        st.divider()

        # --- Learning Plan ---
        st.subheader("📚 Your Personalized Learning Plan")
        st.markdown(f"**{result.learning_plan.plan_summary}**")

        # Quick wins
        if result.learning_plan.quick_wins:
            st.markdown("### ⚡ Quick Wins (Start Today!)")
            for qw in result.learning_plan.quick_wins:
                st.markdown(f"- 🚀 {qw}")

        # Phased learning path
        for path in result.learning_plan.learning_paths:
            st.markdown(f"### 📖 {path.phase}: {path.phase_title}")
            st.markdown(f"*{path.description}*")
            st.caption(f"⏱️ Estimated duration: {path.estimated_duration}")

            for res in path.resources:
                type_emoji = {
                    "course": "🎬", "certification": "🏆", "lab": "🧪",
                    "tutorial": "📝", "book": "📕", "project": "💻",
                }.get(res.resource_type.value, "📦")

                with st.expander(f"{type_emoji} {res.title} ({res.platform})"):
                    st.markdown(f"**Type:** {res.resource_type.value.title()}")
                    st.markdown(f"**Skill:** {res.skill_covered}")
                    st.markdown(f"**Difficulty:** {res.difficulty.title()}")
                    st.markdown(f"**Duration:** {res.estimated_duration}")
                    st.markdown(f"**Why:** {res.reason}")

        # Long-term goals
        if result.learning_plan.long_term_goals:
            st.markdown("### 🎯 Long-Term Goals")
            for goal in result.learning_plan.long_term_goals:
                st.markdown(f"- 🏁 {goal}")

        # Tips
        if result.learning_plan.tips:
            st.markdown("### 💡 Learning Tips")
            for tip in result.learning_plan.tips:
                st.markdown(f"- 💡 {tip}")
