import streamlit as st
from datetime import datetime

from database import (
    init_database,
    add_problem,
    get_problem,
    add_stakeholder,
    get_stakeholders,
    create_collaboration,
    add_collaboration_member,
    add_task,
    get_tasks,
)

from capability_extraction import extract_capabilities

from matching import (
    compute_matches,
    detect_collaboration_gaps,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SAMAADHAN AI",
    page_icon="🤝",
    layout="wide",
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

init_database()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .tagline {
        font-size: 20px;
        color: #666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 30px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .feature-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        background-color: #ffffff;
        min-height: 170px;
    }

    .feature-card h3 {
        margin-top: 0px;
    }

    .capability-box {
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid #dddddd;
        margin-bottom: 8px;
        background-color: #fafafa;
    }

    .success-box {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #b7dfc2;
        background-color: #f1fff4;
    }

    .warning-box {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #ead39a;
        background-color: #fffaf0;
    }

    .metric-box {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        text-align: center;
    }

    .small-text {
        color: #666;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "Home",
    "problem_id": None,
    "problem": None,
    "domain": None,
    "capabilities": [],
    "matches": [],
    "selected_team": [],
    "collaboration_id": None,
    "collaboration_created": False,
    "partner_added": False,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# DOMAIN DATA
# ============================================================

DOMAIN_LABELS = {
    "agriculture": "Agriculture",
    "waste": "Waste Management",
    "water": "Water Management",
    "education": "Education",
    "healthcare": "Healthcare",
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def go_to(page):
    st.session_state.page = page
    st.rerun()


def capability_names():
    return st.session_state.capabilities


def selected_stakeholder_rows():
    return st.session_state.selected_team


def create_demo_problem():
    """
    Creates the main Crop Disease demonstration problem.
    """

    problem_id = add_problem(
        title="Crop Disease Detection",
        description=(
            "Farmers are facing crop disease affecting leaves. "
            "A practical system is required for disease detection "
            "and field monitoring."
        ),
        category="Agriculture",
        location="Jharkhand",
        source="Community / Field Problem",
        domain_key="agriculture",
    )

    st.session_state.problem_id = problem_id

    st.session_state.problem = get_problem(problem_id)

    analysis = extract_capabilities(
        "Agriculture",
        st.session_state.problem["description"],
    )

    st.session_state.domain = analysis["domain"]

    st.session_state.capabilities = analysis["capabilities"]

    st.session_state.matches = []

    st.session_state.selected_team = []

    st.session_state.collaboration_id = None

    st.session_state.collaboration_created = False

    return problem_id


def load_analysis():
    """
    Extract capabilities for the current problem.
    """

    if not st.session_state.problem:
        return

    problem = st.session_state.problem

    result = extract_capabilities(
        problem["category"],
        problem["description"],
    )

    st.session_state.domain = result["domain"]

    st.session_state.capabilities = result["capabilities"]


def calculate_current_gap():
    """
    Calculate capability coverage for the selected team.
    """

    return detect_collaboration_gaps(
        st.session_state.capabilities,
        st.session_state.selected_team,
    )


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown("## SAMAADHAN AI")

    st.caption("From Problem Matching to Collaboration Composition")

    st.divider()

    pages = [
        "Home",
        "Post a Problem",
        "AI Analysis",
        "AI Matching",
        "Collaboration Workspace",
        "Collaboration Outcome",
        "Collaboration Progress",
        "Partner Registration",
    ]

    for page in pages:

        if st.button(
            page,
            use_container_width=True,
        ):

            st.session_state.page = page

            st.rerun()

    st.divider()

    st.caption(
        "Prototype MVP • Capability-based collaboration"
    )


# ============================================================
# PAGE 1 - HOME
# ============================================================

if st.session_state.page == "Home":

    st.markdown(
        '<div class="main-title">SAMAADHAN AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="tagline">'
        'Turn Problems into Solutions'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "### CONNECT • COLLABORATE • SOLVE"
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">

            <h3>🧩 POST A PROBLEM</h3>

            Submit a societal challenge and let the
            system analyse the capabilities required
            to solve it.

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button(
            "POST A PROBLEM",
            use_container_width=True,
        ):

            go_to("Post a Problem")

    with col2:

        st.markdown(
            """
            <div class="feature-card">

            <h3>🔎 EXPLORE PROBLEMS</h3>

            Discover challenges that can benefit
            from university, expert and industry
            collaboration.

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button(
            "EXPLORE PROBLEMS",
            use_container_width=True,
        ):

            go_to("Post a Problem")

    with col3:

        st.markdown(
            """
            <div class="feature-card">

            <h3>🤝 JOIN AS PARTNER</h3>

            Universities, experts and industry
            partners can register their capabilities
            and collaborate on societal challenges.

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button(
            "JOIN AS PARTNER",
            use_container_width=True,
        ):

            go_to("Partner Registration")

    st.write("")

    st.markdown(
        """
        ### What makes SAMAADHAN AI different?

        **We don't just match the problem; we compose the
        collaboration required to solve it.**
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "**Capability Analysis**\n\n"
            "Identify the capabilities required "
            "for a societal challenge."
        )

    with col2:

        st.info(
            "**Collaboration Composer**\n\n"
            "Bring together multiple stakeholders "
            "with complementary capabilities."
        )

    with col3:

        st.info(
            "**Gap Detection**\n\n"
            "Detect missing capabilities and "
            "recommend the type of partner needed."
        )


# ============================================================
# PAGE 2 - POST A PROBLEM
# ============================================================

elif st.session_state.page == "Post a Problem":

    st.markdown(
        '<div class="section-title">Post a Problem</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Submit a societal challenge for AI-assisted "
        "capability analysis and collaboration matching."
    )

    title = st.text_input(
        "Problem Title",
        value="Crop Disease Detection",
    )

    description = st.text_area(
        "Describe the Problem",
        value=(
            "Farmers are facing crop disease affecting "
            "leaves. A practical system is required for "
            "disease detection and field monitoring."
        ),
        height=140,
    )

    col1, col2 = st.columns(2)

    with col1:

        category = st.selectbox(
            "Category",
            [
                "Agriculture",
                "Waste",
                "Water",
                "Education",
                "Healthcare",
            ],
        )

    with col2:

        location = st.text_input(
            "Location",
            value="Jharkhand",
        )

    source = st.selectbox(
        "Problem Source",
        [
            "Community / Field Problem",
            "Student Submission",
            "Government Challenge",
            "Industry",
            "Research",
        ],
    )

    st.file_uploader(
        "Upload Evidence",
        type=[
            "png",
            "jpg",
            "jpeg",
            "pdf",
        ],
    )

    st.write("")

    if st.button(
        "ANALYZE WITH AI",
        type="primary",
        use_container_width=True,
    ):

        if not title.strip() or not description.strip():

            st.error(
                "Please provide both a problem title "
                "and problem description."
            )

        else:

            domain_key = category.lower()

            problem_id = add_problem(
                title=title,
                description=description,
                category=category,
                location=location,
                source=source,
                domain_key=domain_key,
            )

            st.session_state.problem_id = problem_id

            st.session_state.problem = get_problem(
                problem_id
            )

            load_analysis()

            st.session_state.page = "AI Analysis"

            st.rerun()


# ============================================================
# PAGE 3 - AI ANALYSIS
# ============================================================

elif st.session_state.page == "AI Analysis":

    st.markdown(
        '<div class="section-title">AI Analysis</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.problem:

        st.warning(
            "No problem has been submitted yet."
        )

        if st.button("POST A PROBLEM"):

            go_to("Post a Problem")

    else:

        problem = st.session_state.problem

        st.success(
            "✓ Problem successfully analysed"
        )

        st.markdown("### Problem Detected")

        st.info(
            problem["description"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Category")

            st.write(
                f"**{problem['category']}**"
            )

        with col2:

            st.markdown("### Location")

            st.write(
                f"**{problem['location']}**"
            )

        st.markdown("### Required Capabilities")

        for capability in st.session_state.capabilities:

            st.markdown(
                f"""
                <div class="capability-box">
                ✓ {capability}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### AI-Assisted Analysis")

        st.info(
            "This MVP uses transparent capability extraction "
            "from the problem category and description. "
            "The architecture can later integrate richer "
            "NLP or semantic models."
        )

        st.markdown(
            """
            **AI Recommendation**

            This challenge requires collaboration between
            multiple stakeholders with complementary
            agriculture, AI/ML, IoT and hardware capabilities.
            """
        )

        if st.button(
            "FIND MATCHES →",
            type="primary",
            use_container_width=True,
        ):

            stakeholders = get_stakeholders(
                st.session_state.domain
            )

            stakeholder_data = []

            for stakeholder in stakeholders:

                capabilities = stakeholder["capabilities"]

                stakeholder_data.append(
                    {
                        "id": stakeholder["id"],
                        "name": stakeholder["name"],
                        "type": stakeholder["partner_type"],
                        "capabilities": [
                            item.strip()
                            for item in capabilities.split(",")
                        ],
                    }
                )

            st.session_state.matches = compute_matches(
                st.session_state.capabilities,
                stakeholder_data,
            )

            st.session_state.page = "AI Matching"

            st.rerun()


# ============================================================
# PAGE 4 - AI MATCHING
# ============================================================

elif st.session_state.page == "AI Matching":

    st.markdown(
        '<div class="section-title">AI Matching</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.capabilities:

        st.warning(
            "Analyse a problem first."
        )

        if st.button("GO TO AI ANALYSIS"):

            go_to("AI Analysis")

    else:

        st.write(
            "Match required capabilities with universities, "
            "experts and industry partners."
        )

        stakeholders = get_stakeholders(
            st.session_state.domain
        )

        stakeholder_data = []

        for stakeholder in stakeholders:

            stakeholder_data.append(
                {
                    "id": stakeholder["id"],
                    "name": stakeholder["name"],
                    "type": stakeholder["partner_type"],
                    "capabilities": [
                        item.strip()
                        for item in stakeholder["capabilities"].split(",")
                    ],
                }
            )

        matches = compute_matches(
            st.session_state.capabilities,
            stakeholder_data,
        )

        st.session_state.matches = matches

        for index, match in enumerate(matches):

            with st.container(border=True):

                col1, col2 = st.columns(
                    [3, 1]
                )

                with col1:

                    st.subheader(
                        match["name"]
                    )

                    st.caption(
                        match["type"]
                    )

                    if match[
                        "matched_capabilities"
                    ]:

                        st.write(
                            "Covers: "
                            + ", ".join(
                                match[
                                    "matched_capabilities"
                                ]
                            )
                        )

                    st.caption(
                        "Declared capabilities: "
                        + ", ".join(
                            match["capabilities"]
                        )
                    )

                with col2:

                    status = match[
                        "overall_status"
                    ]

                    if status == "STRONG MATCH":

                        st.success(status)

                    elif status == "GOOD MATCH":

                        st.info(status)

                    elif status == "PARTIAL MATCH":

                        st.warning(status)

                    else:

                        st.error(status)

                    if st.button(
                        "ADD TO TEAM",
                        key=f"add_{index}",
                    ):

                        existing_names = [
                            member["name"]
                            for member
                            in st.session_state.selected_team
                        ]

                        if (
                            match["name"]
                            not in existing_names
                        ):

                            st.session_state.selected_team.append(
                                {
                                    "id": next(
                                        (
                                            s["id"]
                                            for s
                                            in stakeholder_data
                                            if s["name"]
                                            == match["name"]
                                        ),
                                        None,
                                    ),
                                    "name": match["name"],
                                    "type": match["type"],
                                    "capabilities": match[
                                        "capabilities"
                                    ],
                                }
                            )

                            st.success(
                                "Added to collaboration team."
                            )

        st.write("")

        st.markdown("### Capability Coverage")

        if st.session_state.selected_team:

            gap = calculate_current_gap()

            covered_count = len(
                gap["covered"]
            )

            total_count = len(
                st.session_state.capabilities
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Capabilities Covered",
                    f"{covered_count}/{total_count}",
                )

            with col2:

                st.metric(
                    "Team Members",
                    len(
                        st.session_state.selected_team
                    ),
                )

            with col3:

                st.metric(
                    "Missing Capabilities",
                    len(gap["missing"]),
                )

            if gap["missing"]:

                st.warning(
                    "⚠ Collaboration Gap Detected"
                )

                for missing in gap["missing"]:

                    st.write(
                        f"**Missing:** {missing}"
                    )

                for recommendation in gap["gaps"]:

                    st.info(
                        "AI Recommendation: "
                        + recommendation[
                            "recommended_partner"
                        ]
                    )

            else:

                st.success(
                    "✓ All required capabilities are covered."
                )

        else:

            st.info(
                "Add stakeholders to the collaboration "
                "team to calculate capability coverage."
            )

        st.write("")

        if st.button(
            "CONTINUE TO COLLABORATION →",
            type="primary",
            use_container_width=True,
        ):

            go_to("Collaboration Workspace")


# ============================================================
# PAGE 5 - COLLABORATION WORKSPACE
# ============================================================

elif st.session_state.page == "Collaboration Workspace":

    st.markdown(
        '<div class="section-title">'
        'Collaboration Workspace'
        '</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.problem:

        st.warning(
            "Please submit a problem first."
        )

    else:

        problem = st.session_state.problem

        st.markdown(
            f"### {problem['title']} — {problem['location']}"
        )

        st.write(
            "Goal: Identify the problem requirements and "
            "develop a practical collaborative solution."
        )

        st.markdown("### Collaboration Team")

        if not st.session_state.selected_team:

            st.info(
                "No stakeholders have been added yet."
            )

        else:

            for member in st.session_state.selected_team:

                st.markdown(
                    f"""
                    <div class="capability-box">
                    <b>{member['name']}</b><br>
                    {member['type']}<br>
                    <span class="small-text">
                    Capabilities: {", ".join(member['capabilities'])}
                    </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("### Capability Coverage")

        gap = calculate_current_gap()

        st.write(
            f"**{len(gap['covered'])}/"
            f"{len(st.session_state.capabilities)} "
            f"capabilities covered**"
        )

        if gap["missing"]:

            st.warning(
                "Missing capabilities detected."
            )

            for missing in gap["missing"]:

                st.write(
                    f"⚠ {missing}"
                )

            for recommendation in gap["gaps"]:

                st.info(
                    "Recommended partner: "
                    + recommendation[
                        "recommended_partner"
                    ]
                )

        else:

            st.success(
                "✓ All required capabilities are covered."
            )

        st.markdown("### Task Lifecycle")

        tasks = [
            ("✓", "Challenge analysed", "Completed"),
            (
                "✓",
                "Required capabilities identified",
                "Completed",
            ),
            (
                "✓",
                "Collaboration team formed",
                "Completed",
            ),
            (
                "↻",
                "Solution development",
                "In Progress",
            ),
            (
                "○",
                "Field pilot",
                "Pending",
            ),
        ]

        for icon, label, status in tasks:

            st.write(
                f"{icon} **{label}** — {status}"
            )

        st.write("")

        if gap["missing"]:

            st.error(
                "The collaboration is incomplete. "
                "Add the recommended partner before "
                "creating the final collaboration."
            )

            if st.button(
                "BACK TO AI MATCHING",
                use_container_width=True,
            ):

                go_to("AI Matching")

        else:

            if st.button(
                "CREATE COLLABORATION",
                type="primary",
                use_container_width=True,
            ):

                collaboration_id = create_collaboration(
                    st.session_state.problem_id,
                    st.session_state.domain,
                    "active",
                )

                st.session_state.collaboration_id = (
                    collaboration_id
                )

                for member in st.session_state.selected_team:

                    add_collaboration_member(
                        collaboration_id=collaboration_id,
                        stakeholder_id=member["id"],
                        name=member["name"],
                        partner_type=member["type"],
                        role=member["type"],
                    )

                task_definitions = [
                    (
                        "Challenge analysed",
                        "Completed",
                    ),
                    (
                        "Required capabilities identified",
                        "Completed",
                    ),
                    (
                        "Collaboration team formed",
                        "Completed",
                    ),
                    (
                        "Solution development",
                        "In Progress",
                    ),
                    (
                        "Field pilot",
                        "Pending",
                    ),
                ]

                for order, (
                    label,
                    status,
                ) in enumerate(task_definitions):

                    add_task(
                        collaboration_id,
                        label,
                        status,
                        order,
                    )

                st.session_state.collaboration_created = True

                go_to(
                    "Collaboration Outcome"
                )


# ============================================================
# PAGE 6 - COLLABORATION OUTCOME
# ============================================================

elif st.session_state.page == "Collaboration Outcome":

    st.markdown(
        '<div class="section-title">'
        'Collaboration Outcome'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "From problem analysis to a complete collaboration."
    )

    if not st.session_state.problem:

        st.warning(
            "No problem available."
        )

    else:

        problem = st.session_state.problem

        gap = calculate_current_gap()

        st.markdown(
            """
            ### AI-Generated Collaboration Plan
            """
        )

        st.info(
            f"**Problem:** {problem['category']} — "
            f"{problem['location']}\n\n"
            "AI analysis identified the capabilities "
            "required for the problem and composed "
            "relevant stakeholders to work together."
        )

        st.markdown("### Required Capabilities")

        for capability in st.session_state.capabilities:

            st.write(
                f"✓ {capability}"
            )

        st.markdown("### Composed Collaboration")

        for member in st.session_state.selected_team:

            st.markdown(
                f"""
                <div class="capability-box">
                <b>{member['name']}</b><br>
                {member['type']}<br>
                Capabilities: {", ".join(member['capabilities'])}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            "### Collaboration Gap Detection"
        )

        if gap["missing"]:

            st.error(
                "Gap Detected"
            )

            for missing in gap["missing"]:

                st.write(
                    f"Missing: **{missing}**"
                )

        else:

            st.success(
                "✓ 4/4 CAPABILITIES COVERED"
            )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Required Capabilities",
                len(
                    st.session_state.capabilities
                ),
            )

        with col2:

            st.metric(
                "Capabilities Covered",
                len(
                    gap["covered"]
                ),
            )

        st.write("")

        if st.button(
            "TRACK COLLABORATION →",
            type="primary",
            use_container_width=True,
        ):

            go_to(
                "Collaboration Progress"
            )


# ============================================================
# PAGE 7 - COLLABORATION PROGRESS
# ============================================================

elif st.session_state.page == "Collaboration Progress":

    st.markdown(
        '<div class="section-title">'
        'Collaboration Progress'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Track the journey from collaboration to solution."
    )

    if not st.session_state.problem:

        st.warning(
            "No active collaboration."
        )

    else:

        st.markdown(
            "### Collaboration Team"
        )

        for member in st.session_state.selected_team:

            st.write(
                f"**{member['name']}** — "
                f"{member['type']}"
            )

        st.markdown(
            "### Collaboration Progress"
        )

        progress_items = [
            (
                "✓",
                "Challenge Analysed",
                "Completed",
            ),
            (
                "✓",
                "Capabilities Identified",
                "Completed",
            ),
            (
                "✓",
                "Collaboration Formed",
                "Completed",
            ),
            (
                "↻",
                "Solution Development",
                "In Progress",
            ),
            (
                "○",
                "Field Pilot",
                "Pending",
            ),
            (
                "○",
                "Wider Deployment",
                "Future",
            ),
        ]

        for icon, label, status in progress_items:

            st.write(
                f"{icon} **{label}** — {status}"
            )

        st.markdown(
            "### Collaboration Status"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                "✓ Team Formed — Completed"
            )

            st.success(
                "✓ Tasks Assigned — Completed"
            )

        with col2:

            st.info(
                "↻ Solution Development — In Progress"
            )

            st.warning(
                "○ Field Pilot — Pending"
            )

        st.markdown(
            "### Prototype Demonstration"
        )

        gap = calculate_current_gap()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Challenges Analysed",
                "1",
            )

        with col2:

            st.metric(
                "Required Capabilities",
                len(
                    st.session_state.capabilities
                ),
            )

        with col3:

            st.metric(
                "Stakeholder Roles",
                len(
                    st.session_state.selected_team
                ),
            )

        with col4:

            st.metric(
                "Collaboration Plans",
                "1",
            )

        st.caption(
            "Values are based on the current prototype demonstration."
        )


# ============================================================
# PAGE 8 - PARTNER REGISTRATION
# ============================================================

elif st.session_state.page == "Partner Registration":

    st.markdown(
        '<div class="section-title">'
        'Partner Registration'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Register a university, expert or industry partner "
        "and declare the capabilities you can contribute."
    )

    with st.form("partner_registration"):

        partner_name = st.text_input(
            "Organization / Partner Name"
        )

        partner_type = st.selectbox(
            "Partner Type",
            [
                "University / Student Team",
                "Domain Expert",
                "Industry Partner",
                "Research Institution",
                "NGO / Community Partner",
            ],
        )

        areas = st.multiselect(
            "Capabilities / Areas",
            [
                "Agriculture",
                "Plant Pathology",
                "AI/ML",
                "Computer Vision",
                "IoT",
                "Sensors",
                "Field Monitoring",
                "Hardware",
                "Prototype Development",
                "Automation",
                "Data Analytics",
                "Software Development",
                "Education",
                "Healthcare",
                "Environmental Science",
            ],
        )

        location = st.text_input(
            "Location"
        )

        contact_person = st.text_input(
            "Contact Person"
        )

        email = st.text_input(
            "Email"
        )

        description = st.text_area(
            "Description"
        )

        submitted = st.form_submit_button(
            "REGISTER PARTNER",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        if not partner_name.strip():

            st.error(
                "Please enter the organization or partner name."
            )

        elif not areas:

            st.error(
                "Please select at least one capability."
            )

        else:

            domain_key = "agriculture"

            selected_text = " ".join(
                areas
            ).lower()

            if any(
                word in selected_text
                for word in [
                    "waste",
                    "recycling",
                    "garbage",
                ]
            ):

                domain_key = "waste"

            elif any(
                word in selected_text
                for word in [
                    "water",
                    "irrigation",
                    "environmental",
                ]
            ):

                domain_key = "water"

            elif "education" in selected_text:

                domain_key = "education"

            elif "healthcare" in selected_text:

                domain_key = "healthcare"

            add_stakeholder(
                name=partner_name,
                partner_type=partner_type,
                domain_key=domain_key,
                capabilities=", ".join(
                    areas
                ),
                location=location,
                contact_person=contact_person,
                email=email,
                description=description,
            )

            st.success(
                f"✓ {partner_name} registered successfully."
            )

            st.info(
                "The partner is now stored in the SQLite "
                "database and can participate in future "
                "capability-based matching."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SAMAADHAN AI • From Problem Matching to Collaboration Composition"
)