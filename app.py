import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime
from pathlib import Path
from lesson_assets import chapter_thumbnail_from_title, chapter_video_from_module, lesson_icon_from_title
from modules import (
    get_all_chapters, get_module, count_total_questions, VIDEO_SCRIPT_TEMPLATES, CASE_STUDIES,
    CEU_COURSE_LIBRARY, ACTIVE_LICENSE_RENEWAL_STEPS, EXPIRED_LICENSE_REACTIVATION_STEPS,
    TULIP_INFORMATION, RENEWAL_READINESS_CHECKLIST, PROFESSIONAL_RECOMMENDATIONS
)

st.set_page_config(
    page_title="TULIP-Link CNA Academy",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "ui_theme" not in st.session_state:
    st.session_state.ui_theme = "light"

# =========================================================
# STYLES
# =========================================================
st.markdown("""
<style>
:root{
    --bg:#ffffff;
    --surface:#ffffff;
    --surface-2:#f9fafb;
    --surface-3:#f3f4f6;
    --text:#000000;
    --muted:#000000;
    --primary:#0f766e;
    --primary-dark:#134e4a;
    --border:#d1d5db;
    --success:#166534;
    --success-soft:#dcfce7;
    --danger:#b91c1c;
    --danger-soft:#fee2e2;
    --warning:#b45309;
    --warning-soft:#ffedd5;
    --info:#075985;
    --info-soft:#e0f2fe;
    --shadow:0 10px 24px rgba(15,23,42,.08);
    --radius:18px;
    --radius-sm:12px;
}
html, body, [class*="css"] {
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
    color:var(--text);
}
body { background:var(--bg); }
[data-testid="stAppViewContainer"] {
    background:var(--bg) !important;
}
[data-testid="stMainBlockContainer"] {
    background:var(--bg) !important;
}
.stApp {
    background:var(--bg) !important;
}
[data-testid="stSidebar"] {
    background:var(--bg) !important;
}
[data-testid="stSidebarContent"] {
    background:var(--bg) !important;
}
.block-container {
    padding-top:1rem;
    padding-bottom:4rem;
    max-width:1280px;
}
.main-hero{
    background:linear-gradient(135deg,var(--primary) 0%,var(--primary-dark) 100%);
    color:#000000;
    border-radius:var(--radius);
    padding:1.2rem 1.2rem;
    box-shadow:var(--shadow);
    margin-bottom:1rem;
}
.card{
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem;
    box-shadow:var(--shadow);
    margin-bottom:1rem;
    transition:transform .18s ease, box-shadow .18s ease;
}
.card:hover{
    transform:translateY(-2px);
    box-shadow:0 14px 30px rgba(15,23,42,.12);
}
.soft-card{
    background:var(--surface-2);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem;
    margin-bottom:1rem;
}
.info-card{
    background:var(--surface-3);
    border:1px solid #bae6fd;
    border-radius:var(--radius);
    padding:1rem;
    margin-bottom:1rem;
}
.metric-card{
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem;
    box-shadow:var(--shadow);
    text-align:center;
    min-height:122px;
}
.kpi{
    color:#000000;
    font-size:1.85rem;
    font-weight:800;
}
.label{
    color:#000000;
    font-size:.92rem;
}
.badge{
    display:inline-block;
    padding:.34rem .72rem;
    border-radius:999px;
    font-size:.82rem;
    font-weight:700;
}
.badge-green{background:var(--success-soft);color:#000000;}
.badge-red{background:var(--danger-soft);color:#000000;}
.badge-amber{background:var(--warning-soft);color:#000000;}
.badge-blue{background:var(--info-soft);color:#000000;}
.critical{
    color:#000000;
    font-weight:800;
}
.check-step{
    background:#fff;
    border:1px solid var(--border);
    border-radius:var(--radius-sm);
    padding:.75rem .85rem;
    margin-bottom:.45rem;
}
.sms-box{
    background:#e5e7eb;
    color:#000000;
    border-radius:var(--radius-sm);
    padding:.95rem;
    font-family:Consolas,monospace;
    font-size:.9rem;
}
.footer-note{
    color:#000000;
    font-size:.9rem;
}
.small-muted{
    color:#000000;
    font-size:.88rem;
}
.study-hero{
    background:linear-gradient(135deg,#ecfeff 0%, #f0f9ff 100%);
    border:1px solid #bae6fd;
    border-radius:var(--radius);
    padding:1rem;
    margin-bottom:1rem;
}
.lesson-card{
    background:#fff;
    border:1px solid var(--border);
    border-left:4px solid #94a3b8;
    border-radius:var(--radius-sm);
    padding:.75rem .85rem;
    margin-bottom:.55rem;
    animation:lessonReveal .34s ease both;
}
.lesson-card.complete{
    border-left-color:#16a34a;
    background:#f0fdf4;
}
.lesson-card.pending{
    border-left-color:#0ea5e9;
}
.lesson-card.active{
    border-left-color:#0f766e;
    box-shadow:0 0 0 1px rgba(15,118,110,.22);
    background:#f0fdfa;
}
.lesson-title{
    font-weight:700;
    color:#000000;
    margin-bottom:.2rem;
}
.lesson-meta{
    color:#000000;
    font-size:.86rem;
}
.lesson-chip{
    display:inline-block;
    padding:.18rem .5rem;
    border-radius:999px;
    font-size:.77rem;
    font-weight:700;
    margin-right:.3rem;
}
.lesson-chip.done{background:#dcfce7;color:#000000;}
.lesson-chip.todo{background:#e0f2fe;color:#000000;}
.mini-progress-track{
    margin-top:.45rem;
    width:100%;
    height:8px;
    background:#e2e8f0;
    border-radius:999px;
    overflow:hidden;
}
.mini-progress-fill{
    height:100%;
    background:linear-gradient(90deg,#0ea5e9 0%, #0f766e 100%);
    border-radius:999px;
}
.visual-banner{
    background:linear-gradient(120deg,#f8fafc 0%, #ecfeff 48%, #f0fdf4 100%);
    border:1px solid #bae6fd;
    border-radius:var(--radius);
    padding:1rem;
    margin-bottom:1rem;
}
.visual-badge{
    display:inline-block;
    margin:.2rem .35rem .2rem 0;
    padding:.25rem .55rem;
    border-radius:999px;
    font-size:.78rem;
    font-weight:700;
    background:#cffafe;
    color:#000000;
}
.sticky-study-header{
    position:sticky;
    top:12px;
    z-index:8;
    background:linear-gradient(120deg,#ecfeff 0%, #f0fdf4 100%);
    border:1px solid #99f6e4;
    border-radius:var(--radius-sm);
    padding:.75rem .85rem;
    margin-bottom:.7rem;
    box-shadow:0 8px 20px rgba(15,23,42,.10);
}
.chapter-thumbnail{
    border-radius:var(--radius-sm);
    border:1px solid #cbd5e1;
    overflow:hidden;
    margin-bottom:.8rem;
}
.crumbs{
    color:#000000;
    font-size:.84rem;
    margin-bottom:.45rem;
}
.action-rail{
    position:sticky;
    top:12px;
    background:#f8fafc;
    border:1px solid #cbd5e1;
    border-radius:var(--radius-sm);
    padding:.85rem;
    box-shadow:var(--shadow);
}
.rec-card{
    background:#fff;
    border:1px solid #cbd5e1;
    border-radius:var(--radius-sm);
    padding:.7rem;
    min-height:140px;
}
.st-key-flashcard_touch button{
    background:#ffffff;
    border:1px solid var(--border);
    color:#111827;
    border-radius:var(--radius-sm);
    padding:1rem;
    min-height:170px;
    text-align:left;
    white-space:pre-wrap;
    line-height:1.45;
    font-weight:600;
    transform-style:preserve-3d;
    animation:flashFlipIn .35s ease;
}
.st-key-flashcard_touch button:hover{
    border-color:#0f766e;
    box-shadow:0 0 0 1px rgba(15,118,110,.2);
}
.st-key-flashcard_touch button p,
.st-key-flashcard_touch button span,
.st-key-flashcard_touch button div{
    color:#111827 !important;
}
.flashcard-state{
    color:#000000;
    font-size:.82rem;
    margin:.35rem 0 .55rem 0;
}
.welcome-login{
    display:grid;
    grid-template-columns:1.1fr .9fr;
    gap:1rem;
    align-items:center;
}
.welcome-copy h2{
    margin:.1rem 0 .5rem 0;
    color:#000000;
}
.welcome-copy p{
    margin:.2rem 0;
    color:#000000;
    font-size:1.03rem;
    line-height:1.55;
}
.welcome-note{
    margin-top:.55rem;
    background:#f0f9ff;
    border:1px solid #bae6fd;
    border-radius:12px;
    padding:.7rem .8rem;
    font-weight:700;
    color:#000000;
}
.cna-carousel{
    position:relative;
    height:285px;
    border-radius:14px;
    overflow:hidden;
    border:1px solid #cbd5e1;
    background:#ffffff;
}
.cna-carousel img{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit:cover;
    opacity:0;
    animation:carouselFade 25s infinite;
}
.cna-carousel img:nth-child(1){animation-delay:0s;}
.cna-carousel img:nth-child(2){animation-delay:5s;}
.cna-carousel img:nth-child(3){animation-delay:10s;}
.cna-carousel img:nth-child(4){animation-delay:15s;}
.cna-carousel img:nth-child(5){animation-delay:20s;}
@keyframes carouselFade{
    0%, 16% {opacity:1;}
    20%, 100% {opacity:0;}
}
@keyframes lessonReveal{
    from{opacity:0; transform:translateY(6px);}
    to{opacity:1; transform:translateY(0);}
}
@keyframes flashFlipIn{
    0%{opacity:.3; transform:rotateY(-90deg) scale(.98);}
    100%{opacity:1; transform:rotateY(0deg) scale(1);}
}
div[data-testid="stDataFrame"]{
    border:1px solid var(--border);
    border-radius:var(--radius);
    overflow:hidden;
}

/* Keep all UI copy readable by default, including checklists and quiz labels. */
.stApp,
.stApp p,
.stApp li,
.stApp span,
.stApp label,
.stApp .stMarkdown,
.stApp .stCaption,
.stApp .stRadio label,
.stApp .stCheckbox label,
.stApp .stToggle label,
.stApp .stSelectbox label,
.stApp .stMultiSelect label,
.stApp .stTextInput label,
.stApp .stTextArea label,
.stApp .stNumberInput label,
.stApp .stDateInput label,
.stApp .stTimeInput label,
.stApp .stSlider label,
.stApp th,
.stApp td {
    color:#000000 !important;
}
@media (max-width:768px){
    .block-container{padding-left:.8rem;padding-right:.8rem;}
    .kpi{font-size:1.45rem;}
    .welcome-login{grid-template-columns:1fr;}
    .cna-carousel{height:240px;}
}
/* Tab button styling */
[role="tab"] {
    border: 3px solid #000000 !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    padding: 0.65rem 1.2rem !important;
    margin-right: 0.5rem !important;
}
[role="tab"][aria-selected="true"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}
[role="tab"][aria-selected="false"] {
    background-color: #ffffff !important;
    color: #000000 !important;
}
[role="tab"]:hover {
    background-color: #f0f0f0 !important;
}
</style>
""", unsafe_allow_html=True)

if st.session_state.ui_theme == "glass":
    st.markdown("""
<style>
:root{
    --bg:#ffffff;
    --surface:rgba(255,255,255,.95);
    --surface-2:rgba(255,255,255,.82);
    --surface-3:rgba(236,254,255,.88);
    --text:#000000;
    --muted:#000000;
    --primary:#22d3ee;
    --primary-dark:#0891b2;
    --border:rgba(148,163,184,.32);
    --success:#86efac;
    --warning:#fde047;
    --danger:#fca5a5;
    --info:#7dd3fc;
}
.card, .soft-card, .info-card, .metric-card, .study-hero, .lesson-card, .visual-banner, .sticky-study-header {
    backdrop-filter:blur(10px);
}
.lesson-title{ color:#000000; }
.main-hero{ background:linear-gradient(135deg,#cffafe 0%, #e0f2fe 100%); }
.action-rail{ background:rgba(255,255,255,.82); border-color:rgba(148,163,184,.34); }
.rec-card{ background:rgba(255,255,255,.85); border-color:rgba(148,163,184,.34); }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
TODAY = date.today()

def pct(value, total):
    if total == 0:
        return 0
    return max(0, min(100, int((value / total) * 100)))

def days_until_expiration(expiration_date: date):
    return (expiration_date - TODAY).days

def tulip_window_open_date(expiration_date: date):
    return expiration_date - timedelta(days=90)

def days_until_tulip_window(expiration_date: date):
    return (tulip_window_open_date(expiration_date) - TODAY).days

def status_from_expiration(expiration_date: date):
    return "RED" if days_until_expiration(expiration_date) <= 90 else "GREEN"

def compliance_snapshot(cna_id, expiration_date, ceu_records):
    recs = ceu_records[ceu_records["cna_id"] == cna_id]
    hours = int(recs["hours"].sum()) if not recs.empty else 0
    geriatric = bool(recs["geriatric_flag"].any()) if not recs.empty else False
    dementia = bool(recs["dementia_flag"].any()) if not recs.empty else False
    infection = bool(recs["infection_flag"].any()) if not recs.empty else False
    days_left = days_until_expiration(expiration_date)
    tulip_days = days_until_tulip_window(expiration_date)
    return {
        "hours": hours,
        "geriatric": geriatric,
        "dementia": dementia,
        "infection": infection,
        "days_left": days_left,
        "tulip_days": tulip_days
    }

def readiness_score(summary):
    score = 0
    if summary["hours"] >= 24:
        score += 35
    else:
        score += int((summary["hours"] / 24) * 35)
    if summary["geriatric"]:
        score += 15
    if summary["dementia"]:
        score += 15
    if summary["infection"]:
        score += 15
    if summary["days_left"] > 90:
        score += 20
    elif summary["days_left"] > 0:
        score += 10
    else:
        score += 0
    return max(0, min(100, score))

def missing_items(summary):
    items = []
    if summary["hours"] < 24:
        items.append(f"Complete {24 - summary['hours']} more in-service hours")
    if not summary["geriatric"]:
        items.append("Add geriatrics-related training record")
    if not summary["dementia"]:
        items.append("Add dementia / Alzheimer's-related training record")
    if not summary["infection"]:
        items.append("Confirm annual infection-control training")
    if summary["days_left"] <= 90:
        items.append("Begin or finish TULIP renewal submission now")
    else:
        items.append("Monitor countdown until 90-day TULIP window opens")
    return items

texas_ceu_requirements = [
    {
        "Requirement": "24 hours of in-service education",
        "Detail": "Required every 24 months for CNA renewal",
        "Notes": "Includes general nursing assistant topics and state-approved training"
    },
    {
        "Requirement": "Geriatrics training",
        "Detail": "Required category content",
        "Notes": "At least one course or contact hour in geriatric care"
    },
    {
        "Requirement": "Dementia / Alzheimer's training",
        "Detail": "Required category content",
        "Notes": "At least one course or contact hour in dementia care"
    },
    {
        "Requirement": "Annual infection-control training",
        "Detail": "Required each year for renewal",
        "Notes": "Must include Texas-specific infection prevention and safety"
    },
    {
        "Requirement": "TULIP renewal window readiness",
        "Detail": "Begins 90 days before license expiration",
        "Notes": "Submit renewal during the open TULIP window"
    },
    {
        "Requirement": "Employer verification support",
        "Detail": "Form 5506-NAR if required by your employer",
        "Notes": "Keep employer and facility verification information ready"
    }
]

def ceu_requirement_status(summary):
    return [
        {
            "Requirement": "24 in-service hours",
            "Status": "Complete" if summary["hours"] >= 24 else "Pending",
            "Progress": f"{summary['hours']}/24 hours"
        },
        {
            "Requirement": "Geriatrics training",
            "Status": "Complete" if summary["geriatric"] else "Pending",
            "Progress": "Recorded" if summary["geriatric"] else "Missing"
        },
        {
            "Requirement": "Dementia / Alzheimer's training",
            "Status": "Complete" if summary["dementia"] else "Pending",
            "Progress": "Recorded" if summary["dementia"] else "Missing"
        },
        {
            "Requirement": "Annual infection-control training",
            "Status": "Complete" if summary["infection"] else "Pending",
            "Progress": "Recorded" if summary["infection"] else "Missing"
        },
        {
            "Requirement": "TULIP window readiness",
            "Status": "Open" if summary["tulip_days"] <= 0 else "Not open yet",
            "Progress": f"{summary['tulip_days']} days until window" if summary["tulip_days"] > 0 else "Window open"
        }
    ]

def make_5506_text(cna_row, facility_row, summary):
    return f"""
TEXAS FORM 5506-NAR MOCK PRE-FILL SUMMARY
=========================================

Form Purpose:
Texas Nurse Aide Registry Employment Verification

APPLICANT INFORMATION
Last Name: {cna_row['last_name']}
First Name: {cna_row['first_name']}
Middle Name:
Maiden Name:
Date of Birth: [Add manually]
Social Security Number: [Do not store in demo]
Email Address: [Add manually]
CNA Certificate Number: {cna_row['license_number']}
Phone Number: {cna_row['phone']}

EMPLOYER INFORMATION
Facility Name: {facility_row['facility_name']}
State License Number: {facility_row['state_license_number']}
Director of Nursing: {facility_row['don_name']}

RENEWAL SUPPORT SNAPSHOT
Last Renewal Date: {cna_row['last_renewal_date']}
Expiration Date: {cna_row['expiration_date']}
Days Until Expiration: {summary['days_left']}
TULIP Window Opens / Opened: {summary['tulip_days']} days from today (negative means already open)
Total In-Service Hours Logged: {summary['hours']}
Geriatrics Training Recorded: {"Yes" if summary["geriatric"] else "No"}
Dementia / Alzheimer's Training Recorded: {"Yes" if summary["dementia"] else "No"}
Annual Infection-Control Training Recorded: {"Yes" if summary["infection"] else "No"}

DON ACTIONS
- Verify employment and identity fields.
- Confirm in-service records and required topic coverage.
- Review timing of renewal activity in TULIP.
- Complete the official state form workflow as required.

NOTE
This is a workflow aid generated by CNA & TULIP-Link - Texas CNA Academy.
Use official Texas HHSC forms and TULIP for real submission.
""".strip()

# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "flash_index": 0,
    "flash_flip": False,
    "flash_category": "All Categories",
    "flash_category_prev": "All Categories",
    "mastered_cards": set(),
    "review_cards": set(),
    "written_answers": {},
    "skills_answers": {},
    "skills_checks": {},
    "chapter_quiz_answers": {},
    "chapter_progress": {},
    "quiz_history": {"written": [], "skills": []},
    "written_timer_started_at": None,
    "skills_timer_started_at": None,
    "written_quiz_log_done": False,
    "skills_quiz_log_done": False,
    "last_selected_chapter": None,
    # CEU & TULIP renewal tracking
    "license_status": "Active",  # "Active" or "Expired"
    "selected_ceus": [],  # Track selected CEU courses
    "ceu_completion_tracking": {},  # Track hours by category
    "renewal_checklist_items": {},  # Track checklist completion
    "renewal_step_expanded": {},  # Track expanded renewal steps
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


@st.cache_data(show_spinner=False)
def load_markdown_content(file_path):
    chapter_path = Path(__file__).resolve().parent / file_path
    try:
        return chapter_path.read_text(encoding="utf-8")
    except Exception as exc:
        return f"Unable to load chapter file: {exc}"


def update_chapter_progress(chapter_key, complete):
    progress = st.session_state.chapter_progress.copy()
    progress[chapter_key] = complete
    st.session_state.chapter_progress = progress


def chapter_progress_summary():
    total = len(get_all_chapters())
    complete = sum(1 for completed in st.session_state.chapter_progress.values() if completed)
    return complete, total


def format_duration(total_seconds):
    mins = total_seconds // 60
    secs = total_seconds % 60
    return f"{mins:02d}:{secs:02d}"


def chapter_quiz_percent(title, module_info):
    quiz = module_info.get("quiz", [])
    if not quiz:
        return 100
    answers = st.session_state.chapter_quiz_answers.get(title, {})
    if len(answers) < len(quiz):
        return 0
    correct = sum(1 for i, item in enumerate(quiz) if answers.get(i) == item["answer"])
    return int((correct / len(quiz)) * 100)


def chapter_mastered(title, module_info):
    completed = st.session_state.chapter_progress.get(title, False)
    quiz = module_info.get("quiz", [])
    if not quiz:
        return completed
    return completed and chapter_quiz_percent(title, module_info) >= 80


def render_view_visuals(view_key):
    media = {
        "a": {
            "headline": "Interactive Learning Studio",
            "sub": "Short visual cues and quick videos keep study sessions engaging and memorable.",
            "badges": ["Flashcards", "Skills", "Exam Prep"],
            "image": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=1200&q=80",
            "video": "https://www.youtube.com/watch?v=3PmVJQUCm4E"
        },
        "b": {
            "headline": "Renewal and CEU Momentum",
            "sub": "Track progress visually and stay confident about TULIP deadlines.",
            "badges": ["CEU Tracker", "TULIP Steps", "Renewal Alerts"],
            "image": "https://images.unsplash.com/photo-1584515933487-779824d29309?auto=format&fit=crop&w=1200&q=80",
            "video": "https://www.youtube.com/watch?v=2fYf2b6YfFM"
        },
        "c": {
            "headline": "Facility Leadership Command Center",
            "sub": "Use visual operations insights to support staff readiness and prevent compliance risk.",
            "badges": ["Dashboard", "Risk Triage", "Action Center"],
            "image": "https://images.unsplash.com/photo-1550831107-1553da8c8464?auto=format&fit=crop&w=1200&q=80",
            "video": "https://www.youtube.com/watch?v=qTQ5YGQ5wE8"
        }
    }

    payload = media.get(view_key)
    if not payload:
        return

    st.markdown('<div class="visual-banner">', unsafe_allow_html=True)
    st.markdown(f"### {payload['headline']}")
    st.write(payload["sub"])
    badges = "".join([f'<span class="visual-badge">{badge}</span>' for badge in payload["badges"]])
    st.markdown(badges, unsafe_allow_html=True)
    c1, c2 = st.columns([1.1, 1])
    with c1:
        st.image(payload["image"], use_container_width=True)
    with c2:
        st.video(payload["video"])
    st.markdown('</div>', unsafe_allow_html=True)


def render_quiz_history_panel(history_key, title):
    history = st.session_state.quiz_history.get(history_key, [])
    st.markdown(f"### {title}")
    if not history:
        st.info("No attempts recorded yet. Complete and grade a quiz to start tracking your growth.")
        return

    attempts = len(history)
    best_pct = max(item["percent"] for item in history)
    last_pct = history[-1]["percent"]
    avg_pct = int(sum(item["percent"] for item in history) / attempts)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="kpi">{attempts}</div><div class="label">Attempts</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="kpi">{best_pct}%</div><div class="label">Best Score</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="kpi">{last_pct}%</div><div class="label">Last Score</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card"><div class="kpi">{avg_pct}%</div><div class="label">Average Score</div></div>', unsafe_allow_html=True)

    records = []
    for idx, item in enumerate(reversed(history[-5:]), start=1):
        records.append({
            "Recent Attempt": idx,
            "Date": item["timestamp"],
            "Score": f"{item['score']}/{item['total']}",
            "Percent": f"{item['percent']}%",
            "Mode": "Timed" if item["timed_mode"] else "Practice",
            "Time": item["duration"]
        })
    st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)


# =========================================================
# DATA
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
    {"record_id": 1, "cna_id": 1, "course_title": "Resident Safety Essentials", "hours": 8, "geriatric_flag": True,  "dementia_flag": False, "infection_flag": False},
    {"record_id": 2, "cna_id": 1, "course_title": "Dementia Communication Basics", "hours": 8, "geriatric_flag": False, "dementia_flag": True,  "infection_flag": False},
    {"record_id": 3, "cna_id": 1, "course_title": "Infection Prevention Update", "hours": 10, "geriatric_flag": False, "dementia_flag": False, "infection_flag": True},
    {"record_id": 4, "cna_id": 2, "course_title": "Geriatric Skin Care", "hours": 6, "geriatric_flag": True,  "dementia_flag": False, "infection_flag": False},
    {"record_id": 5, "cna_id": 2, "course_title": "Lift & Transfer Safety", "hours": 4, "geriatric_flag": False, "dementia_flag": False, "infection_flag": False},
    {"record_id": 6, "cna_id": 3, "course_title": "Alzheimer's Support Foundations", "hours": 6, "geriatric_flag": False, "dementia_flag": True,  "infection_flag": False},
    {"record_id": 7, "cna_id": 3, "course_title": "Resident Rights Refresher", "hours": 5, "geriatric_flag": False, "dementia_flag": False, "infection_flag": False},
])

PROMETRIC_SKILLS_SOURCE_URL = "https://www.prometric.com/files/FL_CNA_ClinicalSkillsChecklist.pdf"
PROMETRIC_SKILLS_SOURCE_LABEL = "Prometric Clinical Skills Test Checklist (Florida CNA, 2014)"
PROMETRIC_TX_CIB_SOURCE_URL = "https://www.prometric.com/files/Nurse-Aide/TX-CNA-CIB.pdf"
PROMETRIC_TX_CIB_SOURCE_LABEL = "Prometric Texas CNA Candidate Information Bulletin (2020)"
TX_HHS_CNA_MANUAL_SOURCE_URL = "https://www.hhs.texas.gov/sites/default/files/documents/doing-business-with-hhs/licensing-credentialing-regulation/nurse-aide/cna.pdf"
TX_HHS_CNA_MANUAL_SOURCE_LABEL = "Texas HHS CNA Curriculum for Long-Term Care Facilities (March 2024)"
PROMETRIC_VERIFIED_ALIGNMENT_LABEL = (
    f"{PROMETRIC_SKILLS_SOURCE_LABEL} + "
    f"{PROMETRIC_TX_CIB_SOURCE_LABEL} + "
    f"{TX_HHS_CNA_MANUAL_SOURCE_LABEL}"
)
PROMETRIC_SKILLS_TRUST_NOTE = (
    "Verified sources integrated for clinical-skills, Texas exam content, and Texas curriculum standards: "
    f"[{PROMETRIC_SKILLS_SOURCE_LABEL}]({PROMETRIC_SKILLS_SOURCE_URL}) and "
    f"[{PROMETRIC_TX_CIB_SOURCE_LABEL}]({PROMETRIC_TX_CIB_SOURCE_URL}), and "
    f"[{TX_HHS_CNA_MANUAL_SOURCE_LABEL}]({TX_HHS_CNA_MANUAL_SOURCE_URL})."
)

flashcards = [
    {"category": "Infection Control", "front": "Why should hand hygiene be done before and after caring for a resident?", "back": "It helps reduce the spread of germs and protects both the resident and the caregiver."},
    {"category": "Infection Control", "front": "What does PPE mean in nurse aide care?", "back": "PPE means personal protective equipment, such as gloves, gowns, masks, and face shields."},
    {"category": "Infection Control", "front": "When should gloves be used during resident care?", "back": "Gloves should be used when contact with blood, body fluids, mucous membranes, or contaminated items may happen."},
    {"category": "Infection Control", "front": "Why is it important to avoid touching the inside of the sink during handwashing?", "back": "Touching the sink can recontaminate clean hands."},
    {"category": "Infection Control", "front": "Why should a paper towel be used to shut off the faucet after washing hands?", "back": "Using a paper towel helps prevent clean hands from touching a contaminated faucet."},
    {"category": "Infection Control", "front": "Why should dirty linen be held away from your body?", "back": "Holding soiled linen away from your uniform lowers the chance of spreading contamination."},
    {"category": "Infection Control", "front": "What is the purpose of standard precautions?", "back": "Standard precautions are used with every resident to lower the risk of exposure to infection."},
    {"category": "Infection Control", "front": "Why should a CNA wash hands even after removing gloves?", "back": "Gloves are not perfect barriers, and germs may still be present after removal."},
    {"category": "Infection Control", "front": "Why must clean supplies stay separate from contaminated items?", "back": "Keeping them separate helps stop cross-contamination."},
    {"category": "Infection Control", "front": "Why should fingertips point downward while rinsing the hands?", "back": "This helps water flow away from cleaner areas and reduces contamination."},

    {"category": "Resident Rights", "front": "What does it mean to preserve a resident’s dignity?", "back": "It means treating the resident with respect, courtesy, and sensitivity."},
    {"category": "Resident Rights", "front": "Why should a CNA explain care before starting a task?", "back": "Explanation helps the resident understand what will happen and supports respectful care."},
    {"category": "Resident Rights", "front": "Why should the privacy curtain or door be closed during personal care?", "back": "It protects the resident’s privacy and dignity."},
    {"category": "Resident Rights", "front": "What is informed choice in resident care?", "back": "It means the resident has the right to receive information and take part in decisions."},
    {"category": "Resident Rights", "front": "Why should a CNA knock before entering a resident’s room?", "back": "Knocking shows respect for the resident’s privacy and space."},
    {"category": "Resident Rights", "front": "What should a CNA do if a resident says no to care?", "back": "The CNA should respect the refusal, stay calm, and report it according to policy."},
    {"category": "Resident Rights", "front": "Why must resident information be kept confidential?", "back": "Private health information must be protected from improper sharing."},
    {"category": "Resident Rights", "front": "Why should a resident be covered as much as possible during a bath?", "back": "Keeping the resident covered helps protect privacy, warmth, and dignity."},
    {"category": "Resident Rights", "front": "Why is choice important during daily care routines?", "back": "Allowing choice supports independence and person-centered care."},
    {"category": "Resident Rights", "front": "Why should a CNA speak directly to the resident instead of only to family members?", "back": "The resident remains the main person in the care interaction and deserves direct respect."},

    {"category": "Communication", "front": "How should a CNA talk with a resident who has hearing loss?", "back": "Face the resident, speak clearly, and reduce background noise when possible."},
    {"category": "Communication", "front": "Why is active listening important in CNA work?", "back": "Listening carefully helps the CNA understand needs, preferences, and possible problems."},
    {"category": "Communication", "front": "How should a CNA communicate with a resident who is confused?", "back": "Use short, calm, simple instructions and a reassuring tone."},
    {"category": "Communication", "front": "Why should a CNA avoid arguing with a disoriented resident?", "back": "Arguing can increase stress, fear, and confusion."},
    {"category": "Communication", "front": "What tone of voice is best during resident care?", "back": "A calm, respectful, and reassuring tone is best."},
    {"category": "Communication", "front": "Why is it important to report changes in a resident’s condition quickly?", "back": "Prompt reporting helps the nurse respond to potential problems sooner."},
    {"category": "Communication", "front": "What should a CNA do if a resident does not understand directions?", "back": "Repeat the directions slowly and use simpler wording if needed."},
    {"category": "Communication", "front": "Why should a CNA introduce themselves before giving care?", "back": "Introducing yourself helps orient the resident and build trust."},
    {"category": "Communication", "front": "Why is body language important when caring for residents?", "back": "Posture and facial expression affect whether the resident feels respected and safe."},
    {"category": "Communication", "front": "Why should observations be reported objectively?", "back": "Clear, factual reporting gives the nurse better information for decision-making."},

    {"category": "Safety", "front": "Why must wheelchair wheels be locked before a transfer?", "back": "Locked wheels keep the chair from moving and reduce fall risk."},
    {"category": "Safety", "front": "Why should bed wheels be locked before movement-based care?", "back": "A locked bed stays stable and helps prevent unsafe shifting."},
    {"category": "Safety", "front": "Why should the call light be left within easy reach?", "back": "The resident can request help safely without attempting unsafe movement alone."},
    {"category": "Safety", "front": "Why should walkways stay free of clutter?", "back": "Clear pathways lower the chance of trips and falls."},
    {"category": "Safety", "front": "What should a CNA do if equipment seems unsafe or broken?", "back": "Do not use it and report the problem according to facility policy."},
    {"category": "Safety", "front": "Why are non-skid shoes or socks often important?", "back": "They help lower slipping risk during standing or walking."},
    {"category": "Safety", "front": "What should a CNA do if a resident grows weak during a transfer?", "back": "Protect the resident from falling and call for help."},
    {"category": "Safety", "front": "Why is proper resident positioning important after care is finished?", "back": "Good positioning supports comfort, safety, and pressure relief."},
    {"category": "Safety", "front": "Why should a CNA explain movement before helping a resident stand or transfer?", "back": "Preparation improves cooperation and supports safer movement."},
    {"category": "Safety", "front": "Why should the environment be checked before starting care?", "back": "Looking for hazards first helps prevent accidents during the task."},

    {"category": "Transfers and Mobility", "front": "What is the purpose of a gait belt during certain transfers?", "back": "A gait belt can provide safer support and guidance when moving a resident."},
    {"category": "Transfers and Mobility", "front": "Why should the wheelchair be placed close to the bed before a transfer?", "back": "Close positioning reduces unsafe reaching, twisting, and extra movement."},
    {"category": "Transfers and Mobility", "front": "Why should a CNA use proper body mechanics?", "back": "Good body mechanics help protect both the resident and the caregiver from injury."},
    {"category": "Transfers and Mobility", "front": "Why may the bed height need adjustment before a transfer?", "back": "Proper bed height can support safer movement and better body alignment."},
    {"category": "Transfers and Mobility", "front": "What should be checked before assisting with walking?", "back": "Check the resident’s readiness, footwear, surroundings, and any needed safety equipment."},
    {"category": "Transfers and Mobility", "front": "Why should a resident help with movement if able?", "back": "Participation can improve safety, strength, and independence."},
    {"category": "Transfers and Mobility", "front": "What does ambulation mean?", "back": "Ambulation means walking or helping a resident walk."},
    {"category": "Transfers and Mobility", "front": "Why might a resident need to sit briefly before standing?", "back": "A short pause can help reduce dizziness from position changes."},
    {"category": "Transfers and Mobility", "front": "Why should the wheelchair be aligned correctly before lowering a resident into it?", "back": "Proper alignment supports smoother, safer movement and better positioning."},
    {"category": "Transfers and Mobility", "front": "Why should a CNA stay close during transfer assistance?", "back": "Staying close allows quicker support if balance is lost."},

    {"category": "Vital Signs", "front": "What does blood pressure tell you?", "back": "It reflects the pressure of blood against artery walls."},
    {"category": "Vital Signs", "front": "Why should a blood pressure cuff be placed on a bare arm?", "back": "A bare arm helps improve the accuracy of the reading."},
    {"category": "Vital Signs", "front": "Why should the resident’s arm be supported at heart level during blood pressure measurement?", "back": "Correct arm position helps give a more accurate reading."},
    {"category": "Vital Signs", "front": "What should a CNA do after taking a blood pressure reading?", "back": "Record it correctly and report concerns according to instructions."},
    {"category": "Vital Signs", "front": "Why should unusual vital sign results be reported?", "back": "Abnormal findings may show a change in the resident’s condition."},
    {"category": "Vital Signs", "front": "Why is resident identification important before checking vital signs?", "back": "It helps ensure the right care is provided to the right person."},
    {"category": "Vital Signs", "front": "Why is exact documentation important after measuring a vital sign?", "back": "Accurate records help the care team monitor changes safely."},
    {"category": "Vital Signs", "front": "What does it mean to document a measurement exactly?", "back": "It means recording the actual number observed, not an estimate."},
    {"category": "Vital Signs", "front": "Why should the procedure be explained before taking a vital sign?", "back": "Explaining the step helps the resident know what to expect."},
    {"category": "Vital Signs", "front": "What should a CNA do if unsure whether a reading is correct?", "back": "Follow policy, repeat if allowed, and report to the nurse."},

    {"category": "Elimination", "front": "Why should urinary output be read at eye level?", "back": "Reading it at eye level helps improve measurement accuracy."},
    {"category": "Elimination", "front": "Why are gloves needed when handling urine or urine equipment?", "back": "Gloves help protect against exposure to body fluids."},
    {"category": "Elimination", "front": "Why should urinary output be recorded exactly instead of estimated?", "back": "Exact amounts are needed for accurate monitoring."},
    {"category": "Elimination", "front": "Why is privacy important during elimination care?", "back": "Privacy supports dignity, respect, and comfort."},
    {"category": "Elimination", "front": "What should a CNA do after measuring urinary output?", "back": "Clean equipment as instructed, remove gloves, and perform hand hygiene."},
    {"category": "Elimination", "front": "Why should the measuring container be placed on a flat surface to read it?", "back": "A level surface helps improve measurement accuracy."},
    {"category": "Elimination", "front": "Why should changes in bowel or bladder patterns be reported?", "back": "Changes may signal a health issue that needs attention."},
    {"category": "Elimination", "front": "Why is it important to avoid spills while measuring urine?", "back": "Spills affect accuracy and increase contamination risk."},
    {"category": "Elimination", "front": "What is urinary output?", "back": "Urinary output is the amount of urine a resident produces."},
    {"category": "Elimination", "front": "Why should hand hygiene still be done after glove removal in elimination care?", "back": "Hands may still carry germs after the gloves come off."},

    {"category": "Nutrition and Hydration", "front": "Why is good hydration important for residents?", "back": "Fluids support body function, comfort, and overall health."},
    {"category": "Nutrition and Hydration", "front": "Why should a CNA observe how much a resident eats and drinks?", "back": "Poor intake may need reporting and follow-up."},
    {"category": "Nutrition and Hydration", "front": "Why is positioning important before meals?", "back": "Proper positioning can improve comfort and lower choking risk."},
    {"category": "Nutrition and Hydration", "front": "What should a CNA do if a resident begins coughing during a meal?", "back": "Stop and respond according to safety procedures, then report the concern."},
    {"category": "Nutrition and Hydration", "front": "Why should meal preferences be respected when allowed?", "back": "Respecting preferences supports dignity and better participation in meals."},
    {"category": "Nutrition and Hydration", "front": "Why should a poor appetite be reported?", "back": "Not eating enough may affect nutrition and health."},
    {"category": "Nutrition and Hydration", "front": "Why should residents not be rushed while eating?", "back": "A calm pace supports safety, comfort, and better intake."},
    {"category": "Nutrition and Hydration", "front": "What should be checked before assisting with a meal tray?", "back": "Check the resident, position, and any feeding instructions or precautions."},
    {"category": "Nutrition and Hydration", "front": "Why may intake need to be documented?", "back": "Tracking intake helps the care team monitor nutrition and hydration."},
    {"category": "Nutrition and Hydration", "front": "Why can gentle encouragement help at mealtime?", "back": "Encouragement may improve comfort and cooperation without forcing."},

    {"category": "Skin Care and Personal Care", "front": "Why is observing the skin important during daily care?", "back": "Skin checks can reveal redness, irritation, or breakdown early."},
    {"category": "Skin Care and Personal Care", "front": "Why should the skin be dried gently after bathing?", "back": "Gentle drying helps protect delicate skin and improve comfort."},
    {"category": "Skin Care and Personal Care", "front": "Why is perineal care usually done from cleaner areas toward dirtier areas?", "back": "This method helps reduce the spread of germs."},
    {"category": "Skin Care and Personal Care", "front": "Why should all needed supplies be prepared before starting personal care?", "back": "Preparation helps care stay safe, efficient, and organized."},
    {"category": "Skin Care and Personal Care", "front": "Why should the resident remain covered during a bath except for the body part being washed?", "back": "This protects warmth, privacy, and dignity."},
    {"category": "Skin Care and Personal Care", "front": "Why should skin products be used only as directed?", "back": "Products should follow instructions or care plans to avoid harm."},
    {"category": "Skin Care and Personal Care", "front": "Why should red areas over bony parts be reported?", "back": "They may be early warning signs of pressure injury."},
    {"category": "Skin Care and Personal Care", "front": "Why is oral care important in daily CNA practice?", "back": "Oral care supports comfort, cleanliness, and general health."},
    {"category": "Skin Care and Personal Care", "front": "Why should nail care be done carefully?", "back": "Careful nail care helps avoid injury and supports hygiene."},
    {"category": "Skin Care and Personal Care", "front": "Why does gentle handling matter during personal care?", "back": "Gentle care supports trust, comfort, and dignity."},

    {"category": "Mental Health and Social Needs", "front": "Why is reassurance important for an anxious resident?", "back": "Reassurance can reduce fear and help the resident feel safer."},
    {"category": "Mental Health and Social Needs", "front": "Why should a CNA encourage independence when possible?", "back": "Encouraging independence supports self-esteem and function."},
    {"category": "Mental Health and Social Needs", "front": "Why may loneliness affect a resident’s well-being?", "back": "Isolation can affect mood, motivation, and overall quality of life."},
    {"category": "Mental Health and Social Needs", "front": "Why should a CNA report sudden mood or behavior changes?", "back": "Unexpected changes may signal illness, pain, or emotional distress."},
    {"category": "Mental Health and Social Needs", "front": "Why should residents be treated as adults even when they need full care?", "back": "Every resident deserves respect regardless of their level of dependence."},
    {"category": "Mental Health and Social Needs", "front": "Why is patience important when helping a slow-moving resident?", "back": "Patience supports dignity and reduces frustration for the resident."},
    {"category": "Mental Health and Social Needs", "front": "Why should family concerns sometimes be shared with the nurse?", "back": "Family observations may provide useful information about the resident’s condition."},
    {"category": "Mental Health and Social Needs", "front": "Why is social interaction part of quality care?", "back": "Meaningful interaction can support emotional well-being and reduce isolation."},
    {"category": "Mental Health and Social Needs", "front": "Why should a CNA avoid speaking about a resident as if they are not present?", "back": "It is disrespectful and can harm dignity and trust."},
    {"category": "Mental Health and Social Needs", "front": "Why should a CNA support resident routines when possible?", "back": "Familiar routines can improve comfort, security, and cooperation."},

    {"category": "Restorative Care", "front": "What is the purpose of restorative care?", "back": "Restorative care helps residents maintain or improve function and independence."},
    {"category": "Restorative Care", "front": "Why should a CNA encourage a resident to do what they can for themselves?", "back": "Doing so helps preserve ability, confidence, and independence."},
    {"category": "Restorative Care", "front": "Why are range-of-motion exercises used?", "back": "They help maintain joint movement and flexibility."},
    {"category": "Restorative Care", "front": "Why should movements during exercises be slow and gentle?", "back": "Slow, careful motion reduces discomfort and injury risk."},
    {"category": "Restorative Care", "front": "Why should pain during movement be reported?", "back": "Pain may mean the exercise or activity should be reassessed."},
    {"category": "Restorative Care", "front": "Why can assistive devices support independence?", "back": "Devices such as walkers or adaptive tools can help residents do more safely."},
    {"category": "Restorative Care", "front": "Why should a CNA follow instructions closely during restorative tasks?", "back": "These activities should match the resident’s plan and safety needs."},
    {"category": "Restorative Care", "front": "Why is regular walking encouragement helpful for some residents?", "back": "Walking may help preserve strength, mobility, and circulation."},
    {"category": "Restorative Care", "front": "Why should a resident’s progress or decline in function be reported?", "back": "Changes in ability may affect the care approach and safety plan."},
    {"category": "Restorative Care", "front": "Why should independence be balanced with supervision?", "back": "Residents should do what they can, but still need protection from unsafe situations."},

    {"category": "Documentation and Reporting", "front": "When should a CNA document care?", "back": "Care should be documented after it is completed."},
    {"category": "Documentation and Reporting", "front": "Why must charting be accurate?", "back": "Accurate charting supports safe communication and care decisions."},
    {"category": "Documentation and Reporting", "front": "What kinds of resident changes should be reported quickly?", "back": "Examples include pain, dizziness, weakness, confusion, unusual drowsiness, or safety concerns."},
    {"category": "Documentation and Reporting", "front": "Why should a CNA avoid guessing when documenting?", "back": "Documentation should reflect exact observations, not assumptions."},
    {"category": "Documentation and Reporting", "front": "Why should a fall be reported right away?", "back": "A fall may involve injury or urgent follow-up needs."},
    {"category": "Documentation and Reporting", "front": "What is objective reporting?", "back": "Objective reporting means sharing clear facts and observations instead of opinions."},
    {"category": "Documentation and Reporting", "front": "Why should unusual bruising, redness, or swelling be reported?", "back": "These may show injury or a change in condition."},
    {"category": "Documentation and Reporting", "front": "Why must documentation be entered for the correct resident?", "back": "Correct identification is necessary for safe, accurate records."},
    {"category": "Documentation and Reporting", "front": "Why is timely reporting important for the nurse aide role?", "back": "Fast reporting helps the care team respond sooner to problems."},
    {"category": "Documentation and Reporting", "front": "Why should facility policy guide reporting and charting?", "back": "Following policy helps information stay consistent, safe, and properly handled."},

    {"category": "Prometric Clinical Skills (Verified)", "front": "Which two skills are always scored in the Prometric clinical skills test?", "back": "Handwashing and Indirect Care are scored for every candidate."},
    {"category": "Prometric Clinical Skills (Verified)", "front": "What are core Indirect Care behaviors observed across all skills?", "back": "Greet by name, explain care, ask preferences/comfort, use infection control, protect rights, and promote safety."},
    {"category": "Prometric Clinical Skills (Verified)", "front": "During ambulation with a gait belt, where should the CNA stand?", "back": "At the side and slightly behind the resident while supporting with the gait belt."},
    {"category": "Prometric Clinical Skills (Verified)", "front": "What is the checklist expectation for radial pulse timing?", "back": "Count for one full minute and record within +/- 4 bpm of the nurse measurement."},
    {"category": "Prometric Clinical Skills (Verified)", "front": "For urinary output skill, when should gloves be removed?", "back": "Remove gloves before documenting intake/output after handling drainage bag or urine container."},
    {"category": "Prometric Clinical Skills (Verified)", "front": "During feeding skill, how often should fluids be offered?", "back": "Offer fluids throughout feeding, at least every 2-3 bites of food."},
    {"category": "Prometric Clinical Skills (Verified)", "front": "What transfer checkpoint is required before pivot transfer to wheelchair?", "back": "Move footrests out of the way and place non-skid footwear before standing the resident."},
    {"category": "Prometric Clinical Skills (Verified)", "front": "In female catheter care, what direction is used for cleansing?", "back": "Wipe front to back, and clean catheter away from the body while stabilizing near the meatus."},

    {"category": "Texas CNA CIB (Verified)", "front": "How many questions are on the Texas CNA written exam according to the CIB?", "back": "The written test has 60 multiple-choice questions."},
    {"category": "Texas CNA CIB (Verified)", "front": "How much time is allowed for the Texas CNA written test?", "back": "The CIB lists 90 minutes for the written test."},
    {"category": "Texas CNA CIB (Verified)", "front": "How many skills are scored in the Texas clinical skills exam?", "back": "Five skills are scored: three assigned skills plus Handwashing and Indirect Care."},
    {"category": "Texas CNA CIB (Verified)", "front": "How many attempts are allowed in Texas before retraining is required?", "back": "Up to three attempts each for the clinical skills test and the written/oral test within 24 months."},
    {"category": "Texas CNA CIB (Verified)", "front": "What happens after passing both Texas CNA exams?", "back": "Candidate information is sent for placement on the Texas Nurse Aide Registry."},
    {"category": "Texas CNA CIB (Verified)", "front": "What must candidates bring to test day based on the CIB?", "back": "Authorization to Test letter, one current government-issued photo ID with signature, and a second matching ID."},
    {"category": "Texas CNA CIB (Verified)", "front": "What footwear is required for the clinical skills test?", "back": "Flat, nonskid, closed-toed shoes are required."},
    {"category": "Texas CNA CIB (Verified)", "front": "When should candidates arrive at the test site?", "back": "At least 30 minutes before the scheduled test appointment."},

    {"category": "Texas HHS CNA Manual (Verified)", "front": "What is the core goal of the Texas HHS CNA curriculum?", "back": "Prepare nurse aides to provide person-centered basic care in long-term care facilities."},
    {"category": "Texas HHS CNA Manual (Verified)", "front": "What three documentation actions are emphasized in the Texas HHS manual?", "back": "Observe, report, and document to the nurse."},
    {"category": "Texas HHS CNA Manual (Verified)", "front": "What does OBRA focus on in Texas long-term care training?", "back": "Resident rights, restorative care, psychosocial care, and preventive care for maximum wellness."},
    {"category": "Texas HHS CNA Manual (Verified)", "front": "How many total training hours are required in the Texas HHS nurse aide training program?", "back": "At least 100 total hours, including 60 classroom and 40 clinical hours."},
    {"category": "Texas HHS CNA Manual (Verified)", "front": "What is required before any direct resident contact during training?", "back": "The first 16 hours of training must be completed before direct resident contact."},
    {"category": "Texas HHS CNA Manual (Verified)", "front": "How often must nurse aides complete in-service education for renewal per the Texas HHS manual?", "back": "24 hours of in-service education every two years."},
    {"category": "Texas HHS CNA Manual (Verified)", "front": "How does the Texas HHS manual define hand hygiene?", "back": "Washing with soap and water or correctly applying alcohol-based sanitizer."},
    {"category": "Texas HHS CNA Manual (Verified)", "front": "What does person-centered care mean in LTC training?", "back": "Respecting resident choices and tailoring care, dining, and activities to resident preferences."}
]

category_descriptions = {
    "Infection Control": "Practice hand hygiene, PPE, and contamination prevention for every resident interaction.",
    "Resident Rights": "Focus on dignity, privacy, choice, and respectful communication.",
    "Communication": "Use clear, calm language and active listening to support resident understanding.",
    "Safety": "Remember hazard checks, secure equipment, and safe resident positioning.",
    "Transfers and Mobility": "Review gait belts, body mechanics, and safe transfer preparation.",
    "Vital Signs": "Prioritize accurate technique, correct positioning, and prompt reporting.",
    "Elimination": "Keep care private, hygienic, and report any changes in output patterns.",
    "Nutrition and Hydration": "Observe intake, support proper positioning, and report appetite changes.",
    "Skin Care and Personal Care": "Protect skin integrity, maintain cleanliness, and preserve dignity.",
    "Mental Health and Social Needs": "Support emotional well-being with patience, reassurance, and social connection.",
    "Restorative Care": "Encourage independence safely and follow restorative plans consistently.",
    "Documentation and Reporting": "Document observations accurately and report changes clearly.",
    "Prometric Clinical Skills (Verified)": "Checklist-aligned checkpoints from the Prometric clinical skills source used in training and review.",
    "Texas CNA CIB (Verified)": "Texas Candidate Information Bulletin facts for exam process, timing, and score requirements.",
    "Texas HHS CNA Manual (Verified)": "Texas HHS curriculum and OBRA-aligned care standards for long-term care training.",
}

written_quiz = [
    {
        "q": "Which action best supports infection prevention?",
        "choices": ["Wash hands before and after care", "Reuse gloves between residents", "Put linen on the floor", "Skip PPE if hurried"],
        "answer": "Wash hands before and after care",
        "rationale": "Hand hygiene is a core infection-prevention action."
    },
    {
        "q": "Which resident right must be protected during bathing and toileting?",
        "choices": ["Privacy", "Speed only", "Silence from all staff", "Immediate discharge"],
        "answer": "Privacy",
        "rationale": "Residents have the right to privacy, dignity, and respectful treatment."
    },
    {
        "q": "Before beginning a clinical skill, the CNA should first:",
        "choices": ["Identify the resident and explain the procedure", "Document care", "Skip to the task", "Ask another resident for help"],
        "answer": "Identify the resident and explain the procedure",
        "rationale": "Proper identification and communication improve safety and trust."
    },
    {
        "q": "Which observation should be reported promptly?",
        "choices": ["Resident watched TV", "New dizziness during transfer", "Resident requested a blanket", "Resident ate lunch"],
        "answer": "New dizziness during transfer",
        "rationale": "A new change in condition may indicate risk and requires attention."
    },
    {
        "q": "Documentation should occur:",
        "choices": ["After care is completed", "Before care starts", "Only weekly", "Only if family asks"],
        "answer": "After care is completed",
        "rationale": "Documentation should reflect actual completed care and observations."
    },
    {
        "q": "A CNA supports resident independence by:",
        "choices": ["Doing everything quickly without asking", "Encouraging the resident to do what they can safely do", "Ignoring assistive devices", "Avoiding all conversation"],
        "answer": "Encouraging the resident to do what they can safely do",
        "rationale": "Long-term care focuses on preserving function and dignity."
    },
    {
        "q": "Which action supports respectful dementia care?",
        "choices": ["Argue with confusion", "Use calm redirection", "Rush the resident", "Mock repeated questions"],
        "answer": "Use calm redirection",
        "rationale": "Calm redirection is safer and more supportive than confrontation."
    },
    {
        "q": "According to the verified Prometric checklist, which pair is always scored in the Clinical Skills Test?",
        "choices": ["Blood pressure and feeding", "Handwashing and Indirect Care", "ROM and transfer", "Catheter care and bedpan"],
        "answer": "Handwashing and Indirect Care",
        "rationale": "Prometric identifies Handwashing and Indirect Care as required scored elements in every skills test."
    },
    {
        "q": "Which behavior is part of Indirect Care in the verified checklist?",
        "choices": ["Skip resident preferences to save time", "Ask about resident preferences during care", "Document before care starts", "Avoid communication during care"],
        "answer": "Ask about resident preferences during care",
        "rationale": "Indirect Care includes asking resident preferences, comfort, and maintaining rights/safety."
    },
    {
        "q": "For the radial pulse skill, what timing is required in the verified checklist?",
        "choices": ["15 seconds", "30 seconds", "45 seconds", "One full minute"],
        "answer": "One full minute",
        "rationale": "Prometric checklist requires counting radial pulse for one full minute."
    },
    {
        "q": "According to the Texas CNA CIB, how many questions are on the written test?",
        "choices": ["40", "50", "60", "75"],
        "answer": "60",
        "rationale": "The Texas CIB states the written knowledge test consists of 60 multiple-choice questions."
    },
    {
        "q": "How much time does the Texas CNA CIB allow for the written test?",
        "choices": ["60 minutes", "75 minutes", "90 minutes", "120 minutes"],
        "answer": "90 minutes",
        "rationale": "The Texas CIB specifies a 90-minute time limit for the written test."
    },
    {
        "q": "Per the Texas CIB, what is required to pass the clinical skills test?",
        "choices": ["Pass any 3 skills", "Pass all 5 scored skills", "Pass handwashing only", "Pass one random skill"],
        "answer": "Pass all 5 scored skills",
        "rationale": "Texas CIB states candidates must pass all five scored skills in the clinical skills test."
    },
    {
        "q": "According to the Texas HHS CNA manual, what are the required NATCEP minimum training hours?",
        "choices": ["80 total: 40 classroom + 40 clinical", "90 total: 50 classroom + 40 clinical", "100 total: 60 classroom + 40 clinical", "120 total: 60 classroom + 60 clinical"],
        "answer": "100 total: 60 classroom + 40 clinical",
        "rationale": "The Texas HHS CNA curriculum states NATCEP must be at least 100 clock hours, including 60 classroom and 40 clinical hours."
    },
    {
        "q": "Before direct resident contact during training, the Texas HHS manual requires completion of:",
        "choices": ["8 hours", "12 hours", "16 hours", "24 hours"],
        "answer": "16 hours",
        "rationale": "The first 16 hours of nurse aide training must be completed prior to any direct resident contact."
    },
    {
        "q": "Which best reflects a Texas HHS curriculum objective for nurse aides?",
        "choices": ["Prioritize speed over resident choice", "Provide person-centered care and protect resident rights", "Avoid documentation unless requested", "Perform only independent care planning"],
        "answer": "Provide person-centered care and protect resident rights",
        "rationale": "Course objectives emphasize person-centered care, resident rights, safety, and observation/reporting/documentation."
    }
]

prometric_sample_test = [
    {
        "q": "A resident often carries a doll with her, treating it like her baby. One day she is wandering around crying that she can't find her baby. The nurse aide should",
        "choices": [
            "ask the resident where she last had the doll.",
            "ask the activity department if they have any other dolls.",
            "offer comfort to the resident and help her look for her baby.",
            "let the other staff know the resident is very confused and should be watched closely."
        ],
        "answer": "offer comfort to the resident and help her look for her baby."
    },
    {
        "q": "A nurse aide is asked to change a urinary drainage bag attached to an indwelling urinary catheter. The nurse aide has never done this before. The best response by the nurse aide is to",
        "choices": [
            "change the indwelling catheter at the same time.",
            "ask another nurse aide to change the urinary drainage bag.",
            "change the bag asking for help only if the nurse aide has problems.",
            "ask a nurse to watch the nurse aide change the bag since it is the first time."
        ],
        "answer": "ask a nurse to watch the nurse aide change the bag since it is the first time."
    },
    {
        "q": "Before feeding a resident, which of the following is the best reason to wash the resident's hands?",
        "choices": [
            "The resident may still touch his/her mouth or food.",
            "It reduces the risk of spreading airborne diseases.",
            "It improves resident morale and appetite.",
            "The resident needs to keep meal routines."
        ],
        "answer": "The resident may still touch his/her mouth or food."
    },
    {
        "q": "Which of the following is a job task performed by the nurse aide?",
        "choices": [
            "Participating in resident care planning conferences",
            "Taking a telephone order from a physician",
            "Giving medications to assigned residents",
            "Changing sterile wound dressings"
        ],
        "answer": "Participating in resident care planning conferences"
    },
    {
        "q": "Which of the following statements is true about range of motion (ROM) exercises?",
        "choices": [
            "Done just once a day",
            "Help prevent strokes and paralysis",
            "Require at least ten repetitions of each exercise",
            "Are often performed during ADLs such as bathing or dressing"
        ],
        "answer": "Are often performed during ADLs such as bathing or dressing"
    },
    {
        "q": "While the nurse aide tries to dress a resident who is confused, the resident keeps trying to grab a hairbrush. The nurse aide should",
        "choices": [
            "put the hairbrush away and out of sight.",
            "give the resident the hairbrush to hold.",
            "try to dress the resident more quickly.",
            "restrain the resident's hand."
        ],
        "answer": "give the resident the hairbrush to hold."
    },
    {
        "q": "A resident who is lying in bed suddenly becomes short of breath. After calling for help, the nurse aide's next action should be to",
        "choices": [
            "ask the resident to take deep breaths.",
            "take the resident's vital signs.",
            "raise the head of the bed.",
            "elevate the resident's feet."
        ],
        "answer": "raise the head of the bed."
    },
    {
        "q": "A resident who has cancer is expected to die within the next couple of days. Nursing care for this resident should focus on",
        "choices": [
            "helping the resident through the stages of grief.",
            "providing for the resident's comfort.",
            "keeping the resident's care routine, such as for bathing.",
            "giving the resident a lot of quiet time and privacy."
        ],
        "answer": "providing for the resident's comfort."
    },
    {
        "q": "While giving a bedbath, the nurse aide hears the alarm from a nearby door suddenly go off. The nurse aide should",
        "choices": [
            "wait a few minutes to see if the alarm stops.",
            "report the alarm to the charge nurse immediately.",
            "make the resident being bathed safe and go check the door right away.",
            "stop the bedbath and go check on the location of all assigned residents."
        ],
        "answer": "make the resident being bathed safe and go check the door right away."
    },
    {
        "q": "Gloves should be worn for which of the following procedures?",
        "choices": [
            "Emptying a urinary drainage bag",
            "Brushing a resident's hair",
            "Ambulating a resident",
            "Feeding a resident"
        ],
        "answer": "Emptying a urinary drainage bag"
    },
    {
        "q": "When walking a resident, a gait or transfer belt is often",
        "choices": [
            "worn around the nurse aide's waist for back support.",
            "used to keep the resident positioned properly in the wheelchair.",
            "used to help stand the resident, and then removed before walking.",
            "put around the resident's waist to provide a way to hold onto the resident."
        ],
        "answer": "put around the resident's waist to provide a way to hold onto the resident."
    },
    {
        "q": "Which of the following statements is true about residents who are restrained?",
        "choices": [
            "They are at greater risk for developing pressure sores.",
            "They are at lower risk of developing pneumonia.",
            "Their posture and alignment are improved.",
            "They are not at risk for falling."
        ],
        "answer": "They are at greater risk for developing pressure sores."
    },
    {
        "q": "A resident has diabetes. Which of the following is a common sign of a low blood sugar?",
        "choices": ["Fever", "Shakiness", "Thirst", "Vomiting"],
        "answer": "Shakiness"
    },
    {
        "q": "When providing foot care to a resident it is important for the nurse aide to",
        "choices": [
            "remove calluses and corns.",
            "check the feet for skin breakdown.",
            "keep the water cool to prevent burns.",
            "apply lotion, including between the toes."
        ],
        "answer": "check the feet for skin breakdown."
    },
    {
        "q": "When feeding a resident, frequent coughing can be a sign the resident is",
        "choices": ["choking.", "getting full.", "needs to drink more fluids.", "having difficulty swallowing."],
        "answer": "having difficulty swallowing."
    },
    {
        "q": "When a person is admitted to the nursing home, the nurse aide should expect that the resident will",
        "choices": [
            "have problems related to incontinence.",
            "require a lot of assistance with personal care.",
            "experience a sense of loss related to the life change.",
            "adjust more quickly if admitted directly from the hospital."
        ],
        "answer": "experience a sense of loss related to the life change."
    },
    {
        "q": "A resident gets dressed and comes out of his room wearing shoes that are from two different pairs. The nurse aide should",
        "choices": [
            "tease the resident by complimenting the resident's sense of style.",
            "ask if the resident realizes that the shoes do not match.",
            "remind the resident that the nurse aide can dress the resident.",
            "ask if the resident lost some of his shoes."
        ],
        "answer": "ask if the resident realizes that the shoes do not match."
    },
    {
        "q": "A resident's wife recently died. The resident is now staying in his room all the time and eating very little. The best response by the nurse aide is to",
        "choices": [
            "remind the resident to be thankful for the years he shared with his wife.",
            "tell the resident that he needs to get out of his room at least once a day.",
            "understand the resident is grieving and give him chances to talk.",
            "avoid mentioning his wife when caring for him."
        ],
        "answer": "understand the resident is grieving and give him chances to talk."
    },
    {
        "q": "When a resident refuses a bedbath, the nurse aide should",
        "choices": [
            "offer the resident a bribe.",
            "wait awhile and then ask the resident again.",
            "remind the resident that people who smell don't have friends.",
            "tell the resident that nursing home policy requires daily bathing."
        ],
        "answer": "wait awhile and then ask the resident again."
    },
    {
        "q": "When a resident is combative and trying to hit the nurse aide, it is important for the nurse aide to",
        "choices": [
            "show the resident that the nurse aide is in control.",
            "call for help to make sure there are witnesses.",
            "explain that if the resident is not calm a restraint may be applied.",
            "step back to protect self from harm while speaking in a calm manner."
        ],
        "answer": "step back to protect self from harm while speaking in a calm manner."
    },
    {
        "q": "During lunch in the dining room, a resident begins yelling and throws a spoon at the nurse aide. The best response by the nurse aide is to",
        "choices": [
            "remain calm and ask what is upsetting the resident.",
            "begin removing all the other residents from the dining room.",
            "scold the resident and ask the resident to leave the dining room immediately.",
            "remove the resident's plate, fork, knife, and cup so there is nothing else to throw."
        ],
        "answer": "remain calm and ask what is upsetting the resident."
    },
    {
        "q": "Which of the following questions asked to the resident is most likely to encourage conversation?",
        "choices": [
            "Are you feeling tired today?",
            "Do you want to wear this outfit?",
            "What are your favorite foods?",
            "Is this water warm enough?"
        ],
        "answer": "What are your favorite foods?"
    },
    {
        "q": "When trying to communicate with a resident who speaks a different language than the nurse aide, the nurse aide should",
        "choices": [
            "use pictures and gestures.",
            "face the resident and speak softly when talking.",
            "repeat words often if the resident does not understand.",
            "assume when the resident nods his/her head that the message is understood."
        ],
        "answer": "use pictures and gestures."
    },
    {
        "q": "While walking down the hall, a nurse aide looks into a resident's room and sees another nurse aide hitting a resident. The nurse aide is expected to",
        "choices": [
            "contact the state agency that inspects the nursing facility.",
            "enter the room immediately to provide for the resident's safety.",
            "wait to confront the nurse aide when he/she leaves the resident's room.",
            "check the resident for any signs of injury after the nurse aide leaves the room."
        ],
        "answer": "enter the room immediately to provide for the resident's safety."
    },
    {
        "q": "Before touching a resident who is crying to offer comfort, the nurse aide should consider",
        "choices": [
            "the resident's recent vital signs.",
            "the resident's cultural background.",
            "whether the resident has been sad recently.",
            "whether the resident has family that visits routinely."
        ],
        "answer": "the resident's cultural background."
    },
    {
        "q": "When a resident is expressing anger, the nurse aide should",
        "choices": [
            "correct the resident's misperceptions.",
            "ask the resident to speak in a kinder tone.",
            "listen closely to the resident's concerns.",
            "remind the resident that everyone gets angry."
        ],
        "answer": "listen closely to the resident's concerns."
    },
    {
        "q": "When giving a backrub, the nurse aide should",
        "choices": [
            "apply lotion to the back directly from the bottle.",
            "keep the resident covered as much as possible.",
            "leave extra lotion on the skin when completing the procedure.",
            "expect the resident to lie on his/her stomach."
        ],
        "answer": "keep the resident covered as much as possible."
    },
    {
        "q": "A nurse aide finds a resident looking in the refrigerator at the nurses' station at 5 a.m. The resident, who is confused, explains he needs breakfast before he leaves for work. The best response by the nurse aide is to",
        "choices": [
            "help the resident back to his room and into bed.",
            "ask the resident about his job and if he is hungry.",
            "tell him that residents are not allowed in the nurses' station.",
            "remind him that he is retired from his job and in a nursing home."
        ],
        "answer": "ask the resident about his job and if he is hungry."
    },
    {
        "q": "Which of the following is true about caring for a resident who wears a hearing aid?",
        "choices": [
            "Apply hairspray after the hearing aid is in place.",
            "Remove the hearing aid before showering.",
            "Clean the earmold and battery case with water daily, drying completely.",
            "Replace batteries weekly."
        ],
        "answer": "Remove the hearing aid before showering."
    },
    {
        "q": "Residents with Parkinson's disease often require assistance with walking because they",
        "choices": [
            "become confused and forget how to take steps without help.",
            "have poor attention skills and do not notice safety problems.",
            "have visual problems that require special glasses.",
            "have a shuffling walk and tremors."
        ],
        "answer": "have a shuffling walk and tremors."
    },
    {
        "q": "A resident who is inactive is at risk of constipation. In addition to increased activity and exercise, which of the following actions helps to prevent constipation?",
        "choices": ["Adequate fluid intake", "Regular mealtimes", "High protein diet", "Low fiber diet"],
        "answer": "Adequate fluid intake"
    },
    {
        "q": "A resident has an indwelling urinary catheter. While making rounds, the nurse aide notices that there is no urine in the drainage bag. The nurse aide should first",
        "choices": [
            "ask the resident to try urinating.",
            "offer the resident fluid to drink.",
            "check for kinks in the tubing.",
            "obtain a new urinary drainage bag."
        ],
        "answer": "check for kinks in the tubing."
    },
    {
        "q": "A resident who is incontinent of urine has an increased risk of developing",
        "choices": ["dementia.", "urinary tract infections.", "pressure sores.", "dehydration."],
        "answer": "pressure sores."
    },
    {
        "q": "When cleansing the genital area during perineal care, the nurse aide should",
        "choices": [
            "cleanse the penis with a circular motion starting from the base and moving toward the tip.",
            "replace the foreskin when pushed back to cleanse an uncircumcised penis.",
            "cleanse the rectal area first, before cleansing the genital area.",
            "use the same area on the washcloth for each washing and rinsing stroke for a female resident."
        ],
        "answer": "replace the foreskin when pushed back to cleanse an uncircumcised penis."
    },
    {
        "q": "Which of the following is considered a normal age-related change?",
        "choices": ["Dementia", "Contractures", "Bladder holding less urine", "Wheezing when breathing"],
        "answer": "Bladder holding less urine"
    },
    {
        "q": "A resident is on a bladder retraining program. The nurse aide can expect the resident to",
        "choices": [
            "have a fluid intake restriction to prevent sudden urges to urinate.",
            "wear an incontinent brief in case of an accident.",
            "have an indwelling urinary catheter.",
            "have a schedule for toileting."
        ],
        "answer": "have a schedule for toileting."
    },
    {
        "q": "A resident who has stress incontinence",
        "choices": [
            "will have an indwelling urinary catheter.",
            "should wear an incontinent brief at night.",
            "may leak urine when laughing or coughing.",
            "needs toileting every 1-2 hours throughout the day."
        ],
        "answer": "may leak urine when laughing or coughing."
    },
    {
        "q": "The doctor has told the resident that his cancer is growing and that he is dying. When the resident tells the nurse aide that there is a mistake, the nurse aide should",
        "choices": [
            "understand that denial is a normal reaction.",
            "remind the resident the doctor would not lie.",
            "suggest the resident ask for more tests.",
            "ask if the resident is afraid of dying."
        ],
        "answer": "understand that denial is a normal reaction."
    },
    {
        "q": "A slipknot is used when securing a restraint so that",
        "choices": [
            "the restraint cannot be removed by the resident.",
            "the restraint can be removed quickly when needed.",
            "body alignment is maintained while wearing the restraint.",
            "it can be easily observed whether the restraint is applied correctly."
        ],
        "answer": "the restraint can be removed quickly when needed."
    },
    {
        "q": "When using personal protective equipment (PPE) the nurse aide correctly follows Standard Precautions when wearing",
        "choices": [
            "double gloves when providing perineal care to a resident.",
            "a mask and gown while feeding a resident that coughs.",
            "gloves to remove a resident's bedpan.",
            "gloves while ambulating a resident."
        ],
        "answer": "gloves to remove a resident's bedpan."
    },
    {
        "q": "To help prevent resident falls, the nurse aide should",
        "choices": [
            "always raise siderails when any resident is in his/her bed.",
            "leave residents' beds at the lowest level when care is complete.",
            "encourage residents to wear larger-sized, loose-fitting clothing.",
            "remind residents who use call lights that they need to wait patiently for staff."
        ],
        "answer": "leave residents' beds at the lowest level when care is complete."
    },
    {
        "q": "As the nurse aide begins his/her assignment, which of the following should the nurse aide do first?",
        "choices": [
            "Collect linen supplies for the shift",
            "Check all the nurse aide's assigned residents",
            "Assist a resident that has called for assistance to get off the toilet",
            "Start bathing a resident that has physical therapy in one hour"
        ],
        "answer": "Assist a resident that has called for assistance to get off the toilet"
    },
    {
        "q": "Which of the following would affect a nurse aide's status on the state's nurse aide registry and also cause the nurse aide to be ineligible to work in a nursing home?",
        "choices": [
            "Having been terminated from another facility for repeated tardiness",
            "Missing a mandatory infection control inservice training program",
            "Failing to show for work without calling to report the absence",
            "Having a finding for resident neglect"
        ],
        "answer": "Having a finding for resident neglect"
    },
    {
        "q": "To help prevent the spread of germs between patients, nurse aides should",
        "choices": [
            "wear gloves when touching residents.",
            "hold supplies and linens away from their uniforms.",
            "wash hands for at least two minutes after each resident contact.",
            "warn residents that holding hands spreads germs."
        ],
        "answer": "hold supplies and linens away from their uniforms."
    },
    {
        "q": "When a sink has hand-control faucets, the nurse aide should use",
        "choices": [
            "a paper towel to turn the water on.",
            "a paper towel to turn the water off.",
            "an elbow, if possible, to turn the faucet controls on and off.",
            "bare hands to turn the faucet controls both on and off."
        ],
        "answer": "a paper towel to turn the water off."
    },
    {
        "q": "When moving a resident up in bed who is able to move with assistance, the nurse aide should",
        "choices": [
            "position self with knees straight and bent at waist.",
            "use a gait or transfer belt to assist with the repositioning.",
            "pull the resident up holding onto one side of the drawsheet at a time.",
            "bend the resident's knees and ask the resident to push with his/her feet."
        ],
        "answer": "bend the resident's knees and ask the resident to push with his/her feet."
    },
    {
        "q": "The resident's weight is obtained routinely as a way to check the resident's",
        "choices": ["growth and development.", "adjustment to the facility.", "nutrition and health.", "activity level."],
        "answer": "nutrition and health."
    },
    {
        "q": "Which of the following is a right that is included in the Resident's Bill of Rights?",
        "choices": [
            "To have staff available that speak different languages on each shift",
            "To have payment plan options that are based on financial need",
            "To have religious services offered at the facility daily",
            "To make decisions and participate in own care"
        ],
        "answer": "To make decisions and participate in own care"
    },
    {
        "q": "Which of the following, if observed as a sudden change in the resident, is considered a possible warning sign of a stroke?",
        "choices": ["Dementia", "Contractures", "Slurred speech", "Irregular heartbeat"],
        "answer": "Slurred speech"
    },
    {
        "q": "Considering the resident's activity, which of the following sets of vital signs should be reported to the charge nurse immediately?",
        "choices": [
            "Resting: 98.6°-98-32",
            "After eating: 97.0°-64-24",
            "After walking exercise: 98.2°-98-28",
            "While watching television: 98.8°-72-14"
        ],
        "answer": "Resting: 98.6°-98-32"
    }
]

skills_quiz = [
    {
        "q": "Before transferring a resident from bed to wheelchair, which safety step is critical?",
        "choices": ["Offer juice first", "Lock the wheels", "Raise the bed to the highest point", "Remove footwear"],
        "answer": "Lock the wheels",
        "rationale": "Unlocked equipment can move and create fall risk."
    },
    {
        "q": "For urinary output measurement, what improves accuracy?",
        "choices": ["Estimate visually", "Read at eye level in a graduate", "Chart before measuring", "Discard before reading"],
        "answer": "Read at eye level in a graduate",
        "rationale": "Eye-level measurement is more accurate."
    },
    {
        "q": "During handwashing, which step helps avoid contamination?",
        "choices": ["Touch the inside sink after washing", "Keep fingertips pointed down when rinsing", "Dry hands on clothing", "Skip soap if rushed"],
        "answer": "Keep fingertips pointed down when rinsing",
        "rationale": "This helps keep runoff away from cleaner areas."
    },
    {
        "q": "What should happen if a resident becomes weak during a transfer?",
        "choices": ["Force the transfer", "Ignore it and continue", "Protect the resident and call for help", "Leave the resident alone"],
        "answer": "Protect the resident and call for help",
        "rationale": "Resident safety comes first during any change in condition."
    },
    {
        "q": "During feeding skill, verified checklist guidance says to offer fluids:",
        "choices": ["Only at start of meal", "Only at end of meal", "At least every 2-3 bites", "Only if resident requests"],
        "answer": "At least every 2-3 bites",
        "rationale": "Prometric feeding checkpoint specifies offering fluids throughout feeding at least every 2-3 bites."
    },
    {
        "q": "For bed-to-wheelchair pivot transfer, what must be done before standing?",
        "choices": ["Remove shoes", "Move footrests out of the way", "Keep wheelchair far from bed", "Skip gait belt"],
        "answer": "Move footrests out of the way",
        "rationale": "Prometric transfer checklist includes moving footrests and preparing a close, safe pivot setup."
    },
    {
        "q": "In female catheter care, correct cleansing direction is:",
        "choices": ["Back to front", "Side to side", "Front to back", "Any direction if rinsed"],
        "answer": "Front to back",
        "rationale": "Prometric checklist requires front-to-back cleansing and cleaning catheter away from the body."
    },
    {
        "q": "On Texas test day, what arrival time does the CIB recommend?",
        "choices": ["Exactly at start time", "10 minutes early", "At least 30 minutes early", "1 hour early only for oral exam"],
        "answer": "At least 30 minutes early",
        "rationale": "Texas CIB advises arriving at least 30 minutes before the scheduled appointment."
    },
    {
        "q": "Which item is required for the Texas clinical skills exam attire?",
        "choices": ["Open-toe footwear", "Flat nonskid closed-toed shoes", "Business formal shoes", "Socks only"],
        "answer": "Flat nonskid closed-toed shoes",
        "rationale": "The Texas CIB requires flat, nonskid, closed-toed shoes for the clinical skills test."
    },
    {
        "q": "If a candidate is absent or too late for Texas CNA testing, the CIB says they are treated as:",
        "choices": ["Auto-rescheduled free", "Deferred with no fee", "No show and must pay exam fee to reschedule", "Passed written but not skills"],
        "answer": "No show and must pay exam fee to reschedule",
        "rationale": "Texas CIB indicates absent/late candidates are no-shows and must repay the exam fee to reschedule."
    },
    {
        "q": "Texas HHS curriculum emphasizes which sequence during routine care findings?",
        "choices": ["Document, then observe", "Observe, report, and document to the nurse", "Report only if family requests", "Observe only unusual behaviors"],
        "answer": "Observe, report, and document to the nurse",
        "rationale": "Procedural guidelines in the Texas HHS CNA manual emphasize observing, reporting, and documenting findings to the nurse."
    },
    {
        "q": "For certification renewal standards noted in the Texas HHS manual, nurse aides need in-service education every two years of:",
        "choices": ["12 hours", "16 hours", "20 hours", "24 hours"],
        "answer": "24 hours",
        "rationale": "The curriculum notes 24 hours of in-service education every two years for renewal standards."
    },
    {
        "q": "Which answer matches person-centered care principles in the Texas HHS manual?",
        "choices": ["Set one schedule for all residents", "Respect each resident's care and activity preferences", "Do tasks without explanation", "Limit resident choices to save time"],
        "answer": "Respect each resident's care and activity preferences",
        "rationale": "Person-centered care in the Texas HHS curriculum focuses on honoring resident preferences, dignity, and choices."
    }
]

clinical_skills = {
    "Texas HHS Curriculum Essentials (Verified)": [
        "Start each care interaction with person-centered communication and resident choice.",
        "Protect and promote resident rights, privacy, and dignity at all times.",
        "Use hand hygiene and infection-control practices before and after care.",
        "Integrate safety checks when entering and leaving resident care areas.",
        "Apply OBRA-aligned focus: restorative, psychosocial, and preventive care.",
        "Observe resident status continuously and identify changes from baseline.",
        "Report and document findings to the supervising nurse accurately and promptly.",
        "CRITICAL SAFETY STEP: Complete only trained/proficient tasks and escalate concerns immediately to the nurse."
    ],
    "Texas CIB Exam Essentials (Verified)": [
        "Arrive at least 30 minutes before your scheduled testing appointment.",
        "Bring ATT letter, one current government-issued photo ID with signature, and a second matching ID.",
        "Wear flat, nonskid, closed-toed shoes for the clinical skills test.",
        "Understand that five skills are scored (three assigned skills plus Handwashing and Indirect Care).",
        "Pass all five scored skills to pass the clinical skills exam.",
        "Complete the written test as 60 multiple-choice questions in 90 minutes.",
        "Know attempt limits: three attempts each for skills and written/oral within 24 months.",
        "CRITICAL SAFETY STEP: Follow test-site rules and required identification exactly to avoid denial/no-show status."
    ],
    "Prometric Indirect Care (Verified)": [
        "Greet resident, address by name, and introduce yourself.",
        "Explain care before beginning and during care.",
        "Ask resident preferences during care.",
        "Use standard precautions and infection-control measures.",
        "Ask about comfort/needs during care and before completion.",
        "Promote resident rights during care.",
        "CRITICAL SAFETY STEP: Promote resident safety throughout all care tasks."
    ],
    "Handwashing": [
        "Wet hands and wrists under warm running water.",
        "Apply soap.",
        "Lather all surfaces, including between fingers.",
        "Rub for at least 20 seconds.",
        "Clean fingertips and nails.",
        "Rinse with fingertips pointed downward.",
        "Dry with clean paper towel.",
        "Use paper towel to turn off faucet.",
        "CRITICAL SAFETY STEP: Do not recontaminate clean hands by touching the sink or faucet directly."
    ],
    "Measuring & Recording Blood Pressure": [
        "Identify the resident and explain the skill.",
        "Position the arm correctly at heart level.",
        "Apply the cuff to the bare upper arm.",
        "Place the stethoscope over the brachial artery.",
        "Inflate and deflate cuff carefully.",
        "Identify systolic and diastolic values.",
        "Record the reading accurately.",
        "CRITICAL SAFETY STEP: Report abnormal or concerning findings according to policy."
    ],
    "Measuring & Recording Urinary Output": [
        "Explain the procedure and provide privacy.",
        "Put on gloves.",
        "Pour urine into the graduate without spilling.",
        "Read at eye level.",
        "Discard and clean equipment per instructions.",
        "Remove gloves.",
        "Perform hand hygiene.",
        "Record the exact amount measured.",
        "CRITICAL SAFETY STEP: Record the measured amount, not an estimate."
    ],
    "Transfer: Bed to Wheelchair": [
        "Identify the resident and explain the procedure.",
        "Provide non-skid footwear if indicated.",
        "Position wheelchair correctly.",
        "Lock the bed wheels and wheelchair wheels.",
        "Adjust bed height for safe transfer.",
        "Use gait belt if required by care approach.",
        "Pivot safely and lower resident into wheelchair.",
        "Ensure resident is aligned and comfortable.",
        "CRITICAL SAFETY STEP: Lock equipment before movement begins."
    ]
}

study_tracks = [
    {
        "title": "Role of the Nurse Aide",
        "items": [
            "Work under nurse supervision and follow the care plan.",
            "Observe and report changes in resident condition.",
            "Support comfort, safety, dignity, and independence.",
            "Document accurately after care tasks are completed."
        ]
    },
    {
        "title": "Resident Rights",
        "items": [
            "Protect privacy and dignity during all care.",
            "Respect choice, confidentiality, and respectful treatment.",
            "Recognize and report abuse, neglect, or property concerns.",
            "Promote informed participation in care whenever possible."
        ]
    },
    {
        "title": "Infection Prevention & PPE",
        "items": [
            "Perform hand hygiene before and after care.",
            "Use gloves and PPE according to task and exposure risk.",
            "Handle soiled items carefully to reduce spread.",
            "Maintain annual infection-control training awareness."
        ]
    },
    {
        "title": "Communication & Mental Health",
        "items": [
            "Use clear, calm, respectful communication.",
            "Adapt communication for hearing, vision, or cognitive needs.",
            "Use reassurance and redirection with confused residents.",
            "Observe and report behavior or mood changes."
        ]
    },
    {
        "title": "Basic Nursing Skills",
        "items": [
            "Measure and record vital signs and outputs accurately.",
            "Observe pain, weakness, breathing changes, skin concerns, and dizziness.",
            "Use proper body mechanics and safety setup.",
            "Report significant changes promptly."
        ]
    },
    {
        "title": "Restorative Care",
        "items": [
            "Encourage residents to do what they can safely do.",
            "Support mobility, grooming, feeding, and function.",
            "Use assistive devices safely.",
            "Help preserve independence and quality of life."
        ]
    },
    {
        "title": "Dementia / Alzheimer's Support",
        "items": [
            "Approach calmly and reduce environmental stress.",
            "Use short, simple directions and reassurance.",
            "Redirect rather than argue.",
            "Protect safety and maintain respect."
        ]
    }
]

renewal_rules = [
    "Texas nurse aides renew on a 24-month cycle.",
    "The 90-day TULIP action window opens before expiration.",
    "At least 24 hours of in-service education are expected every two years.",
    "Education should include geriatrics and dementia / Alzheimer's-related content.",
    "Annual infection-control training should also be maintained.",
    "Form 5506-NAR workflow can support employment verification needs."
]

tulip_coach_steps = [
    "Sign in to TULIP and confirm your profile details.",
    "Review certificate number, name, and contact information.",
    "Check your expiration date and confirm your renewal window timing.",
    "Confirm your in-service records, including required topic coverage.",
    "Gather any employer verification information needed for renewal workflow.",
    "Upload required documents if the portal requests them.",
    "Review the summary page carefully before final submission.",
    "Save or print your confirmation details for your records."
]

common_delay_mistakes = [
    "Waiting until the last minute after the 90-day window opens.",
    "Not tracking in-service hours throughout the full 24-month period.",
    "Missing geriatrics, dementia, or infection-control documentation.",
    "Entering profile or certificate information incorrectly.",
    "Failing to follow up on TULIP messages or deficiencies.",
    "Not coordinating employer verification early enough."
]

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="main-hero">
    <h1>🩺 TULIP-Link CNA Academy</h1>
    <div>Study tools, flashcards, and TULIP renewal guidance built for Texas nurse aides and facility teams.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card welcome-login">
    <div class="welcome-copy">
        <h2>Welcome to Your CNA Learning Home</h2>
        <p>Thank you for your service and your commitment to safe, compassionate care.</p>
        <p>This space is built to support you with confidence, clarity, and a friendly step-by-step path for studying and renewal.</p>
        <p>Whether you are preparing for exams, staying current with CEUs, or guiding your team, we are glad you are here.</p>
        <div class="welcome-note">You make a real difference every shift. We appreciate you.</div>
    </div>
    <div class="cna-carousel" aria-label="CNA and nurse smiling carousel">
        <img src="https://images.unsplash.com/photo-1584515933487-779824d29309?auto=format&fit=crop&w=1400&q=80" alt="Smiling nurse with confidence" />
        <img src="https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1400&q=80" alt="Caring healthcare professionals smiling" />
        <img src="https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=1400&q=80" alt="Nurses smiling in clinical setting" />
        <img src="https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=1400&q=80" alt="Friendly nurse team portrait" />
        <img src="https://images.unsplash.com/photo-1612277795421-9bc7706a4a41?auto=format&fit=crop&w=1400&q=80" alt="Healthcare worker smiling with patient care focus" />
    </div>
</div>
""", unsafe_allow_html=True)

# Heartbeat card
st.write("""
<div style="background:#ECFEFF;border:2px solid #67E8F9;border-radius:12px;padding:20px 24px;margin:16px 0;">
  <h3 style="margin:0 0 8px 0;color:#0e7490;">💚 CNAs Are The Heartbeat Of Healthcare</h3>
  <p style="margin:0;color:#164e63;">Thank you for the care, patience, and courage you bring to every shift.</p>
</div>
""", unsafe_allow_html=True)

# Mission card
st.write("""
<div style="background:#fff;border:1.5px solid #0e7490;border-radius:12px;padding:20px 24px;margin:16px 0;">
  <h3 style="margin:0 0 8px 0;color:#0e7490;">🎯 Our Mission</h3>
  <p style="margin:0;color:#1e293b;">To elevate and empower CNAs and CNA students by providing the clarity, tools, and mentorship needed to master clinical skills, excel on the frontline, and confidently advance their healthcare journeys.</p>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("Navigation")
    glass_mode = st.toggle("Dark Glass Theme", value=st.session_state.ui_theme == "glass", key="glass_theme_toggle")
    selected_theme = "glass" if glass_mode else "light"
    if selected_theme != st.session_state.ui_theme:
        st.session_state.ui_theme = selected_theme
        st.rerun()

    view = st.radio(
        "Choose your path",
        [
            "View A: Texas CNA Academy",
            "View B: CNA CEUs & TULIP-Link",
            "View C: DON or Instructors & Facility Dashboard"
        ]
    )
    st.markdown("---")
    if view == "View A: Texas CNA Academy":
        st.caption("Practice flashcards, written questions, and clinical skills review for CNA certification.")
    elif view == "View B: CNA CEUs & TULIP-Link":
        st.caption("Track renewal progress, review in-service requirements, and stay ready for the TULIP window.")
    else:
        st.caption("Monitor facility-level DON compliance, verification tasks, and CNA renewal support workflows.")
    st.markdown("---")
    st.caption("Lesson intro videos can be updated in chapter_videos.json")
    st.markdown("---")
    st.caption("Built for students, active CNAs, and nursing facility leadership.")
    st.markdown("### Quick start")
    st.write(
        "- Pick the view that matches your role\n"
        "- Use flashcard categories to focus study\n"
        "- Track readiness progress before test or renewal"
    )

# =========================================================
# VIEW A
# =========================================================
if view == "View A: Texas CNA Academy":
    st.subheader("Texas CNA Academy")
    st.markdown(
        '<div class="info-card">Focus on mastery, practice written questions, and simulate clinical skill checklists. Use the tabs to keep your review structured and efficient.</div>',
        unsafe_allow_html=True
    )
    st.info(PROMETRIC_SKILLS_TRUST_NOTE)
    render_view_visuals("a")

    mastered = len(st.session_state.mastered_cards)
    total_flash = len(flashcards)
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

    readiness_total = len(flashcards) + len(written_quiz) + len(skills_quiz)
    readiness_points = mastered + written_score + skills_score
    readiness_pct = pct(readiness_points, readiness_total)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="kpi">{mastered}/{total_flash}</div><div class="label">Flashcards Mastered</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="kpi">{written_score}/{len(written_quiz)}</div><div class="label">Written Quiz Score</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="kpi">{skills_score}/{len(skills_quiz)}</div><div class="label">Skills Quiz Score</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Test Readiness Progress")
    st.progress(readiness_pct / 100)
    st.write(f"Readiness score: **{readiness_pct}%**")
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "Study Tracks",
        "Flashcards",
        "Written Quiz",
        "Clinical Skills",
        "Skills Quiz",
        "Curriculum Modules",
        "Study Plan",
        "Exam Tips",
        "Texas CNA Success",
        "Prometric Sample Test"
    ])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Texas Study Tracks")
        for track in study_tracks:
            with st.expander(track["title"], expanded=False):
                for item in track["items"]:
                    st.write(f"- {item}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Interactive Flashcards")
        st.markdown('<div class="info-card">Select a category, flip cards to see the answer, then mark cards as mastered or for review.</div>', unsafe_allow_html=True)

        categories = ["All Categories"] + sorted({card["category"] for card in flashcards})
        c1, c2 = st.columns([2, 1])
        with c1:
            category = st.selectbox("Filter by category", categories, key="flash_category")
            if st.button("Reset to All Categories", use_container_width=True):
                st.session_state.flash_category = "All Categories"
                st.session_state.flash_category_prev = "All Categories"
                st.session_state.flash_index = 0
                st.session_state.flash_flip = False
                st.rerun()
            if category != "All Categories":
                st.caption(category_descriptions.get(category, ""))
            else:
                st.caption("Browse all flashcards or pick a category to focus your study.")
        with c2:
            total_cards = len(flashcards)
            filtered_count = sum(1 for card in flashcards if category == "All Categories" or card["category"] == category)
            st.metric("Category", category)
            st.metric("Visible cards", f"{filtered_count}/{total_cards}")

        if st.session_state.flash_category != st.session_state.flash_category_prev:
            st.session_state.flash_index = 0
            st.session_state.flash_flip = False
            st.session_state.flash_category_prev = st.session_state.flash_category

        filtered_flashcards = [
            (idx, card)
            for idx, card in enumerate(flashcards)
            if category == "All Categories" or card["category"] == category
        ]

        if not filtered_flashcards:
            st.warning("No flashcards match that category. Please choose another category.")
        else:
            main_col, tip_col = st.columns([3, 1])
            with main_col:
                if st.session_state.flash_index >= len(filtered_flashcards):
                    st.session_state.flash_index = 0

                card_index, card = filtered_flashcards[st.session_state.flash_index]
                st.caption(f"Card {st.session_state.flash_index + 1} of {len(filtered_flashcards)} • {card['category']}")

                st.markdown(
                    f"""
                    <div class="soft-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
                            <span style="font-size:0.95rem; color:#000000; font-weight:700;">{card['category']}</span>
                            <span style="font-size:0.90rem; color:#000000;">{st.session_state.flash_index + 1}/{len(filtered_flashcards)}</span>
                        </div>
                        <h3>{'Answer' if st.session_state.flash_flip else 'Question'}</h3>
                        <p class="small-muted">Tap the card below to flip.</p>
                    </div>
                    """, unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="flashcard-state">Showing: <strong>{"Answer" if st.session_state.flash_flip else "Question"}</strong></div>',
                    unsafe_allow_html=True
                )

                flashcard_bg = "#ffffff"
                flashcard_border = "#111827" if st.session_state.flash_flip else "#d1d5db"
                flashcard_font_size = "1.22rem" if st.session_state.flash_flip else "1.42rem"
                flashcard_font_weight = "700" if st.session_state.flash_flip else "800"
                st.markdown(
                    f"""
                    <style>
                    .st-key-flashcard_touch button {{
                        background:{flashcard_bg} !important;
                        border-color:{flashcard_border} !important;
                        color:#111827 !important;
                        font-size:{flashcard_font_size} !important;
                        font-weight:{flashcard_font_weight} !important;
                        line-height:1.55 !important;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                flash_label = f"{'Answer' if st.session_state.flash_flip else 'Question'}\n\n{card['back'] if st.session_state.flash_flip else card['front']}"
                if st.button(flash_label, key="flashcard_touch", use_container_width=True):
                    st.session_state.flash_flip = not st.session_state.flash_flip
                    st.rerun()

                progress = (st.session_state.flash_index + 1) / len(filtered_flashcards)
                st.progress(progress)

                nav_col1, nav_col2 = st.columns([1, 1])
                with nav_col1:
                    if st.button("🩺 Previous", use_container_width=True):
                        st.session_state.flash_index = (st.session_state.flash_index - 1) % len(filtered_flashcards)
                        st.session_state.flash_flip = False
                        st.rerun()
                with nav_col2:
                    if st.button("Next 🩺", use_container_width=True):
                        st.session_state.flash_index = (st.session_state.flash_index + 1) % len(filtered_flashcards)
                        st.session_state.flash_flip = False
                        st.rerun()

                action_col1, action_col2 = st.columns([1, 1])
                with action_col1:
                    if st.button("Mastered", use_container_width=True):
                        st.session_state.mastered_cards.add(card_index)
                        st.session_state.review_cards.discard(card_index)
                        st.success("Marked as mastered.")
                with action_col2:
                    if st.button("Needs Review", use_container_width=True):
                        st.session_state.review_cards.add(card_index)
                        st.session_state.mastered_cards.discard(card_index)
                        st.warning("Marked for review.")

                st.markdown(
                    f"<div class='soft-card' style='padding:0.9rem; background:#f8fafc;'>Mastered: <strong>{len(st.session_state.mastered_cards)}</strong> | Review: <strong>{len(st.session_state.review_cards)}</strong></div>",
                    unsafe_allow_html=True
                )

            with tip_col:
                review_counts = {}
                for idx in st.session_state.review_cards:
                    if 0 <= idx < len(flashcards):
                        cat = flashcards[idx]["category"]
                        review_counts[cat] = review_counts.get(cat, 0) + 1

                current_category_review = 0
                if category != "All Categories":
                    current_category_review = sum(
                        1
                        for idx in st.session_state.review_cards
                        if 0 <= idx < len(flashcards) and flashcards[idx]["category"] == category
                    )

                top_review_category = None
                if review_counts:
                    top_review_category = max(review_counts, key=review_counts.get)

                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown('### Flashcard Focus Summary')
                st.write(f'- Mastered cards: **{len(st.session_state.mastered_cards)}**')
                st.write(f'- Review cards: **{len(st.session_state.review_cards)}**')
                if top_review_category:
                    st.write(f'- Most review cards are in **{top_review_category}** ({review_counts[top_review_category]})')
                else:
                    st.write('- No review cards yet — keep studying and mark anything you want to revisit.')
                if category != "All Categories":
                    st.write(f'- Review cards in this category: **{current_category_review}**')
                if top_review_category and category != top_review_category:
                    st.write(f'- Suggested next focus: **{top_review_category}**')
                st.markdown('---')
                st.markdown('### Texas CNA Study Tips')
                st.write('- Focus on infection control, resident rights, and safe transfers first.')
                st.write('- Speak the answer out loud to help embed the state exam language.')
                st.write('- Use the review flag for cards that mention policy, safety, or documentation.')
                st.write('- Aim for steady progress across categories, not just one topic area.')
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Written Practice Quiz")
        st.caption(f"Verified skills-source alignment: {PROMETRIC_VERIFIED_ALIGNMENT_LABEL}")
        written_key = "written_quiz_submitted"
        if written_key not in st.session_state:
            st.session_state[written_key] = False

        timed_written = st.toggle("Enable timed mode (10 minutes)", key="written_timed_mode")
        if timed_written:
            t1, t2 = st.columns(2)
            with t1:
                if st.button("Start / Restart Written Timer", use_container_width=True, key="start_written_timer"):
                    st.session_state.written_timer_started_at = datetime.now().isoformat()
                    st.rerun()
            with t2:
                if st.session_state.written_timer_started_at:
                    elapsed_written = int((datetime.now() - datetime.fromisoformat(st.session_state.written_timer_started_at)).total_seconds())
                    remaining_written = max(0, 600 - elapsed_written)
                    st.markdown(f"**Time left:** {format_duration(remaining_written)}")
                    if remaining_written == 0:
                        st.error("Time is up. Grade now or reset for a new timed attempt.")
                else:
                    st.markdown("**Timer status:** Not started")

        for i, item in enumerate(written_quiz):
            st.markdown(f"**Q{i+1}. {item['q']}**")
            ans = st.radio(
                f"Choose answer for written question {i+1}",
                item["choices"],
                key=f"written_{i}",
                index=None
            )
            if ans:
                st.session_state.written_answers[i] = ans
            st.markdown("---")

        answered_written = len(st.session_state.written_answers)
        st.markdown(f"**Progress:** {answered_written}/{len(written_quiz)} answered")
        st.progress(answered_written / len(written_quiz) if written_quiz else 0)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Grade Written Quiz", use_container_width=True, key="grade_written_quiz"):
                st.session_state[written_key] = True
                st.session_state.written_quiz_log_done = False
        with c2:
            if st.button("Reset Written Quiz", use_container_width=True, key="reset_written_quiz"):
                st.session_state.written_answers = {}
                st.session_state[written_key] = False
                st.session_state.written_timer_started_at = None
                st.session_state.written_quiz_log_done = False
                st.rerun()

        if st.session_state[written_key]:
            if answered_written < len(written_quiz):
                st.warning("Please answer all written quiz questions before grading.")
            else:
                score = sum(1 for i, q in enumerate(written_quiz) if st.session_state.written_answers.get(i) == q["answer"])
                pct_score = int((score / len(written_quiz)) * 100)

                elapsed_written = 0
                if timed_written and st.session_state.written_timer_started_at:
                    elapsed_written = int((datetime.now() - datetime.fromisoformat(st.session_state.written_timer_started_at)).total_seconds())

                if pct_score >= 80:
                    st.success(f"Written quiz score: {score}/{len(written_quiz)} ({pct_score}%). Excellent work.")
                else:
                    st.warning(f"Written quiz score: {score}/{len(written_quiz)} ({pct_score}%). Review rationales and retry.")

                if timed_written:
                    if not st.session_state.written_timer_started_at:
                        st.warning("Timed mode was enabled, but timer was not started.")
                    else:
                        time_status = "within" if elapsed_written <= 600 else "over"
                        st.info(f"Timed attempt duration: {format_duration(elapsed_written)} ({time_status} the 10-minute target).")

                if not st.session_state.written_quiz_log_done:
                    history = st.session_state.quiz_history
                    history.setdefault("written", []).append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "score": score,
                        "total": len(written_quiz),
                        "percent": pct_score,
                        "timed_mode": timed_written,
                        "duration": format_duration(elapsed_written) if timed_written and st.session_state.written_timer_started_at else "--:--"
                    })
                    st.session_state.quiz_history = history
                    st.session_state.written_quiz_log_done = True

                for i, item in enumerate(written_quiz):
                    selected = st.session_state.written_answers.get(i)
                    if selected == item["answer"]:
                        st.success(f"Q{i+1}: Correct. {item['rationale']}")
                    else:
                        st.error(f"Q{i+1}: Incorrect. Correct answer: {item['answer']}. {item['rationale']}")
        elif len(st.session_state.written_answers) == len(written_quiz):
            score = sum(1 for i, q in enumerate(written_quiz) if st.session_state.written_answers.get(i) == q["answer"])
            st.info(f"Written quiz score: {score}/{len(written_quiz)}")

        st.markdown("---")
        render_quiz_history_panel("written", "Written Quiz History")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Clinical Skills Checklists")
        st.caption(f"Verified skills-source alignment: {PROMETRIC_VERIFIED_ALIGNMENT_LABEL}")
        chosen_skill = st.selectbox("Choose a Prometric-style skill", list(clinical_skills.keys()))
        st.markdown('<div class="info-card">Focus especially on hand hygiene, privacy, communication, safe setup, accurate measurement, and reporting concerns.</div>', unsafe_allow_html=True)

        for idx, step in enumerate(clinical_skills[chosen_skill]):
            key = f"{chosen_skill}_{idx}"
            c1, c2 = st.columns([0.08, 0.92])
            with c1:
                checked = st.checkbox("", key=key)
                st.session_state.skills_checks[key] = checked
            with c2:
                if "CRITICAL SAFETY STEP" in step:
                    st.markdown(f'<div class="check-step"><span class="critical">{step}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="check-step">{step}</div>', unsafe_allow_html=True)

        completed = sum(
            1 for idx, _ in enumerate(clinical_skills[chosen_skill])
            if st.session_state.skills_checks.get(f"{chosen_skill}_{idx}", False)
        )
        st.write(f"Checklist completion: **{completed}/{len(clinical_skills[chosen_skill])}**")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Skills Quiz")
        st.caption(f"Verified skills-source alignment: {PROMETRIC_VERIFIED_ALIGNMENT_LABEL}")
        skills_key = "skills_quiz_submitted"
        if skills_key not in st.session_state:
            st.session_state[skills_key] = False

        timed_skills = st.toggle("Enable timed mode (10 minutes)", key="skills_timed_mode")
        if timed_skills:
            t1, t2 = st.columns(2)
            with t1:
                if st.button("Start / Restart Skills Timer", use_container_width=True, key="start_skills_timer"):
                    st.session_state.skills_timer_started_at = datetime.now().isoformat()
                    st.rerun()
            with t2:
                if st.session_state.skills_timer_started_at:
                    elapsed_skills = int((datetime.now() - datetime.fromisoformat(st.session_state.skills_timer_started_at)).total_seconds())
                    remaining_skills = max(0, 600 - elapsed_skills)
                    st.markdown(f"**Time left:** {format_duration(remaining_skills)}")
                    if remaining_skills == 0:
                        st.error("Time is up. Grade now or reset for a new timed attempt.")
                else:
                    st.markdown("**Timer status:** Not started")

        for i, item in enumerate(skills_quiz):
            st.markdown(f"**Q{i+1}. {item['q']}**")
            ans = st.radio(
                f"Choose answer for skills question {i+1}",
                item["choices"],
                key=f"skills_{i}",
                index=None
            )
            if ans:
                st.session_state.skills_answers[i] = ans
            st.markdown("---")

        answered_skills = len(st.session_state.skills_answers)
        st.markdown(f"**Progress:** {answered_skills}/{len(skills_quiz)} answered")
        st.progress(answered_skills / len(skills_quiz) if skills_quiz else 0)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Grade Skills Quiz", use_container_width=True, key="grade_skills_quiz"):
                st.session_state[skills_key] = True
                st.session_state.skills_quiz_log_done = False
        with c2:
            if st.button("Reset Skills Quiz", use_container_width=True, key="reset_skills_quiz"):
                st.session_state.skills_answers = {}
                st.session_state[skills_key] = False
                st.session_state.skills_timer_started_at = None
                st.session_state.skills_quiz_log_done = False
                st.rerun()

        if st.session_state[skills_key]:
            if answered_skills < len(skills_quiz):
                st.warning("Please answer all skills quiz questions before grading.")
            else:
                score = sum(1 for i, q in enumerate(skills_quiz) if st.session_state.skills_answers.get(i) == q["answer"])
                pct_score = int((score / len(skills_quiz)) * 100)

                elapsed_skills = 0
                if timed_skills and st.session_state.skills_timer_started_at:
                    elapsed_skills = int((datetime.now() - datetime.fromisoformat(st.session_state.skills_timer_started_at)).total_seconds())

                if pct_score >= 80:
                    st.success(f"Skills quiz score: {score}/{len(skills_quiz)} ({pct_score}%). Strong clinical judgment.")
                else:
                    st.warning(f"Skills quiz score: {score}/{len(skills_quiz)} ({pct_score}%). Review safety-focused rationales and retry.")

                if timed_skills:
                    if not st.session_state.skills_timer_started_at:
                        st.warning("Timed mode was enabled, but timer was not started.")
                    else:
                        time_status = "within" if elapsed_skills <= 600 else "over"
                        st.info(f"Timed attempt duration: {format_duration(elapsed_skills)} ({time_status} the 10-minute target).")

                if not st.session_state.skills_quiz_log_done:
                    history = st.session_state.quiz_history
                    history.setdefault("skills", []).append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "score": score,
                        "total": len(skills_quiz),
                        "percent": pct_score,
                        "timed_mode": timed_skills,
                        "duration": format_duration(elapsed_skills) if timed_skills and st.session_state.skills_timer_started_at else "--:--"
                    })
                    st.session_state.quiz_history = history
                    st.session_state.skills_quiz_log_done = True

                for i, item in enumerate(skills_quiz):
                    selected = st.session_state.skills_answers.get(i)
                    if selected == item["answer"]:
                        st.success(f"Q{i+1}: Correct. {item['rationale']}")
                    else:
                        st.error(f"Q{i+1}: Incorrect. Correct answer: {item['answer']}. {item['rationale']}")
        elif len(st.session_state.skills_answers) == len(skills_quiz):
            score = sum(1 for i, q in enumerate(skills_quiz) if st.session_state.skills_answers.get(i) == q["answer"])
            st.info(f"Skills quiz score: {score}/{len(skills_quiz)}")

        st.markdown("---")
        render_quiz_history_panel("skills", "Skills Quiz History")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab6:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Curriculum Modules")
        st.markdown(
            '<div class="study-hero"><strong>Course Experience:</strong> Learn by lesson, track progress, and take chapter quizzes in one clean flow.</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="crumbs">Home / Texas CNA Academy / Curriculum Modules</div>', unsafe_allow_html=True)

        chapters = get_all_chapters()
        all_titles = [title for title, _ in chapters]

        if not all_titles:
            st.warning("No lessons are available right now.")
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()

        if st.session_state.get("selected_chapter") not in all_titles:
            st.session_state.selected_chapter = all_titles[0]

        first_incomplete = next((title for title, _ in chapters if not st.session_state.chapter_progress.get(title, False)), all_titles[0])
        continue_target = st.session_state.get("last_selected_chapter") if st.session_state.get("last_selected_chapter") in all_titles else first_incomplete

        cta1, cta2 = st.columns([2, 1])
        with cta1:
            target_name = continue_target.split(":", 1)[1].strip()
            st.markdown(f"**Continue recommendation:** {target_name}")
            st.caption("Use your last opened lesson or the next incomplete lesson to keep steady momentum.")
        with cta2:
            if st.button("Continue Where I Left Off", use_container_width=True, key="continue_lesson_button"):
                st.session_state.selected_chapter = continue_target
                st.rerun()

        complete, total = chapter_progress_summary()
        quiz_done_count = sum(
            1
            for title, module_info in chapters
            if len(st.session_state.chapter_quiz_answers.get(title, {})) == len(module_info.get("quiz", [])) and len(module_info.get("quiz", [])) > 0
        )

        search_term = st.text_input("Search lessons", placeholder="Try: infection, dementia, safety", key="module_search")
        filtered_chapters = [
            (title, module_info)
            for title, module_info in chapters
            if search_term.strip().lower() in title.lower() or search_term.strip().lower() in " ".join(module_info.get("key_topics", [])).lower()
        ] if search_term else chapters

        sequence_mode = st.toggle(
            "Enable sequence mode (lock future lessons)",
            key="module_sequence_mode",
            help="When enabled, learners unlock lessons by mastery (lesson complete + 80% quiz score)."
        )

        chapter_titles = [title for title, _ in filtered_chapters] if filtered_chapters else [title for title, _ in chapters]
        if st.session_state.get("selected_chapter") not in chapter_titles:
            st.session_state.selected_chapter = chapter_titles[0]

        first_incomplete_idx = next(
            (idx for idx, (title, module_info) in enumerate(chapters) if not chapter_mastered(title, module_info)),
            len(chapters) - 1
        )

        if sequence_mode:
            unlocked_titles = {title for idx, (title, _) in enumerate(chapters) if idx <= first_incomplete_idx}
            if st.session_state.selected_chapter not in unlocked_titles:
                st.session_state.selected_chapter = chapters[first_incomplete_idx][0]
                st.info("Sequence mode redirected you to the next lesson that is not yet mastered.")

        if st.session_state.selected_chapter not in chapter_titles:
            st.session_state.selected_chapter = chapter_titles[0]

        selected_chapter = st.selectbox("Choose a lesson", chapter_titles, key="selected_chapter")
        st.session_state.last_selected_chapter = selected_chapter
        module = get_module(selected_chapter)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="kpi">{complete}/{total}</div><div class="label">Lessons Completed</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="kpi">{quiz_done_count}</div><div class="label">Quizzes Finished</div></div>', unsafe_allow_html=True)
        with m3:
            pct_complete = int((complete / total) * 100) if total else 0
            st.markdown(f'<div class="metric-card"><div class="kpi">{pct_complete}%</div><div class="label">Course Progress</div></div>', unsafe_allow_html=True)

        st.progress(complete / total if total else 0)
        st.markdown("---")

        layout_cols = st.columns([1.05, 1.95, 0.9])
        left_col, right_col = layout_cols[0], layout_cols[1]

        with left_col:
            st.markdown("#### Lesson Library")
            source_for_list = filtered_chapters if filtered_chapters else chapters
            for title, module_info in source_for_list:
                chapter_title = title.split(":", 1)[1].strip()
                icon = lesson_icon_from_title(chapter_title)
                chapter_complete = st.session_state.chapter_progress.get(title, False)
                chapter_class = "complete" if chapter_complete else "pending"
                if title == selected_chapter:
                    chapter_class += " active"
                list_index = all_titles.index(title)
                is_unlocked = (not sequence_mode) or (list_index <= first_incomplete_idx)
                quiz_total = len(module_info.get("quiz", []))
                quiz_answers = len(st.session_state.chapter_quiz_answers.get(title, {}))
                quiz_done = quiz_total > 0 and quiz_answers == quiz_total
                mastery_pct = chapter_quiz_percent(title, module_info)
                mastered = chapter_mastered(title, module_info)
                complete_chip = "<span class=\"lesson-chip done\">Complete</span>" if chapter_complete else "<span class=\"lesson-chip todo\">In Progress</span>"
                quiz_chip = "<span class=\"lesson-chip done\">Quiz Done</span>" if quiz_done else "<span class=\"lesson-chip todo\">Quiz Pending</span>"
                lock_chip = "<span class=\"lesson-chip done\">Unlocked</span>" if is_unlocked else "<span class=\"lesson-chip todo\">Locked</span>"
                mastery_chip = "<span class=\"lesson-chip done\">Mastered</span>" if mastered else "<span class=\"lesson-chip todo\">Not Mastered</span>"
                if quiz_total > 0:
                    lesson_progress = int(((1 if chapter_complete else 0) * 40) + ((quiz_answers / quiz_total) * 30) + (mastery_pct * 0.3))
                else:
                    lesson_progress = 100 if chapter_complete else 0

                st.markdown(
                    f'''
                    <div class="lesson-card {chapter_class}">
                        <div class="lesson-title">{icon} Chapter {module_info['chapter_number']}: {chapter_title}</div>
                        <div>{complete_chip}{quiz_chip}{mastery_chip}{lock_chip}</div>
                        <div class="mini-progress-track"><div class="mini-progress-fill" style="width:{lesson_progress}%;"></div></div>
                        <div class="lesson-meta">Estimated time: {module_info['duration_hours']} hr • Topics: {len(module_info.get("key_topics", []))}</div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
                if st.button("Open Lesson", key=f"open_lesson_{module_info['chapter_number']}", use_container_width=True, disabled=not is_unlocked):
                    st.session_state.selected_chapter = title
                    st.rerun()

        with right_col:
            if module:
                chapter_name = selected_chapter.split(":", 1)[1].strip()
                chapter_icon = lesson_icon_from_title(chapter_name)
                chapter_image = chapter_thumbnail_from_title(chapter_name)
                chapter_video = chapter_video_from_module(module["chapter_number"])
                quiz_total_for_header = len(module.get("quiz", []))
                quiz_answered_for_header = len(st.session_state.chapter_quiz_answers.get(selected_chapter, {}))
                if quiz_total_for_header > 0:
                    lesson_completion_pct = int(((1 if st.session_state.chapter_progress.get(selected_chapter, False) else 0) * 50) + ((quiz_answered_for_header / quiz_total_for_header) * 50))
                else:
                    lesson_completion_pct = 100 if st.session_state.chapter_progress.get(selected_chapter, False) else 0

                st.markdown(
                    f'<div class="sticky-study-header"><div style="font-weight:800; font-size:1.02rem;">Now Studying: {chapter_icon} Chapter {module["chapter_number"]}</div><div style="font-weight:700; margin-top:.15rem;">{chapter_name}</div><div class="small-muted">Study time: {module["duration_hours"]} hour(s) • Quiz questions: {len(module.get("quiz", []))} • Lesson progress: {lesson_completion_pct}%</div></div>',
                    unsafe_allow_html=True
                )
                st.markdown('<div class="chapter-thumbnail">', unsafe_allow_html=True)
                st.image(chapter_image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                with st.expander("Watch 60-second lesson intro", expanded=False):
                    st.video(chapter_video)

                current_index = all_titles.index(selected_chapter)
                nav1, nav2 = st.columns(2)
                with nav1:
                    if st.button("Previous Lesson", use_container_width=True, key=f"prev_lesson_{module['chapter_number']}", disabled=current_index == 0):
                        st.session_state.selected_chapter = all_titles[current_index - 1]
                        st.rerun()
                with nav2:
                    if st.button("Next Lesson", use_container_width=True, key=f"next_lesson_{module['chapter_number']}", disabled=current_index == len(all_titles) - 1):
                        st.session_state.selected_chapter = all_titles[current_index + 1]
                        st.rerun()

                action1, action2 = st.columns([1.2, 1])
                with action1:
                    was_complete = st.session_state.chapter_progress.get(selected_chapter, False)
                    chapter_complete = st.checkbox(
                        "Mark this lesson complete",
                        value=st.session_state.chapter_progress.get(selected_chapter, False),
                        key=f"chapter_complete_{module['chapter_number']}"
                    )
                    update_chapter_progress(selected_chapter, chapter_complete)
                    if chapter_complete and not was_complete:
                        st.success("Lesson completed. Great momentum!")
                        st.balloons()
                with action2:
                    if st.button("Open Quiz Section", use_container_width=True, key=f"open_quiz_{module['chapter_number']}"):
                        st.session_state[f"focus_quiz_{module['chapter_number']}"] = True

                lesson_tab1, lesson_tab2, lesson_tab3, lesson_tab4 = st.tabs([
                    "Overview",
                    "Lesson Content",
                    "Chapter Quiz",
                    "Case Studies & Scripts"
                ])

                if st.session_state.get(f"focus_quiz_{module['chapter_number']}"):
                    st.info("Open the 'Chapter Quiz' tab above to take or retake this lesson quiz.")
                    st.session_state[f"focus_quiz_{module['chapter_number']}"] = False

                with lesson_tab1:
                    st.markdown("### Key Topics")
                    st.write("- " + "\n- ".join(module["key_topics"]))
                    st.markdown("---")
                    st.markdown("### Suggested Study Flow")
                    st.write("1. Read the lesson content once for understanding.")
                    st.write("2. Re-read high-risk safety and reporting topics.")
                    st.write("3. Complete the chapter quiz and review rationales.")
                    st.write("4. Use related case studies to apply the chapter concepts.")

                with lesson_tab2:
                    content = load_markdown_content(module["file"])
                    st.markdown(content)

                with lesson_tab3:
                    chapter_quiz = module.get("quiz", [])
                    chapter_submit_key = f"chapter_quiz_submitted_{module['chapter_number']}"
                    if chapter_submit_key not in st.session_state:
                        st.session_state[chapter_submit_key] = False

                    for i, item in enumerate(chapter_quiz):
                        st.markdown(f"**Q{i+1}. {item['q']}**")
                        ans = st.radio(
                            f"Choose answer for chapter question {i+1}",
                            item["choices"],
                            key=f"chapter_{module['chapter_number']}_quiz_{i}",
                            index=None
                        )
                        if ans:
                            if selected_chapter not in st.session_state.chapter_quiz_answers:
                                st.session_state.chapter_quiz_answers[selected_chapter] = {}
                            st.session_state.chapter_quiz_answers[selected_chapter][i] = ans
                        st.markdown("---")

                    chapter_answers = st.session_state.chapter_quiz_answers.get(selected_chapter, {})
                    answered_chapter = len(chapter_answers)

                    if chapter_quiz:
                        st.markdown(f"**Progress:** {answered_chapter}/{len(chapter_quiz)} answered")
                        st.progress(answered_chapter / len(chapter_quiz))

                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("Grade Chapter Quiz", use_container_width=True, key=f"grade_chapter_quiz_{module['chapter_number']}"):
                                st.session_state[chapter_submit_key] = True
                        with c2:
                            if st.button("Reset Chapter Quiz", use_container_width=True, key=f"reset_chapter_quiz_{module['chapter_number']}"):
                                if selected_chapter in st.session_state.chapter_quiz_answers:
                                    st.session_state.chapter_quiz_answers[selected_chapter] = {}
                                st.session_state[chapter_submit_key] = False
                                st.rerun()

                        if st.session_state[chapter_submit_key]:
                            if answered_chapter < len(chapter_quiz):
                                st.warning("Please answer all chapter quiz questions before grading.")
                            else:
                                score = sum(
                                    1
                                    for i, item in enumerate(chapter_quiz)
                                    if chapter_answers.get(i) == item["answer"]
                                )
                                pct_score = int((score / len(chapter_quiz)) * 100)
                                if pct_score >= 80:
                                    st.success(f"Chapter quiz score: {score}/{len(chapter_quiz)} ({pct_score}%). Great chapter mastery.")
                                else:
                                    st.warning(f"Chapter quiz score: {score}/{len(chapter_quiz)} ({pct_score}%). Review this chapter and retake.")

                                for i, item in enumerate(chapter_quiz):
                                    selected = chapter_answers.get(i)
                                    if selected == item["answer"]:
                                        st.success(f"Q{i+1}: Correct. {item['rationale']}")
                                    else:
                                        st.error(f"Q{i+1}: Incorrect. Correct answer: {item['answer']}. {item['rationale']}")

                with lesson_tab4:
                    related_cases = [case for case in CASE_STUDIES if case["chapter"] == selected_chapter]
                    if related_cases:
                        st.markdown("### Related Case Studies")
                        for case in related_cases:
                            with st.expander(case["title"]):
                                st.write(case["scenario"])
                                st.write("**Best response:** " + case["answer"])
                                st.write(case["rationale"])
                        st.markdown("---")

                    chapter_key = selected_chapter.split(":", 1)[1].strip().lower()
                    templates = [
                        template for template in VIDEO_SCRIPT_TEMPLATES
                        if chapter_key in template.get("chapter", "").lower()
                        or chapter_key in template.get("objective", "").lower()
                        or chapter_key in template.get("title", "").lower()
                    ]
                    if templates:
                        st.markdown("### Video Script Templates")
                        for template in templates:
                            st.markdown(f"**{template['title']}**")
                            for line in template.get("script", []):
                                st.write(f"- {line}")
                            st.markdown("---")

                st.markdown("### Recommended Next Lessons")
                rec_slice = all_titles[current_index + 1: current_index + 4]
                if not rec_slice:
                    st.success("You are on the final lesson. Great work completing the curriculum path.")
                else:
                    rec_cols = st.columns(len(rec_slice))
                    for idx, rec_title in enumerate(rec_slice):
                        rec_module = get_module(rec_title)
                        if not rec_module:
                            continue
                        rec_name = rec_title.split(":", 1)[1].strip()
                        rec_icon = lesson_icon_from_title(rec_name)
                        rec_mastered = chapter_mastered(rec_title, rec_module)
                        rec_badge = "Mastered" if rec_mastered else "Continue"
                        with rec_cols[idx]:
                            st.markdown('<div class="rec-card">', unsafe_allow_html=True)
                            st.markdown(f"**{rec_icon} Chapter {rec_module['chapter_number']}**")
                            st.markdown(rec_name)
                            st.caption(f"{rec_module['duration_hours']} hr • {rec_badge}")
                            if st.button("Open", key=f"rec_open_{rec_module['chapter_number']}", use_container_width=True):
                                st.session_state.selected_chapter = rec_title
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Selected lesson module could not be loaded.")

        with layout_cols[2]:
            st.markdown('<div class="action-rail">', unsafe_allow_html=True)
            st.markdown("#### Lesson Actions")
            if module:
                mastery_now = chapter_quiz_percent(selected_chapter, module)
                mastered_now = chapter_mastered(selected_chapter, module)
                st.caption(f"Mastery: {mastery_now}%")
                st.caption("Target: 80% to unlock next lesson in sequence mode")
                if st.button("Take / Retake Quiz", key=f"rail_quiz_{module['chapter_number']}", use_container_width=True):
                    st.session_state[f"focus_quiz_{module['chapter_number']}"] = True
                    st.rerun()
                notes = f"Chapter {module['chapter_number']} Notes\n" + "- " + "\n- ".join(module.get("key_topics", []))
                st.download_button(
                    "Download Notes",
                    data=notes,
                    file_name=f"chapter_{module['chapter_number']}_notes.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key=f"rail_notes_{module['chapter_number']}"
                )
                if mastered_now:
                    st.success("Lesson mastered")
                else:
                    st.warning("Mastery not reached")
            else:
                st.caption("Select a lesson to view actions.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab7:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Study Plan")
        st.markdown('<div class="info-card">Track chapter progress, quiz completion, and identify the next chapters to review.</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card">Mark chapters complete as you finish them, then follow the suggested next chapters to stay on pace for Texas CNA exam readiness.</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card">Tip: start with the highlighted exam-critical chapters first, then use the table to confirm coverage of all 18 topics.</div>', unsafe_allow_html=True)

        chapters = get_all_chapters()
        chapter_rows = []
        next_chapters = []
        for title, module_info in chapters:
            completed = st.session_state.chapter_progress.get(title, False)
            quiz_complete = len(st.session_state.chapter_quiz_answers.get(title, {})) == len(module_info.get("quiz", []))
            chapter_rows.append({
                "Chapter": f"{module_info['chapter_number']}: {title.split(':', 1)[1].strip()}",
                "Completed": "Yes" if completed else "No",
                "Quiz Done": "Yes" if quiz_complete else "No"
            })
            if not completed and len(next_chapters) < 3:
                next_chapters.append(f"{module_info['chapter_number']}: {title.split(':', 1)[1].strip()}")

        completed, total = chapter_progress_summary()
        st.markdown(f"**Overall chapter progress:** {completed} of {total} complete")
        st.progress(completed / total if total else 0)
        st.markdown("---")

        st.markdown("### Next Chapters to Review")
        if next_chapters:
            for chapter in next_chapters:
                st.write(f"- {chapter}")
        else:
            st.success("All chapters are marked complete — excellent study discipline.")

        st.markdown("---")
        st.markdown("### Chapter Progress Tracker")
        st.table(chapter_rows)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab8:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Exam Tips")
        st.write("- Practice speaking each skill step out loud.")
        st.write("- Rehearse handwashing until the sequence feels automatic.")
        st.write("- Focus on safety setup before touching the resident.")
        st.write("- Protect privacy and communicate before, during, and after the skill.")
        st.write("- Read written questions carefully for safety, rights, and reporting clues.")
        st.write("- Watch for changes in condition and know what should be reported.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab9:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Texas CNA Success")
        st.write("- Build a routine: flashcards, one study track, and one quiz set each session.")
        st.write("- Repeat the high-risk safety steps until they are automatic.")
        st.write("- Practice documentation language that is factual and simple.")
        st.write("- Learn resident rights and infection prevention as priority content areas.")
        st.write("- Use the Renewal Hub after certification so you stay active in Texas.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab10:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Prometric Nurse Aide Certification Sample Test")
        st.caption("50-question sample test based on the Prometric Texas Nurse Aide Candidate Information Bulletin sample exam.")
        st.caption(f"Verified skills-source alignment: {PROMETRIC_VERIFIED_ALIGNMENT_LABEL}")

        sample_key = "prometric_sample_test_submitted"
        if sample_key not in st.session_state:
            st.session_state[sample_key] = False
        if "prometric_sample_answers" not in st.session_state:
            st.session_state.prometric_sample_answers = {}

        for i, item in enumerate(prometric_sample_test):
            st.markdown(f"**Q{i+1}. {item['q']}**")
            ans = st.radio(
                f"Choose answer for Prometric sample question {i+1}",
                item["choices"],
                key=f"prometric_sample_{i}",
                index=None
            )
            if ans:
                st.session_state.prometric_sample_answers[i] = ans
            st.markdown("---")

        answered_sample = len(st.session_state.prometric_sample_answers)
        st.markdown(f"**Progress:** {answered_sample}/{len(prometric_sample_test)} answered")
        st.progress(answered_sample / len(prometric_sample_test) if prometric_sample_test else 0)

        s1, s2 = st.columns(2)
        with s1:
            if st.button("Grade Sample Test", use_container_width=True, key="grade_prometric_sample_test"):
                st.session_state[sample_key] = True
        with s2:
            if st.button("Reset Sample Test", use_container_width=True, key="reset_prometric_sample_test"):
                st.session_state.prometric_sample_answers = {}
                st.session_state[sample_key] = False
                st.rerun()

        if st.session_state[sample_key]:
            if answered_sample < len(prometric_sample_test):
                st.warning("Please answer all sample test questions before grading.")
            else:
                sample_score = sum(
                    1 for i, item in enumerate(prometric_sample_test)
                    if st.session_state.prometric_sample_answers.get(i) == item["answer"]
                )
                sample_pct = int((sample_score / len(prometric_sample_test)) * 100)
                if sample_pct >= 80:
                    st.success(f"Sample test score: {sample_score}/{len(prometric_sample_test)} ({sample_pct}%).")
                else:
                    st.warning(f"Sample test score: {sample_score}/{len(prometric_sample_test)} ({sample_pct}%). Review the missed items and retry.")

                for i, item in enumerate(prometric_sample_test):
                    selected = st.session_state.prometric_sample_answers.get(i)
                    if selected == item["answer"]:
                        st.success(f"Q{i+1}: Correct.")
                    else:
                        st.error(f"Q{i+1}: Incorrect. Correct answer: {item['answer']}")

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# VIEW B
# =========================================================
# VIEW B
# =========================================================
elif view == "View B: CNA CEUs & TULIP-Link":
    st.subheader("🏥 CNA CEUs & TULIP-Link: Texas Renewal Center")
    st.markdown(
        '<div class="info-card">Complete step-by-step guidance for CNA renewal, required CEU courses, and Texas TULIP submission. Choose your path below.</div>',
        unsafe_allow_html=True
    )
    render_view_visuals("b")

    def render_professional_growth(pathway):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### 🌟 Professional Growth ({pathway} Path)")
        st.markdown("Use this section to build confidence, improve workplace performance, and plan your next career step.")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Next 30 Days")
            st.write("- Finish your required CEU plan and organize certificates in one folder.")
            st.write("- Practice concise shift reports using SBAR-style communication.")
            st.write("- Choose one high-impact topic to strengthen each week (safety, dementia care, documentation).")
            st.write("- Ask a charge nurse or mentor for one weekly feedback point to improve.")
        with c2:
            st.markdown("#### Career Toolkit")
            st.write("- Keep a one-page resume updated with current CEUs and care specialties.")
            st.write("- Prepare interview stories showing resident advocacy, teamwork, and reliability.")
            st.write("- Track measurable wins (attendance, quality notes, resident compliments).")
            st.write("- Build a realistic self-care plan to support consistency and avoid burnout.")

        st.divider()
        st.markdown("#### Professional Standards and Best Practices")
        for section, items in PROFESSIONAL_RECOMMENDATIONS.items():
            with st.expander(f"**{section}**"):
                for item in items:
                    st.write(f"- {item}")

        st.info(
            "Professional tip: Pair compliance progress (CEUs + TULIP) with one career-development goal each month so your license stays active and your opportunities keep growing."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    def render_monthly_ceu_reminder():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### 🗓️ {TODAY.strftime('%B %Y')} Monthly CEU Encouragement Reminder")
        st.markdown("Stay current every month by checking your CEU progress and renewal timeline below.")

        reminder_options = cna_df[cna_df["user_type"] != "Student"].copy()
        if reminder_options.empty:
            st.info("No CNA profiles are available for monthly reminders.")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        reminder_options["display"] = (
            reminder_options["first_name"] + " " + reminder_options["last_name"] + " • " + reminder_options["license_number"]
        )
        selected_name = st.selectbox(
            "Choose CNA for monthly reminder",
            reminder_options["display"].tolist(),
            key="monthly_reminder_cna_select"
        )
        selected = reminder_options[reminder_options["display"] == selected_name].iloc[0]

        summary = compliance_snapshot(selected["cna_id"], selected["expiration_date"], ceu_df)
        days_left = summary["days_left"]
        remaining_hours = max(0, 24 - summary["hours"])
        months_left = max(1, (max(days_left, 1) + 29) // 30)
        monthly_target_hours = 0 if remaining_hours == 0 else max(1, (remaining_hours + months_left - 1) // months_left)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="kpi">{summary["hours"]}/24</div><div class="label">CEU Hours Logged</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="kpi">{remaining_hours}</div><div class="label">Hours Remaining</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="kpi">{days_left}</div><div class="label">Days Until Expiration</div></div>', unsafe_allow_html=True)

        if days_left > 60:
            st.markdown(
                '<div class="soft-card" style="background:#dcfce7; border-left:4px solid #166534;"><strong>🎆🎇 Firecracker Celebration: You are staying current!</strong><br>Keep your momentum this month. Complete at least <strong>'
                + str(monthly_target_hours)
                + ' CEU hour(s)</strong> and keep all certificates organized for TULIP.</div>',
                unsafe_allow_html=True
            )
            st.success("Encouragement reminder: Great job staying ahead. Small monthly CEU wins protect your license and open more opportunities.")
        elif days_left > 30:
            st.markdown(
                '<div class="soft-card" style="background:#fffbeb; border-left:4px solid #b45309;"><strong>🚩 Yellow Flag Warning:</strong> You are within 60 days of renewal. Start or finish CEUs now so your TULIP submission is smooth.</div>',
                unsafe_allow_html=True
            )
            st.warning(f"Monthly reminder: Focus on at least {monthly_target_hours} CEU hour(s) this month and prepare your documents now.")
        elif days_left >= 0:
            st.markdown(
                '<div class="soft-card" style="background:#fee2e2; border-left:4px solid #b91c1c;"><strong>🚩 Red Flag Alert:</strong> Your license is within 30 days of expiration. Finish CEUs immediately and submit through TULIP as soon as possible.</div>',
                unsafe_allow_html=True
            )
            st.error("Urgent monthly reminder: Complete any remaining CEUs and submit renewal now to avoid expiration.")
        else:
            st.markdown(
                '<div class="soft-card" style="background:#fee2e2; border-left:4px solid #7f1d1d;"><strong>🚩 License Expired:</strong> Start reactivation steps immediately and contact Texas HHSC before TULIP submission.</div>',
                unsafe_allow_html=True
            )
            st.error("Critical reminder: Your license is expired. Use the Reactivation tabs now and contact HHSC for pathway confirmation.")

        st.info(
            f"This month\'s CEU target: **{monthly_target_hours} hour(s)**. Keep your course certificates in one folder and review your status at least once every month."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # License Status Selection
    st.markdown("### Your License Status")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✓ Active License", use_container_width=True, key="status_active"):
            st.session_state.license_status = "Active"
            st.rerun()
    with col2:
        if st.button("⚠ Expired License", use_container_width=True, key="status_expired"):
            st.session_state.license_status = "Expired"
            st.rerun()

    # Color-coded indicator
    if st.session_state.license_status == "Active":
        st.markdown('<div class="soft-card" style="background: #dcfce7; border-left: 4px solid #166534;"><strong>✓ Active License Path</strong><br>Track your renewal timeline and complete CEUs before your TULIP window opens.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="soft-card" style="background: #fee2e2; border-left: 4px solid #b91c1c;"><strong>⚠ Expired License Path</strong><br>Reactivate your license with an updated CEU plan and TULIP resubmission.</div>', unsafe_allow_html=True)

    render_monthly_ceu_reminder()

    st.markdown("---")

    # Show appropriate tabs based on license status
    if st.session_state.license_status == "Active":
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📋 Start Here: Your Renewal Timeline",
            "📚 Browse & Complete CEU Courses",
            "✅ Step-by-Step Renewal Guide",
            "📋 Renewal Checklist",
            "🔗 TULIP Info & Official Links",
            "❓ FAQs & Common Questions",
            "🌟 Professional Growth",
            "📊 Legacy Dashboard (Profiles)"
        ])

        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Your Renewal Timeline at a Glance")
            st.markdown("""
**Texas requires:**
- **24 hours** of in-service education every 24 months
- **Required courses:** 4 hrs infection control + 4 hrs geriatrics + 4 hrs dementia = 12 hours minimum
- **Flexible courses:** 12 additional hours on any approved topic

**Key Dates:**
- Your license expires on your expiration date
- **90 days before expiration = TULIP window opens**
- You can ONLY renew through TULIP once the window opens
- Renewal after expiration requires reinstatement procedures (more complex)
            """)
            
            st.markdown("### Quick Start Questions")
            q1 = st.checkbox("When does my TULIP renewal window open?")
            if q1:
                st.info("**TULIP opens exactly 90 days before your license expires.**\n\nExample: If your license expires June 15, TULIP opens March 17.")
            
            q2 = st.checkbox("How many hours do I need?")
            if q2:
                st.success("**24 hours total** over your 24-month license period.\n\n- 4 hours: Infection Control (required, annual)\n- 4 hours: Geriatric Care (required)\n- 4 hours: Dementia/Alzheimer's (required)\n- 12 hours: Any approved courses")
            
            q3 = st.checkbox("What if I wait until after my license expires?")
            if q3:
                st.warning("**After expiration, you cannot work as a CNA.**\n\nReactivation requires a Reinstatement application (more steps, potential delays). Renew **before** your license expires!")
            
            q4 = st.checkbox("Can I do these courses now, before TULIP opens?")
            if q4:
                st.success("**Yes!** Complete your 24 hours anytime. When TULIP opens, you'll upload your certificates for renewal.")
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Texas DHS Approved CEU Courses")
            st.markdown("Select courses and track your progress. All courses below meet Texas Department of Health Services requirements.")
            
            # Filter by category
            categories = sorted(set(course["category"] for course in CEU_COURSE_LIBRARY))
            selected_category = st.selectbox("Filter by category", ["All Categories"] + categories, key="ceu_category_filter")
            
            # Display courses
            if selected_category == "All Categories":
                display_courses = CEU_COURSE_LIBRARY
            else:
                display_courses = [c for c in CEU_COURSE_LIBRARY if c["category"] == selected_category]
            
            total_hours = sum(c["hours"] for c in display_courses)
            required_count = sum(1 for c in display_courses if c["required"])
            
            st.markdown(f"**Displaying {len(display_courses)} courses** • {total_hours} total hours • {required_count} required")
            
            st.markdown("---")
            
            for i, course in enumerate(display_courses):
                col1, col2, col3 = st.columns([0.08, 0.72, 0.20])
                
                with col1:
                    selected = st.checkbox("", value=course["id"] in st.session_state.selected_ceus, key=f"course_{course['id']}")
                    if selected:
                        if course["id"] not in st.session_state.selected_ceus:
                            st.session_state.selected_ceus.append(course["id"])
                    else:
                        if course["id"] in st.session_state.selected_ceus:
                            st.session_state.selected_ceus.remove(course["id"])
                
                with col2:
                    badge_color = "🔴 REQUIRED" if course["required"] else "🟢 OPTIONAL"
                    st.markdown(f"""
**{course['title']}**  
{badge_color} • {course['hours']} hours • {course['category']}  
*{course['description']}*  
📍 {course['provider']} • 💰 {course['cost']} • 📱 {course['format']}
                    """)
                
                with col3:
                    if st.button("Details ℹ", key=f"details_{course['id']}", use_container_width=True):
                        st.session_state[f"show_details_{course['id']}"] = not st.session_state.get(f"show_details_{course['id']}", False)
                
                if st.session_state.get(f"show_details_{course['id']}", False):
                    with st.expander("Course Details", expanded=True):
                        st.markdown("**Highlights:**")
                        for highlight in course["highlights"]:
                            st.write(f"- {highlight}")
                        st.divider()
                        st.markdown(f"**Provider:** {course['provider']}")
                        st.markdown(f"**Cost Range:** {course['cost']}")
                        st.markdown(f"**Format:** {course['format']}")
                
                st.divider()
            
            # Selection summary
            if st.session_state.selected_ceus:
                selected_courses = [c for c in CEU_COURSE_LIBRARY if c["id"] in st.session_state.selected_ceus]
                total_selected_hours = sum(c["hours"] for c in selected_courses)
                st.markdown(f"### Your Selection: {len(selected_courses)} courses • {total_selected_hours} hours")
                
                for course in selected_courses:
                    st.markdown(f"- **{course['title']}** — {course['hours']} hrs ({course['category']})")
                
                if total_selected_hours >= 24:
                    st.success(f"✓ You've selected {total_selected_hours} hours — meets the 24-hour requirement!")
                else:
                    st.warning(f"You've selected {total_selected_hours} hours. You need 24 hours total.")
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Step-by-Step: Active License Renewal Path")
            st.markdown("Follow these steps in order to successfully renew your Texas CNA license.")
            
            for step_info in ACTIVE_LICENSE_RENEWAL_STEPS:
                with st.expander(f"**Step {step_info['step']}: {step_info['title']}**", expanded=step_info['step'] == 1):
                    st.markdown(f"**Description:**\n{step_info['description']}")
                    st.markdown(f"**What to do:**\n{step_info['action']}")
                    st.markdown("**Checklist:**")
                    for item in step_info["checklist"]:
                        st.checkbox(item, key=f"active_step_{step_info['step']}_item_{item}")
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Interactive Renewal Checklist")
            st.markdown("Track your progress through the renewal process. Check off items as you complete them.")
            
            checklist_items = RENEWAL_READINESS_CHECKLIST["active_cna"]
            completed_count = 0
            
            for i, item_data in enumerate(checklist_items):
                completed = st.checkbox(item_data["item"], key=f"active_checklist_{i}")
                if completed:
                    completed_count += 1
                st.session_state.renewal_checklist_items[f"active_{i}"] = completed
            
            progress_pct = (completed_count / len(checklist_items)) * 100
            st.markdown(f"### Progress: {completed_count}/{len(checklist_items)} items complete")
            st.progress(progress_pct / 100)
            st.markdown(f"**{progress_pct:.0f}% Complete**")
            
            if completed_count == len(checklist_items):
                st.success("🎉 All items checked! You're ready to submit your renewal through TULIP.")
            
            # Print-friendly version
            if st.button("📄 Generate Printable Checklist"):
                checklist_text = "TEXAS CNA RENEWAL CHECKLIST - ACTIVE LICENSE\n" + "="*50 + "\n\n"
                for i, item_data in enumerate(checklist_items, 1):
                    status = "☑" if st.session_state.renewal_checklist_items.get(f"active_{i-1}", False) else "☐"
                    checklist_text += f"{status} {item_data['item']}\n"
                st.download_button(
                    "Download Checklist",
                    checklist_text,
                    "cna_renewal_checklist.txt",
                    "text/plain"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab5:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### TULIP: Texas Uniform License and Permit System")
            st.markdown(f"**Official Portal:** [TULIP.texas.gov](https://www.tulip.texas.gov)")
            
            st.markdown("### What You Need for TULIP Renewal")
            st.markdown("""
✓ **Personal Information:**
- Your Texas CNA Certificate Number
- Social Security Number (for identity verification)
- Current contact information (address, phone, email)

✓ **Proof of 24-Hour In-Service Education:**
- CEU certificates from all courses
- Provider information
- Dates completed

✓ **Required Topics Documentation:**
- Infection Control training certificate (4+ hours)
- Geriatric Care certificate (4+ hours)
- Dementia/Alzheimer's Care certificate (4+ hours)

✓ **Employer Verification (if requested):**
- Form 5506-NAR (May be required by your facility)
- Employer/facility contact information

✓ **Renewal Fee:**
- Current fee: $75-$100 (verify in TULIP)
- Payment method: Credit/debit card through TULIP portal
            """)
            
            st.divider()
            
            st.markdown("### Texas HHSC Support Resources")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Official Websites:**")
                st.markdown("[🔗 Texas HHSC CNA Registry](https://hhs.texas.gov/nurses-aids)")
                st.markdown("[🔗 TULIP System](https://www.tulip.texas.gov)")
                st.markdown("[🔗 TULIP Support Portal](https://www.tulip.texas.gov/support)")
            
            with col2:
                st.markdown("**Contact Information:**")
                st.markdown("📞 **Phone:** 512-438-1234")
                st.markdown("📧 **Email:** contactcna@dshs.texas.gov")
                st.markdown("💬 **Chat:** Available through TULIP portal")
            
            st.markdown("---")
            
            st.markdown("### TULIP Timeline for Your Renewal")
            
            renewal_timeline = f"""
1. **Now**: Complete your 24-hour CEU requirement
2. **90 Days Before Expiration**: TULIP renewal window opens (automatic email notification)
3. **TULIP Opens - First Day**: Log in immediately, verify your information
4. **Within 2 Weeks**: Upload all CEU certificates and documentation
5. **Within 3 Weeks**: Confirm required topics and submit application
6. **5-10 Business Days**: Processing (TULIP will update your status)
7. **Upon Approval**: Receive new license by mail + digital certificate in TULIP
8. **Before Expiration Date**: Download/print your new license for your records
            """
            st.info(renewal_timeline)
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab6:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Frequently Asked Questions")
            
            faq_items = [
                ("Can I renew my license early?", "No. TULIP only opens 90 days before your license expires. You cannot renew before that window."),
                ("What if I don't complete 24 hours before the TULIP window opens?", "You can still renew if you complete them by the TULIP deadline. TULIP will show you the status of your application as you add documents."),
                ("Can I renew after my license expires?", "Not through the standard renewal process. After expiration, you must file a Reinstatement application, which takes longer and has additional requirements."),
                ("What if TULIP is down on the deadline day?", "Contact Texas HHSC immediately. You may be granted a brief extension if there are system issues. Document the problem."),
                ("Do I need to be employed to renew?", "No. You can renew as long as your documentation is complete. Your employment status is separate from renewal."),
                ("If I'm employed at a facility, do they file the renewal?", "No. You file the renewal through TULIP. Your employer may provide Form 5506-NAR verification if required."),
                ("What if my CEU was from out of state?", "Texas generally requires courses from Texas-approved providers. Check with HHSC to verify if your course qualifies."),
                ("How long does processing take?", "Usually 5-10 business days. You'll receive email updates in TULIP."),
                ("Can I download my license before it's mailed?", "Yes! Your digital certificate is available in TULIP immediately upon approval."),
                ("What's the renewal fee?", "Current fee is $75-$100. The exact amount will display in TULIP when you submit."),
            ]
            
            for question, answer in faq_items:
                with st.expander(f"**Q: {question}**"):
                    st.markdown(f"{answer}")
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab7:
            render_professional_growth("Active License")

        with tab8:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Profile-Based Renewal Dashboard (Legacy View)")
            st.markdown("This view shows individual CNA profiles with renewal status if you prefer the traditional profile-based interface.")
            
            active_options = cna_df[cna_df["user_type"] != "Student"].copy()
            if not active_options.empty:
                active_options["display"] = active_options["first_name"] + " " + active_options["last_name"] + " • " + active_options["license_number"]
                selected_name = st.selectbox("Select CNA profile", active_options["display"].tolist(), key="active_profile_select")
                selected = active_options[active_options["display"] == selected_name].iloc[0]

                summary = compliance_snapshot(selected["cna_id"], selected["expiration_date"], ceu_df)
                score = readiness_score(summary)
                records = ceu_df[ceu_df["cna_id"] == selected["cna_id"]]

                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.markdown(f'<div class="metric-card"><div class="kpi">{score}%</div><div class="label">Renewal Readiness</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-card"><div class="kpi">{summary["hours"]}/24</div><div class="label">In-Service Hours</div></div>', unsafe_allow_html=True)
                with m3:
                    status = "OPEN" if summary["tulip_days"] <= 0 else "NOT OPEN"
                    st.markdown(f'<div class="metric-card"><div class="kpi">{status}</div><div class="label">TULIP Window</div></div>', unsafe_allow_html=True)
                with m4:
                    st.markdown(f'<div class="metric-card"><div class="kpi">{summary["days_left"]}</div><div class="label">Days Until Expiration</div></div>', unsafe_allow_html=True)

                st.markdown("---")
                
                st.markdown("### Personal Compliance Details")
                st.write(f"**CNA:** {selected['first_name']} {selected['last_name']}")
                st.write(f"**License Number:** {selected['license_number']}")
                st.write(f"**Expiration Date:** {selected['expiration_date']}")
                st.progress(score / 100)

                x1, x2, x3 = st.columns(3)
                with x1:
                    st.success("✓ Geriatrics recorded") if summary["geriatric"] else st.error("✗ Geriatrics not recorded")
                with x2:
                    st.success("✓ Dementia recorded") if summary["dementia"] else st.error("✗ Dementia not recorded")
                with x3:
                    st.success("✓ Infection control recorded") if summary["infection"] else st.error("✗ Infection control not recorded")

                st.markdown("---")

                st.markdown("### CEU Records on File")
                if records.empty:
                    st.info("No CEU records found for this profile.")
                else:
                    display = records.rename(columns={
                        "course_title": "Course Title",
                        "hours": "Hours",
                        "geriatric_flag": "Geriatric",
                        "dementia_flag": "Dementia",
                        "infection_flag": "Infection Control"
                    })[["Course Title", "Hours", "Geriatric", "Dementia", "Infection Control"]]
                    st.dataframe(display, use_container_width=True, hide_index=True)
            else:
                st.info("No active CNA profiles available.")
            
            st.markdown('</div>', unsafe_allow_html=True)

    else:  # EXPIRED LICENSE PATH
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📋 Start Here: Reactivation Timeline",
            "📚 Browse & Complete CEU Courses",
            "✅ Step-by-Step Reactivation Guide",
            "📋 Reactivation Checklist",
            "🔗 TULIP Info & Official Links",
            "❓ FAQs & Common Questions",
            "🌟 Professional Growth",
            "📊 Legacy Dashboard (Profiles)"
        ])

        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Reactivating Your Expired Texas CNA License")
            st.markdown("Don't worry! You can reactivate your license, but it requires updated CEU documentation and resubmission through TULIP.")
            
            st.markdown("""
**Important Notes:**
- You **cannot work as a CNA** until your license is reactivated
- Your employer needs to know your current status
- Reactivation is similar to renewal but requires additional verification
- The reactivation process may take longer than standard renewal
            """)
            
            st.info("""
**Quick Decision:**
- **If expired < 2 years:** Use standard renewal pathway (slightly easier)
- **If expired > 2 years:** May require reinstatement pathway (more steps)

**First step:** Contact Texas HHSC to confirm which pathway you need.
            """)
            
            st.markdown("### Key Requirements for Reactivation")
            st.markdown("""
✓ **Current CEU Documentation (24 hours)**
- 4 hours: Infection Prevention & Control (current/annual)
- 4 hours: Geriatric Care
- 4 hours: Dementia/Alzheimer's Care
- 12 hours: Additional approved courses

✓ **Proof of Current Training**
- Original CEU certificates with dates
- Provider information
- Course verification

✓ **Employer Verification (if employed)**
- Proof that you work (or want to work) as a CNA
- Form 5506-NAR if required

✓ **Updated Personal Information**
- Current address
- Current phone/email
- Confirmation you're ready to work as CNA
            """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("### 📞 Step 1")
                st.markdown("**Contact Texas HHSC**\n\nCall or email to confirm your reactivation pathway")
            with col2:
                st.markdown("### 📚 Step 2")
                st.markdown("**Complete CEU Courses**\n\nFinish your 24 hours of required training")
            with col3:
                st.markdown("### 📤 Step 3")
                st.markdown("**Submit Through TULIP**\n\nReactivate online with your new documentation")
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Texas DHS Approved CEU Courses for Reactivation")
            st.markdown("You must complete current training (within the last 2 years ideally) to reactivate your license.")
            
            # Filter by category
            categories = sorted(set(course["category"] for course in CEU_COURSE_LIBRARY))
            selected_category = st.selectbox("Filter by category", ["All Categories"] + categories, key="expired_ceu_category_filter")
            
            # Display courses
            if selected_category == "All Categories":
                display_courses = CEU_COURSE_LIBRARY
            else:
                display_courses = [c for c in CEU_COURSE_LIBRARY if c["category"] == selected_category]
            
            total_hours = sum(c["hours"] for c in display_courses)
            required_count = sum(1 for c in display_courses if c["required"])
            
            st.markdown(f"**Displaying {len(display_courses)} courses** • {total_hours} total hours • {required_count} required")
            
            st.markdown("---")
            
            for i, course in enumerate(display_courses):
                col1, col2, col3 = st.columns([0.08, 0.72, 0.20])
                
                with col1:
                    selected = st.checkbox("", value=course["id"] in st.session_state.selected_ceus, key=f"expired_course_{course['id']}")
                    if selected:
                        if course["id"] not in st.session_state.selected_ceus:
                            st.session_state.selected_ceus.append(course["id"])
                    else:
                        if course["id"] in st.session_state.selected_ceus:
                            st.session_state.selected_ceus.remove(course["id"])
                
                with col2:
                    badge_color = "🔴 REQUIRED" if course["required"] else "🟢 OPTIONAL"
                    st.markdown(f"""
**{course['title']}**  
{badge_color} • {course['hours']} hours • {course['category']}  
*{course['description']}*  
📍 {course['provider']} • 💰 {course['cost']} • 📱 {course['format']}
                    """)
                
                with col3:
                    if st.button("Details ℹ", key=f"expired_details_{course['id']}", use_container_width=True):
                        st.session_state[f"expired_show_details_{course['id']}"] = not st.session_state.get(f"expired_show_details_{course['id']}", False)
                
                if st.session_state.get(f"expired_show_details_{course['id']}", False):
                    with st.expander("Course Details", expanded=True):
                        st.markdown("**Highlights:**")
                        for highlight in course["highlights"]:
                            st.write(f"- {highlight}")
                        st.divider()
                        st.markdown(f"**Provider:** {course['provider']}")
                        st.markdown(f"**Cost Range:** {course['cost']}")
                        st.markdown(f"**Format:** {course['format']}")
                
                st.divider()
            
            # Selection summary
            if st.session_state.selected_ceus:
                selected_courses = [c for c in CEU_COURSE_LIBRARY if c["id"] in st.session_state.selected_ceus]
                total_selected_hours = sum(c["hours"] for c in selected_courses)
                st.markdown(f"### Your Selection: {len(selected_courses)} courses • {total_selected_hours} hours")
                
                for course in selected_courses:
                    st.markdown(f"- **{course['title']}** — {course['hours']} hrs ({course['category']})")
                
                if total_selected_hours >= 24:
                    st.success(f"✓ You've selected {total_selected_hours} hours — meets the 24-hour requirement!")
                else:
                    st.warning(f"You've selected {total_selected_hours} hours. You need 24 hours total.")
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Step-by-Step: Expired License Reactivation Path")
            st.markdown("Follow these steps to reactivate your Texas CNA license.")
            
            for step_info in EXPIRED_LICENSE_REACTIVATION_STEPS:
                with st.expander(f"**Step {step_info['step']}: {step_info['title']}**", expanded=step_info['step'] == 1):
                    st.markdown(f"**Description:**\n{step_info['description']}")
                    st.markdown(f"**What to do:**\n{step_info['action']}")
                    st.markdown("**Checklist:**")
                    for item in step_info["checklist"]:
                        st.checkbox(item, key=f"expired_step_{step_info['step']}_item_{item}")
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Interactive Reactivation Checklist")
            st.markdown("Track your progress through the reactivation process. Check off items as you complete them.")
            
            checklist_items = RENEWAL_READINESS_CHECKLIST["expired_cna"]
            completed_count = 0
            
            for i, item_data in enumerate(checklist_items):
                completed = st.checkbox(item_data["item"], key=f"expired_checklist_{i}")
                if completed:
                    completed_count += 1
                st.session_state.renewal_checklist_items[f"expired_{i}"] = completed
            
            progress_pct = (completed_count / len(checklist_items)) * 100
            st.markdown(f"### Progress: {completed_count}/{len(checklist_items)} items complete")
            st.progress(progress_pct / 100)
            st.markdown(f"**{progress_pct:.0f}% Complete**")
            
            if completed_count == len(checklist_items):
                st.success("🎉 All items checked! You're ready to submit your reactivation through TULIP.")
            
            # Print-friendly version
            if st.button("📄 Generate Printable Checklist", key="expired_print_checklist"):
                checklist_text = "TEXAS CNA REACTIVATION CHECKLIST - EXPIRED LICENSE\n" + "="*50 + "\n\n"
                for i, item_data in enumerate(checklist_items, 1):
                    status = "☑" if st.session_state.renewal_checklist_items.get(f"expired_{i-1}", False) else "☐"
                    checklist_text += f"{status} {item_data['item']}\n"
                st.download_button(
                    "Download Checklist",
                    checklist_text,
                    "cna_reactivation_checklist.txt",
                    "text/plain",
                    key="expired_download_checklist"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab5:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### TULIP: Texas Uniform License and Permit System")
            st.markdown(f"**Official Portal:** [TULIP.texas.gov](https://www.tulip.texas.gov)")
            
            st.markdown("### Reactivation Through TULIP")
            st.markdown("""
**When you log into TULIP, select:**
- **If expired < 2 years:** "Renew License"
- **If expired > 2 years:** "Reinstatement Application"

**You will need:**
- Your old Certificate Number or Social Security Number
- Current CEU documentation (24 hours)
- Updated contact information
- Proof of employment or intent to work as CNA
            """)
            
            st.divider()
            
            st.markdown("### Texas HHSC Support Resources for Reactivation")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Official Websites:**")
                st.markdown("[🔗 Texas HHSC CNA Registry](https://hhs.texas.gov/nurses-aids)")
                st.markdown("[🔗 TULIP System](https://www.tulip.texas.gov)")
                st.markdown("[🔗 TULIP Support Portal](https://www.tulip.texas.gov/support)")
            
            with col2:
                st.markdown("**Contact Information:**")
                st.markdown("📞 **Phone:** 512-438-1234")
                st.markdown("📧 **Email:** contactcna@dshs.texas.gov")
                st.markdown("💬 **Chat:** Available through TULIP portal")
            
            st.markdown("---")
            
            st.markdown("### Why Contacting HHSC First Matters")
            st.info("""
**Before submitting in TULIP, call Texas HHSC to:**
1. Confirm your reactivation pathway (renewal vs. reinstatement)
2. Ask if there are any special requirements for your situation
3. Verify your old certificate number or provide SSN
4. Get estimated processing timeline
5. Ask about any late fees or additional documentation

This 10-minute call can save you from delays!
            """)
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab6:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Frequently Asked Questions About Reactivation")
            
            faq_items = [
                ("How long has my license been expired?", "Check your license expiration date to know how long it's been. If < 2 years, the process is easier."),
                ("Will I lose my seniority or experience?", "Your prior work history remains on record. Reactivation restores your active status."),
                ("Do I need to find a job before reactivating?", "No. You can reactivate without a job lined up. However, employers may ask to verify your active status."),
                ("Will I need to retake the CNA exam?", "No. Reactivation only requires updated CEU documentation, not re-testing."),
                ("Can I work while my reactivation is pending?", "No. You cannot work as a CNA until your license is officially reactivated in TULIP."),
                ("Will reactivation cost more than renewal?", "The fee is typically the same ($75-$100), though reinstatement may have additional fees. TULIP will show the exact amount."),
                ("How long does reactivation take?", "Usually 5-10 business days if all documentation is complete. Reinstatement may take longer (2-3 weeks)."),
                ("What if I can't find my old certificate number?", "You can use your Social Security Number instead. TULIP will look up your record."),
                ("Can my employer help with the reactivation?", "Your employer can provide Form 5506-NAR verification, but you must submit the reactivation yourself through TULIP."),
                ("What if my information has changed (name, address)?", "Update your information in TULIP. You may need to provide verification for legal name changes."),
            ]
            
            for question, answer in faq_items:
                with st.expander(f"**Q: {question}**"):
                    st.markdown(f"{answer}")
            
            st.markdown('</div>', unsafe_allow_html=True)

        with tab7:
            render_professional_growth("Expired License")

        with tab8:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Profile-Based Dashboard (Legacy View)")
            st.markdown("If you were previously employed and want to view your old profile information:")
            
            active_options = cna_df[cna_df["user_type"] != "Student"].copy()
            if not active_options.empty:
                active_options["display"] = active_options["first_name"] + " " + active_options["last_name"] + " • " + active_options["license_number"]
                selected_name = st.selectbox("Select CNA profile", active_options["display"].tolist(), key="expired_profile_select")
                selected = active_options[active_options["display"] == selected_name].iloc[0]

                summary = compliance_snapshot(selected["cna_id"], selected["expiration_date"], ceu_df)
                score = readiness_score(summary)

                st.warning(f"**License Status:** EXPIRED (expired {abs(summary['days_left'])} days ago)")
                st.markdown(f"**CNA:** {selected['first_name']} {selected['last_name']}")
                st.markdown(f"**License Number:** {selected['license_number']}")
                st.markdown(f"**Expiration Date:** {selected['expiration_date']}")
                
                st.info("This profile shows historical information. To reactivate, use the Step-by-Step guide in the Reactivation Guide tab above.")
            else:
                st.info("No profiles available.")
            
            st.markdown('</div>', unsafe_allow_html=True)
# =========================================================
# VIEW C
# =========================================================
else:
    st.subheader("DON or Instructors & Facility Dashboard")
    st.markdown(
        '<div class="info-card">Monitor facility readiness, highlight urgent CNA action items, and support TULIP compliance with clear staff-level guidance.</div>',
        unsafe_allow_html=True
    )
    render_view_visuals("c")
    facility = facility_df.iloc[0]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"**Facility:** {facility['facility_name']}")
    st.write(f"**State License Number:** {facility['state_license_number']}")
    st.write(f"**Director of Nursing:** {facility['don_name']}")
    st.markdown('</div>', unsafe_allow_html=True)

    active_staff = cna_df[cna_df["user_type"] != "Student"].copy()
    rows = []
    for _, row in active_staff.iterrows():
        summary = compliance_snapshot(row["cna_id"], row["expiration_date"], ceu_df)
        rows.append({
            "CNA ID": row["cna_id"],
            "First Name": row["first_name"],
            "Last Name": row["last_name"],
            "License Number": row["license_number"],
            "Days Until Expiration": summary["days_left"],
            "CEU Hours Completed": summary["hours"],
            "Geriatrics": "Yes" if summary["geriatric"] else "No",
            "Dementia": "Yes" if summary["dementia"] else "No",
            "Infection Control": "Yes" if summary["infection"] else "No",
            "Readiness Score": readiness_score(summary),
            "Status": status_from_expiration(row["expiration_date"])
        })

    matrix = pd.DataFrame(rows)

    green_count = len(matrix[matrix["Status"] == "GREEN"])
    red_count = len(matrix[matrix["Status"] == "RED"])
    incomplete_ceu = len(matrix[matrix["CEU Hours Completed"] < 24])

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f'<div class="metric-card"><div class="kpi">{green_count}</div><div class="label">Safe Zone Staff</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="metric-card"><div class="kpi">{red_count}</div><div class="label">Inside 90-Day Window</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="metric-card"><div class="kpi">{incomplete_ceu}</div><div class="label">Below 24 Hours</div></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Staff Matrix",
        "Action Center",
        "DON Risk Notes",
        "Career Board"
    ])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### TULIP Readiness Staff Matrix")
        urgency = st.segmented_control("Filter by urgency", ["ALL", "GREEN", "RED"], default="ALL")
        filtered = matrix if urgency == "ALL" else matrix[matrix["Status"] == urgency]

        def highlight(row):
            color = "#dcfce7" if row["Status"] == "GREEN" else "#fee2e2"
            return [f"background-color: {color}"] * len(row)

        st.dataframe(filtered.style.apply(highlight, axis=1), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Action Center")
        red_staff = matrix[matrix["Status"] == "RED"]

        if red_staff.empty:
            st.success("No CNAs are currently inside the 90-day TULIP window.")
        else:
            options = red_staff.apply(
                lambda x: f"{x['First Name']} {x['Last Name']} • {x['License Number']} • {x['Days Until Expiration']} days left",
                axis=1
            ).tolist()
            selected_option = st.selectbox("Select CNA needing action", options)
            chosen = red_staff.iloc[options.index(selected_option)]
            chosen_cna = cna_df[cna_df["cna_id"] == chosen["CNA ID"]].iloc[0]
            chosen_summary = compliance_snapshot(chosen_cna["cna_id"], chosen_cna["expiration_date"], ceu_df)

            a1, a2 = st.columns(2)
            with a1:
                if st.button("Pre-fill Form 5506-NAR", use_container_width=True):
                    text = make_5506_text(chosen_cna, facility, chosen_summary)
                    st.success("Mock 5506-NAR summary generated.")
                    st.download_button(
                        "Download 5506-NAR Mock Summary",
                        data=text,
                        file_name=f"5506-NAR-{chosen_cna['last_name']}-{chosen_cna['first_name']}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    st.text_area("Preview", text, height=340)

            with a2:
                if st.button("Mock Twilio SMS Trigger", use_container_width=True):
                    sms = f"Hi {chosen_cna['first_name']}, your 3-month Texas TULIP window is OPEN. Your Form 5506-NAR is pre-filled and waiting on the DON desk."
                    st.info("Mock SMS fired.")
                    st.markdown(f'<div class="sms-box">{sms}</div>', unsafe_allow_html=True)

            n1, n2, n3 = st.columns(3)
            with n1:
                st.markdown(f'<span class="badge badge-red">Days Left: {chosen_summary["days_left"]}</span>', unsafe_allow_html=True)
            with n2:
                st.markdown(f'<span class="badge badge-amber">Readiness: {readiness_score(chosen_summary)}%</span>', unsafe_allow_html=True)
            with n3:
                flags = [
                    "Geriatrics ✔" if chosen_summary["geriatric"] else "Geriatrics ✘",
                    "Dementia ✔" if chosen_summary["dementia"] else "Dementia ✘",
                    "Infection ✔" if chosen_summary["infection"] else "Infection ✘"
                ]
                st.markdown(f'<span class="badge badge-red">{" | ".join(flags)}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### DON Risk Notes")
        st.write("- Monitor all CNAs inside the 90-day TULIP window.")
        st.write("- Audit 24-hour totals and required topic coverage early.")
        st.write("- Confirm annual infection-control training records.")
        st.write("- Prepare Form 5506-NAR support before staff become urgent cases.")
        st.write("- Use readiness score trends to prioritize outreach.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown("### Facility Career Board")
        st.write("This placeholder supports a free-community model through targeted facility job and training postings.")
        st.write("- Weekend CNA openings")
        st.write("- Evening and night shift differential opportunities")
        st.write("- Employer-sponsored CEU support")
        st.write("- Test-prep assistance and referral bonuses")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption(
    "Educational workflow application for Texas CNA study, renewal support, and DON compliance planning. Confirm current rules, forms, credential status, and submission requirements with official Texas HHSC, TULIP, and Prometric resources."
)
st.markdown(
    '<div class="footer-note">Version 1.0 • For educational planning only. Always verify with Texas HHSC and facility guidance.</div>',
    unsafe_allow_html=True
)
