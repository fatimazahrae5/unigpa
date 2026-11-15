

import streamlit as st
import plotly.graph_objects as go
from gpa_calculator import calculate_gpa, convert_grades, GRADE_POINTS

st.set_page_config(
    page_title="UniGPA | Academic Planner",
    page_icon="📈",
    layout="wide"
)

# ---------- DESIGN ----------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');

html, body, [data-testid="stApp"] {
    font-family: 'DM Sans', sans-serif;
    color: #244432;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at 96% 0%,
            #ffe6ee 0,
            transparent 25%
        ),
        #fffdfc;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        165deg, #fff0f4, #fff9f8
    );
    border-right: 1px solid #efdfe3;
}

h1, h2, h3 {
    font-family: 'Outfit', sans-serif;
    color: #214e34 !important;
}

[data-testid="stMetric"] {
    border-radius: 20px;
    padding: 20px;
    background: linear-gradient(
        130deg, #fce3eb, #fff5f8
    );
    border: 1px solid #f2d7e1;
    box-shadow: 0 8px 24px #c98c9a13;
}

[data-testid="stMetricValue"] {
    color: #9e365f;
    font-weight: 800;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 20px !important;
    border-color: #eadce1 !important;
}

.stButton button {
    border-radius: 12px;
    background: #e3f1e3;
    color: #205536;
    border: 1px solid #cde1ce;
    font-weight: 700;
}

.stButton button:hover {
    background: #d4e9d5;
    color: #18432b;
    border-color: #9bc9a3;
}

.stButton button[kind="primary"] {
    background: #347a4b;
    color: white;
    border: 0;
}

.stButton button[kind="primary"]:hover {
    background: #245e38;
    color: white;
}

.hero {
    padding: 28px 34px;
    background: linear-gradient(
        105deg,
        #fff0f5 0%,
        #ffffff 55%,
        #e8f3e7 100%
    );
    border: 1px solid #f2e0e5;
    border-radius: 24px;
    margin-bottom: 24px;
}

.hero .eyebrow {
    color: #ae5677;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
}

.hero h1 {
    font-size: 3rem;
    margin: 6px 0;
}

.hero p {
    font-size: 1.05rem;
    color: #5b6c61;
    margin: 0;
}

.section-kicker {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #a65b76;
    text-transform: uppercase;
    margin: 10px 0;
}

.action-card {
    border: 1px solid #e7dfe2;
    background: linear-gradient(
        125deg, #fff, #f6fbf5
    );
    padding: 22px;
    border-radius: 20px;
    min-height: 150px;
    box-shadow: 0 8px 26px #315e3a0a;
}

.action-card.pink {
    background: linear-gradient(
        125deg, #fff, #fff0f5
    );
}

.action-card .num {
    color: #b65b80;
    font-size: 13px;
    font-weight: 800;
}

.action-card h3 {
    font-size: 21px;
    margin: 10px 0 6px;
}

.action-card p {
    font-size: 14px;
    color: #63756a;
}

.result-card {
    padding: 26px;
    text-align: center;
    border-radius: 22px;
    background: linear-gradient(
        120deg, #ffe8ef, #edf7eb
    );
    border: 1px solid #e8d5dc;
    margin-top: 16px;
}

.result-card .value {
    font-size: 3.3rem;
    font-weight: 800;
    color: #245d39;
}

.result-card .label {
    font-weight: 700;
    color: #9d496a;
    letter-spacing: 1px;
}

