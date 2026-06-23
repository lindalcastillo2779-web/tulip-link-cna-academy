import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from io import StringIO
import math

st.set_page_config(
    page_title="TULIP-Link & CNA Academy",
    page_icon="🌷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# MOBILE-FIRST STYLE SYSTEM
# =========================================================
st.markdown("""
<style>
:root {
    --bg: #f6f5f1;
    --surface: #fcfbf8;
    --surface-2: #f0ede7;
    --text: #1f2937;
    --muted: #6b7280;
    --primary: #0f766e;
    --primary-dark: #115e59;
    --success: #2e7d32;
    --danger: #b91c1c;
    --danger-soft: #fee2e2;
    --success-soft: #dcfce7;
    --warning: #b45309;
    --border: #d6d3d1;
    --shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
    --radius: 18px;
    --radius-sm: 12px;
}

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    color: var(--text);
}

body {
    background: var(--bg);
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

h1, h2, h3 {
    letter-spacing: -0.02em;
}

.main-title {
    padding: 1rem 1.2rem;
    border-radius: var(--radius);
    background: linear-gradient(135deg, #0f766e 0%, #134e4a 100%);
    color: white;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}

.subtitle {
    font-size: 0.98rem;
    color: #e6fffb;
    margin-top: 0.35rem;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}

.soft-card {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    margin-bottom: 1rem;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    text-align: center;
    box-shadow: var(--shadow);
    min-height: 120px;
}

.kpi {
    font-size: 1.9rem;
    font-weight: 800;
    color: var(--primary);
}

.label {
    color: var(--muted);
    font-size: 0.92rem;
}

.red-critical {
    color: var(--danger);
    font-weight: 800;
}

.green-safe {
    color: var(--success);
    font-weight: 700;
}

.badge {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    font-size: 0.83rem;
    font-weight: 700;
}

.badge-red {
    background: var(--danger-soft);
    color: var(--danger);
}

.badge-green {
    background: var(--success-soft);
    color: var(--success);
}

.flashcard-shell {
    perspective: 1000px;
    margin-bottom: 1rem;
}

.flashcard-front,
.flashcard-back {
    min-height: 220px;
    border-radius: var(--radius);
    padding: 1.2rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.flashcard-front {
    background: linear-gradient(135deg, #ffffff 0%, #f0fdfa 100%);
}

.flashcard-back {
    background: linear-gradient(135deg, #ecfeff 0%, #f8fafc 100%);
}

.check-step {
    padding: 0.7rem 0.8rem;
    border-radius: var(--radius-sm);
    background: #fff;
    border: 1px solid var(--border);
    margin-bottom: 0.45rem;
}

.table-note {
    color: var(--muted);
    font-size: 0.9rem;
}

.facility-board {
    background: linear-gradient(135deg, #fff 0%, #f8fafc 100%);
    border: 1px dashed #94a3b8;
    border-radius: var(--radius);
    padding: 1rem;
}

.small-muted {
    color: var(--muted);
    font-size: 0.88rem;
}

.sms-box {
    background: #111827;
    color: #f9fafb;
    border-radius: var(--radius-sm);
    padding: 0.9rem;
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 0.9rem;
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .main-title {
        padding: 0.9rem;
    }

    .kpi {
        font-size: 1.55rem;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
TODAY = date.today()

def calc_tulip_open_days(expiration_date: date) -> int:
    tulip_open_date = expiration_date - timedelta(days=90)
    return (tulip_open_date - TODAY).days

def days_until_expiration(expiration_date: date) -> int:
    return (expiration_date - TODAY).days

def status_from_expiration(expiration_date: date) -> str:
    days_left = days_until_expiration(expiration_date)
    if days_left <= 90:
        return "RED"
    return "GREEN"

def percent(value, total):
    if total == 0:
        return 0
    return max(0, min(100, int((value / total) * 100)))

def make_download_text(cna_row, facility_row, ceu_summary):
    text = f"""
TEXAS FORM 5506-NAR MOCK PRE-FILL SUMMARY
=========================================

Form Purpose:
Texas Nurse Aide Registry Employment Verification

SECTION 1 – APPLICANT INFORMATION
Applicant Last Name: {cna_row['last_name']}
Applicant First Name: {cna_row['first_name']}
Applicant Middle Name: 
Maiden Name (if applicable): 
Date of Birth: [Mock Placeholder]
Social Security No.: [Protected / Not Stored]
Email Address: [Mock Placeholder]
CNA Certificate No.: {cna_row['license_number']}

Verification of Requirements for Nurse Aide Recertification
- Listed on Employee Misconduct Registry as unemployable?: [Mock Answer Required]
- Criminal offense listed in Texas Health and Safety Code Section 250?: [Mock Answer Required]
- Completed 24 hours of in-service education in past two years?: {"Yes" if ceu_summary['hours'] >= 24 else "No"}
- Completed required annual infection control / PPE training in past 24 months?: [Mock Answer Required]

SECTION 2 – EMPLOYER VERIFICATION
Facility Name: {facility_row['facility_name']}
State License Number: {facility_row['state_license_number']}
Director of Nursing: {facility_row['don_name']}

Employee Verification Summary
Employee Name: {cna_row['first_name']} {cna_row['last_name']}
Phone Number: {cna_row['phone']}
Last Renewal Date: {cna_row['last_renewal_date']}
Expiration Date: {cna_row['expiration_date']}
Total CEU Hours Logged: {ceu_summary['hours']}
Geriatric Training Met: {"Yes" if ceu_summary['geriatric'] else "No"}
Dementia / Alzheimer's Training Met: {"Yes" if ceu_summary['dementia'] else "No"}

DON ACTION ITEMS
- Review employee work eligibility and renewal timing.
- Verify CEU documentation.
- Complete official employer verification and notarization on the official state form.

SYSTEM TIMING
Days Until Expiration: {days_until_expiration(cna_row['expiration_date'])}
Inside 90-Day TULIP Window: {"Yes" if status_from_expiration(cna_row['expiration_date']) == "RED" else "No"}

NOTE
This is a mock data sheet generated by TULIP-Link & CNA Academy for workflow preparation.
Use the official Texas HHSC Form 5506-NAR for actual submission.
"""
    return text.strip()

# =========================================================
# SESSION STATE
# =========================================================
if "flash_index" not in st.session_state:
    st.session_state.flash_index = 0
if "flash_flipped" not in st.session_state:
    st.session_state.flash_flipped = False
if "mastered_cards" not in st.session_state:
    st.session_state.mastered_cards = set()
if "review_cards" not in st.session_state:
    st.session_state.review_cards = set()
if "written_answers" not in st.session_state:
    st.session_state.written_answers = {}
if "skills_answers" not in st.session_state:
    st.session_state.skills_answers = {}
if "skills_checked" not in st.session_state:
    st.session_state.skills_checked = {}
if "selected_cna_id" not in st.session_state:
    st.session_state.selected_cna_id = None

# =========================================================
# MOCK DATA MODEL
# =========================================================
facility_df = pd.DataFrame([
    {
        "facility_id": 1,
        "facility_name": "Bluebonnet Skilled Nursing Center",
        "state_license_number": "TX-NF-44821",
        "don_name": "Monica Alvarez, RN"
    }
])

cna_df = pd.DataFrame([
    {
        "cna_id": 1,
        "first_name": "Jasmine",
        "last_name": "Carter",
        "phone": "(325) 555-0101",
        "license_number": "CNA-TX-102344",
        "last_renewal_date": TODAY - timedelta(days=500),
        "expiration_date": TODAY + timedelta(days=160),
        "user_type": "Active CNA"
    },
    {
        "cna_id": 2,
        "first_name": "Marco",
        "last_name": "Diaz",
        "phone": "(325) 555-0102",
        "license_number": "CNA-TX-204877",
        "last_renewal_date": TODAY - timedelta(days=640),
        "expiration_date": TODAY + timedelta(days=48),
        "user_type": "Critical Window CNA"
    },
    {
        "cna_id": 3,
        "first_name": "Aaliyah",
        "last_name": "Brooks",
        "phone": "(325) 555-0103",
        "license_number": "CNA-TX-318209",
        "last_renewal_date": TODAY - timedelta(days=700),
        "expiration_date": TODAY + timedelta(days=12),
        "user_type": "Critical Window CNA"
    },
    {
        "cna_id": 4,
        "first_name": "Ethan",
        "last_name": "Reed",
        "phone": "(325) 555-0104",
        "license_number": "STUDENT-001",
        "last_renewal_date": TODAY,
        "expiration_date": TODAY + timedelta(days=730),
        "user_type": "Student"
    }
])

ceu_df = pd.DataFrame([
    {"record_id": 1, "cna_id": 1, "course_title": "Resident Safety Essentials", "hours": 8, "geriatric_flag": True, "dementia_flag": False},
    {"record_id": 2, "cna_id": 1, "course_title": "Dementia Communication Basics", "hours": 8, "geriatric_flag": False, "dementia_flag": True},
    {"record_id": 3, "cna_id": 1, "course_title": "Infection Prevention Update", "hours": 10, "geriatric_flag": False, "dementia_flag": False},
    {"record_id": 4, "cna_id": 2, "course_title": "Geriatric Skin Care", "hours": 6, "geriatric_flag": True, "dementia_flag": False},
    {"record_id": 5, "cna_id": 2, "course_title": "Lift & Transfer Safety", "hours": 4, "geriatric_flag": False, "dementia_flag": False},
    {"record_id": 6, "cna_id": 3, "course_title": "Alzheimer's Support Foundations", "hours": 6, "geriatric_flag": False, "dementia_flag": True},
    {"record_id": 7, "cna_id": 3, "course_title": "Resident Rights Refresher", "hours": 5, "geriatric_flag": False, "dementia_flag": False},
])

student_flashcards = [
    {
        "category": "Infection Control",
        "front": "What is the purpose of hand hygiene before and after resident contact?",
        "back": "It reduces transmission of microorganisms and protects both the resident and the caregiver from preventable infection."
    },
    {
        "category": "Resident Rights",
        "front": "What does dignity mean in CNA care?",
        "back": "Treating each resident with respect, privacy, choice, and courtesy during every interaction and care task."
    },
    {
        "category": "Medical Abbreviations",
        "front": "What does 'PRN' mean?",
        "back": "PRN means 'as needed' and is commonly used for medications or care tasks performed only when necessary."
    },
    {
        "category": "Infection Control",
        "front": "What is PPE?",
        "back": "PPE stands for personal protective equipment such as gloves, gowns, masks, and face shields used to reduce exposure risk."
    },
    {
        "category": "Resident Rights",
        "front": "What is informed choice?",
        "back": "Residents have the right to receive information and participate in decisions about their care, routine, and preferences."
    }
]

written_quiz = [
    {
        "q": "Which action best helps prevent the spread of infection?",
        "choices": ["Skipping gloves if hands are clean", "Washing hands before and after care", "Placing dirty linen on the floor", "Sharing personal care items"],
        "answer": "Washing hands before and after care",
        "rationale": "Hand hygiene is a core infection-control practice and helps break the chain of transmission."
    },
    {
        "q": "When speaking with a resident who has hearing loss, the CNA should:",
        "choices": ["Shout from the doorway", "Face the resident and speak clearly", "Talk only to the family", "Rush through instructions"],
        "answer": "Face the resident and speak clearly",
        "rationale": "Clear, direct communication supports understanding and respects the resident."
    },
    {
        "q": "Before assisting with ambulation, the CNA should first:",
        "choices": ["Ask another resident for help", "Lock equipment if used and explain the procedure", "Remove the resident's shoes", "Leave the bed elevated"],
        "answer": "Lock equipment if used and explain the procedure",
        "rationale": "Safety preparation and resident communication come before movement."
    },
    {
        "q": "Which observation should be reported promptly?",
        "choices": ["Resident enjoyed lunch", "Resident slept 8 hours", "New dizziness during transfer", "Resident asked for water"],
        "answer": "New dizziness during transfer",
        "rationale": "A change in condition such as dizziness may indicate risk or acute concern and should be reported."
    },
    {
        "q": "A CNA should document care:",
        "choices": ["Before it is given", "Only if asked later", "After care is completed", "At the end of the month"],
        "answer": "After care is completed",
        "rationale": "Documentation should be accurate and completed after the care or observation occurs."
    }
]

skills_quiz = [
    {
        "q": "Before transferring a resident from bed to wheelchair, which critical step must happen first?",
        "choices": ["Lower side rails after transfer", "Lock bed and wheelchair wheels", "Offer water", "Raise the bed to the highest setting"],
        "answer": "Lock bed and wheelchair wheels",
        "rationale": "Wheel locks are a high-stakes safety element because uncontrolled movement can cause a fall."
    },
    {
        "q": "Before measuring urinary output, the CNA should:",
        "choices": ["Pour urine into the sink", "Discard gloves", "Read the measurement at eye level after collecting it in a graduate", "Estimate the amount by weight"],
        "answer": "Read the measurement at eye level after collecting it in a graduate",
        "rationale": "Eye-level reading improves accuracy and supports proper recording."
    },
    {
        "q": "During handwashing, which step is essential?",
        "choices": ["Use cold water only", "Keep fingertips pointed down and avoid touching inside sink", "Dry hands on uniform", "Skip soap if rushed"],
        "answer": "Keep fingertips pointed down and avoid touching inside sink",
        "rationale": "This reduces contamination during the handwashing skill."
    }
]

clinical_skills = {
    "Handwashing": [
        "Wet hands and wrists thoroughly under warm running water.",
        "Apply soap.",
        "Rub hands together vigorously for at least 20 seconds, cleaning all surfaces.",
        "Clean under fingernails by rubbing fingertips against palm.",
        "Rinse with fingertips pointed downward.",
        "Dry hands with clean paper towel.",
        "Use dry paper towel to turn off faucet.",
        "CRITICAL SAFETY STEP: Do not contaminate clean hands by touching sink or faucet directly."
    ],
    "Measuring & Recording Blood Pressure": [
        "Identify the resident and explain the procedure.",
        "Position resident comfortably with arm supported at heart level.",
        "Apply cuff snugly to bare upper arm.",
        "Place stethoscope correctly over brachial artery.",
        "Inflate cuff and slowly deflate while listening.",
        "Record systolic and diastolic reading accurately.",
        "CRITICAL SAFETY STEP: Report abnormal reading according to facility instructions."
    ],
    "Measuring & Recording Urinary Output": [
        "Provide privacy and explain the procedure.",
        "Put on gloves before handling urine collection device.",
        "Pour urine into graduate without spilling.",
        "Read measurement at eye level.",
        "Empty graduate and clean equipment per instructions.",
        "Remove gloves and perform hand hygiene.",
        "Record the exact amount.",
        "CRITICAL SAFETY STEP: Avoid contamination and record the actual measured amount, not an estimate."
    ]
}

# =========================================================
# TOP HEADER
# =========================================================
st.markdown("""
<div class="main-title">
    <h1>🌷 TULIP-Link & CNA Academy</h1>
    <div class="subtitle">Mobile-first Texas CNA study, renewal, and DON compliance workspace</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# NAVIGATION
# =========================================================
with st.sidebar:
    st.header("Navigation")
    app_view = st.radio(
        "Choose your path",
        [
            "View A: CNA Study Academy",
            "View B: CNA Renewal Hub",
            "View C: DON & Facility Dashboard"
        ]
    )
    st.markdown("---")
    st.caption("Designed for students, active CNAs, and Texas facility leaders.")

# =========================================================
# VIEW A: STUDY ACADEMY
# =========================================================
if app_view == "View A: CNA Study Academy":
    st.subheader("Pre-Certification Academy")

    total_flashcards = len(student_flashcards)
    mastered_count = len(st.session_state.mastered_cards)
    review_count = len(st.session_state.review_cards)

    written_score = 0
    if len(st.session_state.written_answers) == len(written_quiz):
        written_score = sum(
            1 for i, q in enumerate(written_quiz)
            if st.session_state.written_answers.get(i) == q["answer"]
        )

    skills_score = 0
    if len(st.session_state.skills_answers) == len(skills_quiz):
        skills_score = sum(
            1 for i, q in enumerate(skills_quiz)
            if st.session_state.skills_answers.get(i) == q["answer"]
        )

    readiness_points = mastered_count + written_score + skills_score
    readiness_total = total_flashcards + len(written_quiz) + len(skills_quiz)
    readiness_pct = percent(readiness_points, readiness_total)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="kpi">{mastered_count}/{total_flashcards}</div><div class="label">Flashcards Mastered</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="kpi">{written_score}/{len(written_quiz)}</div><div class="label">Written Quiz Score</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="kpi">{skills_score}/{len(skills_quiz)}</div><div class="label">Skills Quiz Score</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Test Readiness Progress")
    st.progress(readiness_pct / 100)
    st.write(f"Current readiness: **{readiness_pct}%**")
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Flashcards",
        "Written Quiz",
        "Clinical Skills Checklists",
        "Skills Quiz"
    ])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Interactive Flashcards")

        current_card = student_flashcards[st.session_state.flash_index]
        st.caption(f"Card {st.session_state.flash_index + 1} of {len(student_flashcards)} • {current_card['category']}")

        if not st.session_state.flash_flipped:
            st.markdown(
                f"""
                <div class="flashcard-shell">
                    <div class="flashcard-front">
                        <h3>{current_card['category']}</h3>
                        <p style="font-size:1.1rem; margin-top:0.8rem;">{current_card['front']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="flashcard-shell">
                    <div class="flashcard-back">
                        <h3>Answer</h3>
                        <p style="font-size:1.05rem; margin-top:0.8rem;">{current_card['back']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            if st.button("⬅ Previous", use_container_width=True):
                st.session_state.flash_index = (st.session_state.flash_index - 1) % len(student_flashcards)
                st.session_state.flash_flipped = False
                st.rerun()
        with c2:
            if st.button("Flip Card", use_container_width=True):
                st.session_state.flash_flipped = not st.session_state.flash_flipped
                st.rerun()
        with c3:
            if st.button("Mastered", use_container_width=True):
                st.session_state.mastered_cards.add(st.session_state.flash_index)
                if st.session_state.flash_index in st.session_state.review_cards:
                    st.session_state.review_cards.remove(st.session_state.flash_index)
                st.success("Marked as mastered.")
        with c4:
            if st.button("Needs Review", use_container_width=True):
                st.session_state.review_cards.add(st.session_state.flash_index)
                if st.session_state.flash_index in st.session_state.mastered_cards:
                    st.session_state.mastered_cards.remove(st.session_state.flash_index)
                st.warning("Marked for review.")
        with c5:
            if st.button("Next ➡", use_container_width=True):
                st.session_state.flash_index = (st.session_state.flash_index + 1) % len(student_flashcards)
                st.session_state.flash_flipped = False
                st.rerun()

        st.write(f"Mastered cards: **{len(st.session_state.mastered_cards)}** | Needs review: **{len(st.session_state.review_cards)}**")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Written Practice Quiz")
        st.write("Choose the best answer. Feedback appears immediately after each selection.")

        for i, item in enumerate(written_quiz):
            st.markdown(f"**Q{i+1}. {item['q']}**")
            answer = st.radio(
                f"Select answer for Q{i+1}",
                item["choices"],
                key=f"written_q_{i}",
                index=None
            )
            if answer:
                st.session_state.written_answers[i] = answer
                if answer == item["answer"]:
                    st.success(f"Correct. {item['rationale']}")
                else:
                    st.error(f"Not quite. Correct answer: {item['answer']}. {item['rationale']}")
            st.markdown("---")

        if len(st.session_state.written_answers) == len(written_quiz):
            score = sum(
                1 for i, q in enumerate(written_quiz)
                if st.session_state.written_answers.get(i) == q["answer"]
            )
            st.info(f"Written quiz score: {score}/{len(written_quiz)}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Clinical Skills Checklists")
        chosen_skill = st.selectbox("Select a clinical skill", list(clinical_skills.keys()))

        for idx, step in enumerate(clinical_skills[chosen_skill]):
            key = f"{chosen_skill}_{idx}"
            is_critical = "CRITICAL SAFETY STEP" in step
            cols = st.columns([0.08, 0.92])
            with cols[0]:
                checked = st.checkbox("", key=key)
                st.session_state.skills_checked[key] = checked
            with cols[1]:
                if is_critical:
                    st.markdown(f'<div class="check-step"><span class="red-critical">{step}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="check-step">{step}</div>', unsafe_allow_html=True)

        completed_steps = sum(
            1 for idx, _ in enumerate(clinical_skills[chosen_skill])
            if st.session_state.skills_checked.get(f"{chosen_skill}_{idx}", False)
        )
        st.write(f"Checklist completion: **{completed_steps}/{len(clinical_skills[chosen_skill])}**")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Scenario-Based Skills Quiz")

        for i, item in enumerate(skills_quiz):
            st.markdown(f"**Q{i+1}. {item['q']}**")
            answer = st.radio(
                f"Select skills answer for Q{i+1}",
                item["choices"],
                key=f"skills_q_{i}",
                index=None
            )
            if answer:
                st.session_state.skills_answers[i] = answer
                if answer == item["answer"]:
                    st.success(f"Correct. {item['rationale']}")
                else:
                    st.error(f"Incorrect. Correct answer: {item['answer']}. {item['rationale']}")
            st.markdown("---")

        if len(st.session_state.skills_answers) == len(skills_quiz):
            score = sum(
                1 for i, q in enumerate(skills_quiz)
                if st.session_state.skills_answers.get(i) == q["answer"]
            )
            st.info(f"Skills quiz score: {score}/{len(skills_quiz)}")
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# VIEW B: RENEWAL HUB
# =========================================================
elif app_view == "View B: CNA Renewal Hub":
    st.subheader("Post-Certification Renewal Hub")

    cna_options = cna_df[cna_df["user_type"] != "Student"].copy()
    cna_options["display"] = cna_options["first_name"] + " " + cna_options["last_name"] + " • " + cna_options["license_number"]
    selected_display = st.selectbox("Select CNA profile", cna_options["display"].tolist())
    selected_row = cna_options[cna_options["display"] == selected_display].iloc[0]

    records = ceu_df[ceu_df["cna_id"] == selected_row["cna_id"]]
    total_hours = int(records["hours"].sum()) if not records.empty else 0
    geriatric_met = bool(records["geriatric_flag"].any()) if not records.empty else False
    dementia_met = bool(records["dementia_flag"].any()) if not records.empty else False
    hours_pct = percent(total_hours, 24)
    days_to_open = calc_tulip_open_days(selected_row["expiration_date"])
    days_left = days_until_expiration(selected_row["expiration_date"])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="kpi">{total_hours}/24</div><div class="label">In-Service Hours</div></div>', unsafe_allow_html=True)
    with c2:
        status_label = "OPEN" if days_to_open <= 0 else "NOT OPEN"
        st.markdown(f'<div class="metric-card"><div class="kpi">{status_label}</div><div class="label">TULIP Window</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="kpi">{days_left}</div><div class="label">Days Until Expiration</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Personal Compliance Dashboard")
    st.write(f"**CNA:** {selected_row['first_name']} {selected_row['last_name']}")
    st.write(f"**License Number:** {selected_row['license_number']}")
    st.write(f"**Expiration Date:** {selected_row['expiration_date']}")
    st.progress(hours_pct / 100)
    st.write(f"Education progress: **{hours_pct}%** of the 24-hour target")

    g_col, d_col = st.columns(2)
    with g_col:
        if geriatric_met:
            st.success("Geriatric credit recorded")
        else:
            st.error("Geriatric credit not yet recorded")
    with d_col:
        if dementia_met:
            st.success("Dementia / Alzheimer's credit recorded")
        else:
            st.error("Dementia / Alzheimer's credit not yet recorded")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 3-Month TULIP Application Window Countdown")

    if days_to_open > 0:
        st.info(f"Your TULIP renewal window opens in **{days_to_open} days**.")
    elif days_to_open == 0:
        st.success("Your TULIP renewal window opens **today**.")
    else:
        st.warning(f"Your TULIP renewal window is already open and opened **{abs(days_to_open)} days ago**.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Recommended Texas CEU Courses")
    st.write("Sponsored placement area for approved continuing education providers.")
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        st.markdown('<div class="soft-card"><strong>Geriatric Care Update</strong><br><span class="small-muted">8 hours • Sponsored placeholder • Texas-approved listing space</span></div>', unsafe_allow_html=True)
    with rc2:
        st.markdown('<div class="soft-card"><strong>Dementia & Alzheimer’s Care</strong><br><span class="small-muted">8 hours • Sponsored placeholder • Texas-approved listing space</span></div>', unsafe_allow_html=True)
    with rc3:
        st.markdown('<div class="soft-card"><strong>Infection Control Refresher</strong><br><span class="small-muted">8 hours • Sponsored placeholder • Texas-approved listing space</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Logged CEU Records")
    if records.empty:
        st.warning("No CEU records found for this CNA.")
    else:
        display_records = records.rename(columns={
            "course_title": "Course Title",
            "hours": "Hours",
            "geriatric_flag": "Geriatric",
            "dementia_flag": "Dementia/Alzheimer's"
        })[["Course Title", "Hours", "Geriatric", "Dementia/Alzheimer's"]]
        st.dataframe(display_records, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# VIEW C: DON DASHBOARD
# =========================================================
elif app_view == "View C: DON & Facility Dashboard":
    st.subheader("DON & Facility Dashboard")

    facility = facility_df.iloc[0]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"**Facility:** {facility['facility_name']}")
    st.write(f"**State License Number:** {facility['state_license_number']}")
    st.write(f"**Director of Nursing:** {facility['don_name']}")
    st.markdown('</div>', unsafe_allow_html=True)

    active_cnas = cna_df[cna_df["user_type"] != "Student"].copy()

    matrix_rows = []
    for _, row in active_cnas.iterrows():
        recs = ceu_df[ceu_df["cna_id"] == row["cna_id"]]
        hrs = int(recs["hours"].sum()) if not recs.empty else 0
        days_left = days_until_expiration(row["expiration_date"])
        status = status_from_expiration(row["expiration_date"])
        matrix_rows.append({
            "CNA ID": row["cna_id"],
            "First Name": row["first_name"],
            "Last Name": row["last_name"],
            "License Number": row["license_number"],
            "Days Until Expiration": days_left,
            "CEU Hours Completed": hrs,
            "Status": status
        })

    matrix_df = pd.DataFrame(matrix_rows)

    status_filter = st.segmented_control(
        "Filter by urgency",
        ["ALL", "GREEN", "RED"],
        default="ALL"
    )

    filtered_df = matrix_df.copy()
    if status_filter != "ALL":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    def highlight_status(row):
        color = "#dcfce7" if row["Status"] == "GREEN" else "#fee2e2"
        return [f"background-color: {color}"] * len(row)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### TULIP Readiness Staff Matrix")
    st.caption("GREEN = more than 90 days to expiration • RED = inside 90-day TULIP renewal window")
    st.dataframe(
        filtered_df.style.apply(highlight_status, axis=1),
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Administrative Actions")

    red_cnas = matrix_df[matrix_df["Status"] == "RED"]
    if red_cnas.empty:
        st.success("No CNAs are currently inside the 90-day TULIP window.")
    else:
        options = red_cnas.apply(
            lambda x: f"{x['First Name']} {x['Last Name']} • {x['License Number']} • {x['Days Until Expiration']} days left",
            axis=1
        ).tolist()
        selected_staff = st.selectbox("Select CNA in RED renewal window", options)

        chosen = red_cnas.iloc[options.index(selected_staff)]
        chosen_cna = cna_df[cna_df["cna_id"] == chosen["CNA ID"]].iloc[0]
        chosen_recs = ceu_df[ceu_df["cna_id"] == chosen_cna["cna_id"]]

        ceu_summary = {
            "hours": int(chosen_recs["hours"].sum()) if not chosen_recs.empty else 0,
            "geriatric": bool(chosen_recs["geriatric_flag"].any()) if not chosen_recs.empty else False,
            "dementia": bool(chosen_recs["dementia_flag"].any()) if not chosen_recs.empty else False
        }

        a1, a2 = st.columns(2)

        with a1:
            if st.button("Pre-fill Form 5506-NAR", use_container_width=True):
                summary_text = make_download_text(chosen_cna, facility, ceu_summary)
                st.success("Mock 5506-NAR data sheet generated.")
                st.download_button(
                    label="Download 5506-NAR Mock Summary",
                    data=summary_text,
                    file_name=f"5506-NAR-{chosen_cna['last_name']}-{chosen_cna['first_name']}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

                st.text_area(
                    "Preview",
                    summary_text,
                    height=360
                )

        with a2:
            if st.button("Mock Twilio SMS Trigger", use_container_width=True):
                sms_payload = (
                    f"Hi {chosen_cna['first_name']}, your 3-month Texas TULIP window is OPEN. "
                    f"Your Form 5506-NAR is pre-filled and waiting on the DON desk."
                )
                st.info("Mock SMS fired successfully.")
                st.markdown(
                    f'<div class="sms-box">{sms_payload}</div>',
                    unsafe_allow_html=True
                )

        st.markdown("#### Selected CNA Snapshot")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(f'<span class="badge badge-red">Days Left: {days_until_expiration(chosen_cna["expiration_date"])}</span>', unsafe_allow_html=True)
        with s2:
            st.markdown(f'<span class="badge badge-red">CEU Hours: {ceu_summary["hours"]}/24</span>', unsafe_allow_html=True)
        with s3:
            flags = []
            flags.append("Geriatric ✔" if ceu_summary["geriatric"] else "Geriatric ✘")
            flags.append("Dementia ✔" if ceu_summary["dementia"] else "Dementia ✘")
            st.markdown(f'<span class="badge badge-red">{" | ".join(flags)}</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="facility-board">', unsafe_allow_html=True)
    st.markdown("### Facility Career Board")
    st.write("Free-community sustainability area for facility job postings and sponsored recruitment visibility.")
    st.write("- Weekend CNA openings")
    st.write("- Medication aide crossover pathways")
    st.write("- Night-shift differential opportunities")
    st.write("- DON-sponsored tuition and test-prep support")
    st.markdown('<div class="table-note">This placeholder demonstrates how the platform can remain free through targeted facility hiring placements.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption(
    "Educational demo application for local testing. Verify official Texas HHSC, TULIP, Prometric, and employer requirements before real-world use."
)
