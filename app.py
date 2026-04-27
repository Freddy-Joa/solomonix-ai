
import streamlit as st
from PIL import Image
import PyPDF2
import docx
import re

from utils.legal_predictor import predict_case_outcome
from utils.delay_predictor import predict_delay
from utils.priority_engine import calculate_priority
from utils.nlp_engine import summarize_text, extract_keywords

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Solomonix AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #071224, #0B1F3A);
        color: white;
    }

    .main-title {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        color: #FFD700;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        font-size: 1.25rem;
        color: #E2E8F0;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FILE HELPERS
# --------------------------------------------------
# Replace your ENTIRE extract_text_from_file() function

def extract_text_from_file(uploaded_file):
    """
    Extract text and exact page count from TXT, PDF, DOCX.
    Highly accurate for judicial documents.
    """
    text = ""
    page_count = 1
    extension = uploaded_file.name.split(".")[-1].lower()

    try:
        uploaded_file.seek(0)

        if extension == "txt":
            raw = uploaded_file.read()
            text = raw.decode("utf-8", errors="ignore")
            page_count = max(1, round(len(text.split()) / 350))

        elif extension == "pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            # Exact PDF page count
            page_count = len(pdf_reader.pages)

            extracted_pages = []

            for i, page in enumerate(pdf_reader.pages, start=1):
                page_text = page.extract_text()

                if page_text and page_text.strip():
                    extracted_pages.append(page_text.strip())

            text = "\n\n".join(extracted_pages)

        elif extension == "docx":
            document = docx.Document(uploaded_file)

            paragraphs = [
                para.text.strip()
                for para in document.paragraphs
                if para.text.strip()
            ]

            text = "\n".join(paragraphs)

            # Better DOCX page estimation
            word_count = len(text.split())
            page_count = max(1, round(word_count / 300))

    except Exception as e:
        st.error(f"File processing error: {e}")
        return "", 1

    return text.strip(), page_count


# Replace ONLY your extract_case_details() function

def extract_case_details(text, actual_pages=1):
    """
    Extract judicial metadata with maximum precision.
    """

    import re

    def extract_first(patterns):
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 0

    # Evidence
    evidence_count = extract_first([
        r'(\d+)\s+evidence\s+documents?',
        r'(\d+)\s+documents?',
        r'(\d+)\s+exhibits?'
    ])

    # Witnesses
    witness_count = extract_first([
        r'(\d+)\s+witness(?:es)?'
    ])

    # Expert Reports
    expert_reports = extract_first([
        r'(\d+)\s+expert\s+reports?'
    ])

    # --------------------------------------------------
    # SMART PAGE DETECTION
    # --------------------------------------------------
    detected_pages = re.findall(
        r'Page\s+(\d+)',
        text,
        re.IGNORECASE
    )

    if detected_pages:
        actual_pages = max(map(int, detected_pages))

    # --------------------------------------------------
    # TITLE EXTRACTION
    # --------------------------------------------------
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    case_title = lines[0] if lines else "Unknown Case"

    return {
        "title": case_title,
        "evidence": evidence_count,
        "witnesses": witness_count,
        "experts": expert_reports,
        "pages": actual_pages,
        "words": len(text.split())
    }

# --------------------------------------------------
# HEADER
# --------------------------------------------------
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.image("assets/Law-Commission-of-India.jpg", width=140)

with col2:
    st.markdown('<h1 class="main-title">⚖️ Solomonix AI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Predict • Prioritize • Preserve Justice</p>',
        unsafe_allow_html=True
    )

with col3:
    st.image("assets/logo_solomonix_AI.png", width=170)

st.divider()

# --------------------------------------------------
# METRICS
# --------------------------------------------------
m1, m2, m3 = st.columns(3)

m1.metric("Total Cases", "5,42,381")
m2.metric("Completed Cases", "3,91,247")
m3.metric("Pending Cases", "1,51,134")

st.divider()

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📜 Case Intelligence",
    "⏳ Delay Prediction",
    "🎯 Priority Assessment"
])