.muted {
    color: #687a70;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------

DEFAULTS = {
    "semester_gpa": None,
    "future_gpa": None,
    "current_gpa": 0.0,
    "completed_credits": 0,
    "gpa_goal": 3.5,
    "page": "Dashboard",
    "history": [],
    "future_credits": 0
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

PAGES = [
    "Dashboard",
    "GPA Calculator",
    "Future GPA",
    "Grade Converter",
    "About"
]

# ---------- FUNCTIONS ----------

def goto(page):
    st.session_state.page = page
    st.rerun()


def result_card(label, value):
    st.markdown(
        f"""
        <div class="result-card">
            <div class="label">{label}</div>
            <div class="value">
                {value:.3f}
                <span style="font-size:22px">
                    / 4.3
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def course_inputs(prefix):
    count = st.number_input(
        "Number of courses",
        min_value=1,
        max_value=12,
        value=4,
        step=1,
        key=f"{prefix}_count"
    )

    grades = []
    credits = []

    for i in range(int(count)):
        with st.container(border=True):
            st.markdown(f"**Course {i + 1:02d}**")

            a, b = st.columns(2)

            with a:
                grade = st.selectbox(
                    "Letter grade",
                    list(GRADE_POINTS),
                    key=f"{prefix}_grade_{i}"
                )
                grades.append(grade)

            with b:
                credit = st.number_input(
                    "Credits",
                    min_value=1,
                    max_value=6,
                    value=3,
                    key=f"{prefix}_credit_{i}"
                )
                credits.append(credit)

    return grades, credits


# ---------- SIDEBAR ----------

with st.sidebar:
    st.markdown("# UniGPA")
    st.caption("Academic planning studio")
    st.divider()

    selected = st.radio(
        "Navigation",
        PAGES,
        key="page",
        label_visibility="collapsed"
    )

    st.divider()
    st.caption("Track. Plan. Improve.")

# ---------- HEADER ----------

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">
            Your academic space
        </div>
        <h1>Welcome to UniGPA</h1>
        <p>
            Calculate, plan, and visualize
            your academic progress.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- DASHBOARD ----------

if selected == "Dashboard":

    st.markdown(
        '<div class="section-kicker">At a glance</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        semester = st.session_state.semester_gpa

        st.metric(
            "Semester GPA",
            f"{semester:.3f} / 4.3"
            if semester is not None
            else "Not calculated"
        )

    with c2:
        future = st.session_state.future_gpa

        st.metric(
            "Predicted cumulative GPA",
            f"{future:.3f} / 4.3"
            if future is not None
            else "Not calculated"
        )

    with c3:
        st.metric(
            "GPA goal",
            f"{st.session_state.gpa_goal:.2f} / 4.3"
        )

    left, right = st.columns(2)

    # ACADEMIC PROGRESS

    with left:
        with st.container(border=True):
            st.subheader("Academic progress")

            st.number_input(
                "Your current cumulative GPA",
                min_value=0.0,
                max_value=4.3,
                step=0.01,
                key="current_gpa"
            )

            st.number_input(
                "Credits included in GPA",
                min_value=0,
                step=1,
                key="completed_credits"
            )

            st.number_input(
                "Target GPA",
                min_value=0.1,
                max_value=4.3,
                step=0.1,
                key="gpa_goal"
            )

            current = st.session_state.current_gpa
            goal = st.session_state.gpa_goal

            progress = min(current / goal, 1.0)

            st.progress(progress)

            st.caption(
                f"{current:.3f} of {goal:.2f} "
                f"GPA goal ({current / goal:.0%})"
            )

            st.caption(
                "This measures your GPA relative "
                "to your goal, not degree completion."
            )

    # GPA TREND

    with right:
        with st.container(border=True):
            st.subheader("GPA trend")

            st.caption(
                "Add actual semester GPAs "
                "to visualize your progress."
            )

            with st.form(
                "history_form",
                clear_on_submit=True
            ):
                a, b = st.columns([2, 1])

                with a:
                    term = st.text_input(
                        "Term",
                        placeholder="Fall 2026"
                    )

                with b:
                    gpa_value = st.number_input(
                        "GPA",
                        min_value=0.0,
                        max_value=4.3,
                        value=3.0,
                        step=0.01
                    )

                submitted = st.form_submit_button(
                    "Add term"
                )

            if submitted:
                if term.strip():
                    st.session_state.history.append(
                        (term.strip(), float(gpa_value))
                    )
                else:
                    st.warning("Enter a term name first.")

            if st.session_state.history:

                labels, values = zip(
                    *st.session_state.history
                )

                fig = go.Figure(
                    go.Scatter(
                        x=list(labels),
                        y=list(values),
                        mode="lines+markers",
                        line=dict(
                            color="#438957",
                            width=4
                        ),
                        marker=dict(
                            color="#d86e9a",
                            size=10
                        ),
                        fill="tozeroy",
                        fillcolor="rgba(215,236,217,0.35)"
                    )
                )

                fig.update_layout(
                    height=240,
                    margin=dict(
                        l=10,
                        r=10,
                        t=10,
                        b=10
                    ),
                    yaxis=dict(
                        range=[0, 4.3],
                        title="GPA"
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                if st.button("Clear trend"):
                    st.session_state.history = []
                    st.rerun()

            else:
                st.info(
                    "Your trend will appear here "
                    "after you add a term."
                )

    # QUICK ACTIONS

    st.subheader("Quick actions")

    a, b, c = st.columns(3)

    actions = [
        (
            a,
            "01 / CALCULATE",
            "GPA Calculator",
            "Calculate a weighted semester GPA.",
            "Open calculator",
            "GPA Calculator"
        ),
        (
            b,
            "02 / PLAN",
            "Future GPA",
            "See how upcoming grades change your GPA.",
            "Open simulator",
            "Future GPA"
        ),
        (
            c,
            "03 / CONVERT",
            "Grade Converter",
            "Convert letter grades into points.",
            "Open converter",
            "Grade Converter"
        )
    ]

    for i, action in enumerate(actions):

        column, number, title, description, button, target = action

        with column:
            cls = (
                "action-card pink"
                if i == 1
                else "action-card"
            )

            st.markdown(
                f"""
                <div class="{cls}">
                    <div class="num">{number}</div>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                button,
                key=f"quick_{i}",
                use_container_width=True
            ):
                goto(target)

# ---------- GPA CALCULATOR ----------

elif selected == "GPA Calculator":

    st.header("Semester GPA Calculator")

    st.write(
        "Enter your courses to calculate "
        "a credit-weighted semester GPA."
    )

    grades, credits = course_inputs("semester")

    if st.button(
        "Calculate GPA",
        type="primary",
        use_container_width=True
    ):
        st.session_state.semester_gpa = calculate_gpa(
            convert_grades(grades),
            credits
        )

    if st.session_state.semester_gpa is not None:
        result_card(
            "SEMESTER GPA",
            st.session_state.semester_gpa
        )

# ---------- FUTURE GPA ----------

elif selected == "Future GPA":

    st.header("Future GPA Simulator")

    st.write(
        "Explore how your upcoming courses "
        "may affect your cumulative GPA."
    )

    a, b = st.columns(2)

    with a:
        st.number_input(
            "Current cumulative GPA",
            min_value=0.0,
            max_value=4.3,
            step=0.01,
            key="current_gpa"
        )

    with b:
        st.number_input(
            "Credits included in GPA",
            min_value=0,
            step=1,
            key="completed_credits"
        )

    grades, credits = course_inputs("future")

    if st.button(
        "Predict cumulative GPA",
        type="primary",
        use_container_width=True
    ):
        points = sum(
            g * c
            for g, c in zip(
                convert_grades(grades),
                credits
            )
        )

        new_credits = sum(credits)

        total = (
            st.session_state.completed_credits
            + new_credits
        )

        predicted = (
            st.session_state.current_gpa
            * st.session_state.completed_credits
            + points
        ) / total

        st.session_state.future_gpa = round(
            predicted, 3
        )

        st.session_state.future_credits = new_credits

    if st.session_state.future_gpa is not None:

        result_card(
            "PREDICTED CUMULATIVE GPA",
            st.session_state.future_gpa
        )

        difference = (
            st.session_state.future_gpa
            - st.session_state.current_gpa
        )

        st.metric(
            "Change from current GPA",
            f"{difference:+.3f}"
        )

    st.caption(
        "Estimates only. Repeated courses "
        "and institutional policies may change "
        "official GPA results."
    )

# ---------- GRADE CONVERTER ----------

elif selected == "Grade Converter":

    st.header("Grade Converter")

    grade = st.selectbox(
        "Letter grade",
        list(GRADE_POINTS)
    )

    result_card(
        f"{grade} IN GRADE POINTS",
        GRADE_POINTS[grade]
    )

    st.dataframe(
        {
            "Letter grade": list(GRADE_POINTS),
            "Grade points": list(
                GRADE_POINTS.values()
            )
        },
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "This grade scale is provisional. "
        "Verify it against your university's "
        "official rules."
    )

# ---------- ABOUT ----------

else:

    st.header("About UniGPA")

    st.write(
        "UniGPA is an academic planning tool "
        "for weighted GPA calculations and "
        "future-grade simulations."
    )

    st.write(
        "Developer: Fatima Zahrae El Fakir"
    )

    st.caption(
        "Calculations are estimates and "
        "not official academic records."
    )
