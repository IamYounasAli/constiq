import streamlit as st
from boq import compare_boq_pdfs
from vision import analyze_drawing_comparison
from ai import parse_pdf_boq_changes
from calculations import compute_boq_variances
from impact import analyze_ripple_impact
from report import render_dashboard

st.set_page_config(page_title="CONSTRIQ | Dual BOQ PDF Change Analyzer", page_icon="🏗️", layout="wide")

st.title("🏗️ CONSTRIQ")
st.caption("Smart Dual-BOQ PDF & Drawing Change Analyzer (Powered by Groq)")

# 1. Sidebar Uploaders
st.sidebar.header("📁 Document Uploads")
old_boq_file = st.sidebar.file_uploader(
    "1. Upload Old BOQ (CSV, XLSX, or PDF)", 
    type=["csv", "xlsx", "pdf"]
)
new_boq_file = st.sidebar.file_uploader(
    "2. Upload New BOQ with Changes (CSV, XLSX, or PDF)", 
    type=["csv", "xlsx", "pdf"]
)

st.sidebar.header("🖼️ Drawing Uploads (Optional)")
old_drawing = st.sidebar.file_uploader("Upload Old Drawing", type=["png", "jpg", "jpeg"], key="old_draw")
new_drawing = st.sidebar.file_uploader("Upload Revised Drawing", type=["png", "jpg", "jpeg"], key="new_draw")

# 2. Scope Notes Input
st.subheader("✍️ Optional Scope Notes")
user_notes = st.text_area(
    "Additional field context or revision notes (Optional):",
    placeholder="e.g., Client approved expansion of Room 101. Verify structural beam placements.",
    height=80
)

# 3. Execution Pipeline
if st.button("🚀 ANALYZE DIFFERENCES & RIPPLE IMPACT", type="primary", use_container_width=True):
    if not old_boq_file or not new_boq_file:
        st.error("Please upload both the Old BOQ and New BOQ files to run the delta analysis.")
    else:
        with st.spinner("Parsing files, running visual inspection, and calculating variances..."):
            try:
                # Step 1: Drawing Analysis (Handles single or dual drawing comparison)
                drawing_notes = None
                if old_drawing or new_drawing:
                    st.toast("Inspecting drawing diagrams...", icon="🖼️")
                    drawing_notes = analyze_drawing_comparison(old_drawing, new_drawing)
                
                # Step 2: Content Extraction
                st.toast("Extracting content from Old & New BOQ files...", icon="📄")
                boq_data = compare_boq_pdfs(old_boq_file, new_boq_file)
                
                # Step 3: AI Change Detection
                st.toast("Comparing BOQs via Groq LLM...", icon="🤖")
                combined_context = f"{user_notes}\n{drawing_notes if drawing_notes else ''}"
                parsed_changes = parse_pdf_boq_changes(
                    boq_data["old_text"], 
                    boq_data["new_text"], 
                    combined_context
                )
                
                # Step 4: Deterministic Mathematical Computations
                st.toast("Computing precise financial & quantity variances...", icon="🔢")
                calc_results = compute_boq_variances(parsed_changes, boq_data["old_df"])
                
                # Step 5: Risk Assessment & Confidence Synthesis
                st.toast("Synthesizing downstream schedule & trade risks...", icon="⚠️")
                risk_summary = analyze_ripple_impact(
                    calc_results, 
                    parsed_changes.get("change_summary", "Dual BOQ Comparison"),
                    confidence_data=parsed_changes
                )
                
                # Step 6: Render Interactive Dashboard
                render_dashboard(calc_results, risk_summary, drawing_notes)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