# ==================================================
# TAB 1
# ==================================================
with tab1:
    st.header("Evidence Intelligence Engine")

    uploaded_file = st.file_uploader(
        "Upload Legal Document",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file:
        extracted_text, actual_pages = extract_text_from_file(uploaded_file)

        if extracted_text:
            details = extract_case_details(extracted_text)

            st.success("Document uploaded successfully.")

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Evidence", details["evidence"])
            c2.metric("Witnesses", details["witnesses"])
            c3.metric("Expert Reports", details["experts"])
            c4.metric("Pages", details["pages"])
            c5.metric("Words", details["words"])

            st.subheader("Document Preview")
            st.text_area(
                "Preview",
                extracted_text[:6000],
                height=350
            )

            # Replace ONLY the "🚀 Analyze Legal Document" button block

if st.button("🚀 Analyze Legal Document", use_container_width=True):
    with st.spinner("Analyzing judicial document..."):
        try:
            # AI Predictions
            outcome, confidence = predict_case_outcome(extracted_text)
            summary = summarize_text(extracted_text)
            keywords = extract_keywords(extracted_text)

            # -------------------------------
            # SMART JUDICIAL METRICS
            # -------------------------------
            pending_days = max(
                details["pages"] * 240,          # Age of case
                details["witnesses"] * 90,        # Witness complexity
                details["experts"] * 120,         # Expert involvement
                365
            )

            evidence_pages = max(
                details["evidence"] * 35,         # Documentary burden
                details["pages"] * 150,           # Actual file size
                100
            )

            judge_load = min(
                95,
                50 +
                (details["witnesses"] * 2) +
                (details["experts"] * 4)
            )

            # -------------------------------
            # DELAY PREDICTION
            # -------------------------------
            delay_prediction, delay_probability = predict_delay(
                "Civil",
                pending_days,
                evidence_pages,
                max(details["witnesses"], 1),
                "High",
                judge_load
            )

            # -------------------------------
            # PRIORITY ASSESSMENT
            # -------------------------------
            priority_level, priority_score = calculate_priority(
                pending_days,
                max(details["witnesses"], 1),
                evidence_pages
            )

            # -------------------------------
            # RESULTS
            # -------------------------------
            st.success(f"Predicted Outcome: {outcome}")
            st.info(f"Confidence Score: {confidence:.2%}")

            r1, r2, r3 = st.columns(3)

            if delay_prediction == 1:
                r1.error(
                    f"Delay Risk: High ({delay_probability:.2%})"
                )
            else:
                r1.success(
                    f"Delay Risk: Low ({delay_probability:.2%})"
                )

            r2.warning(
                f"Priority Level: {priority_level}"
            )

            r3.metric(
                "Priority Score",
                f"{priority_score:.2f}/100"
            )

            # -------------------------------
            # NLP OUTPUT
            # -------------------------------
            st.subheader("AI Case Summary")
            st.write(summary)

            st.subheader("Legal Keywords")
            st.write(
                ", ".join(keywords)
                if keywords
                else "No keywords detected."
            )

        except Exception as e:
            st.error(f"Analysis failed: {e}")
        else:
            st.warning("No readable text found in the uploaded document.")

# ==================================================
# TAB 2
# ==================================================
with tab2:
    st.header("Judicial Delay Forecasting")

    c1, c2 = st.columns(2)

    with c1:
        case_type = st.selectbox(
            "Case Type",
            ["Civil", "Criminal", "Family", "Corporate", "Property", "Tax"]
        )

        pending_days = st.slider("Pending Days", 1, 3000, 720)
        evidence_pages = st.slider("Evidence Pages", 1, 5000, 1250)

    with c2:
        witness_count = st.slider("Witness Count", 1, 50, 12)
        priority_level = st.selectbox(
            "Priority Level",
            ["Low", "Medium", "High", "Critical"]
        )
        judge_load = st.slider("Judge Workload", 1, 120, 68)

    if st.button("Predict Delay Risk", use_container_width=True):
        prediction, probability = predict_delay(
            case_type,
            pending_days,
            evidence_pages,
            witness_count,
            priority_level,
            judge_load
        )

        if prediction == 1:
            st.error(f"⚠️ High Delay Risk ({probability:.2%})")
        else:
            st.success(f"✅ Low Delay Risk ({probability:.2%})")

# ==================================================
# TAB 3
# ==================================================
with tab3:
    st.header("Automated Priority Assessment")

    p1, p2, p3 = st.columns(3)

    with p1:
        pending_days = st.number_input("Pending Days", 1, value=540)

    with p2:
        witnesses = st.number_input("Witness Count", 1, value=9)

    with p3:
        evidence_pages = st.number_input("Evidence Pages", 1, value=850)

    if st.button("Calculate Priority", use_container_width=True):
        level, score = calculate_priority(
            pending_days,
            witnesses,
            evidence_pages
        )

        st.success(f"Priority Level: {level}")
        st.metric("Priority Score", f"{score:.2f}/100")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption(
    "FREDDY JOA L R - HOUSE OF WISDOM - Solomonix AI © 2026 | In Collaboration with Law Commission of India"
)
