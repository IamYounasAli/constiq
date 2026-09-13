import streamlit as st
from boq import compare_boq_pdfs
from vision import analyze_drawing
from ai import parse_pdf_boq_changes
from calculations import compute_boq_variances
from impact import analyze_ripple_impact
from report import render_dashboard

st.set_page_config(page_title="CONSTRIQ | Dual BOQ PDF Change Analyzer", page_icon="🏗️", layout="wide")

st.title("🏗️ CONSTRIQ")
st.caption("Smart Dual-BOQ PDF & Drawing Change Analyzer (Powered by Groq)")

st.sidebar.header("📁 Document Uploads")
old_boq_file = st.sidebar.file_uploader("1. Upload Old BOQ (PDF)", type=["pdf"])
new_boq_file = st.sidebar.file_uploader("2. Upload New BOQ with Changes (PDF)", type=["pdf"])
drawing_file = st.sidebar.file_uploader("3. Upload Drawing/Diagram (Optional)", type=["png", "jpg", "jpeg"])

st.subheader("✍️ Optional Scope Notes")
user_notes = st.text_area(
    "Additional field context or revision notes (Optional):",
    placeholder="e.g., Client approved expansion of Room 101. Verify structural beam placements.",
    height=80
)

if st.button("🚀 ANALYZE DIFFERENCES & RIPPLE IMPACT", type="primary", use_container_width=True):
    if not old_boq_file or not new_boq_file:
        st.error("Please upload both the Old BOQ PDF and New BOQ PDF to run the delta analysis.")
    else:
        with st.spinner("Parsing PDFs, running visual inspection, and calculating variances..."):
            try:
                # Step 1: Drawing Analysis if provided
                drawing_notes = None
                if drawing_file:
                    st.toast("Inspecting drawing diagram...", icon="🖼️")
                    drawing_notes = analyze_drawing(drawing_file)
                
                # Step 2: PDF Content Extraction
                st.toast("Extracting content from Old & New BOQ PDFs...", icon="📄")
                boq_data = compare_boq_pdfs(old_boq_file, new_boq_file)
                
                # Step 3: AI Change Detection
                st.toast("Comparing BOQs via Groq LLM...", icon="🤖")
                combined_context = f"{user_notes}\n{drawing_notes if drawing_notes else ''}"
                parsed_changes = parse_pdf_boq_changes(
                    boq_data["old_text"], 
                    boq_data["new_text"], 
                    combined_context
                )
                
                # Step 4: Python Mathematical Computations
                st.toast("Computing precise financial & quantity variances...", icon="🔢")
                calc_results = compute_boq_variances(parsed_changes, boq_data["old_df"])
                
                # Step 5: Risk & Ripple Impact Assessment
                st.toast("Synthesizing downstream schedule & trade risks...", icon="⚠️")
                risk_summary = analyze_ripple_impact(
                    calc_results, 
                    parsed_changes.get("change_summary", "Dual BOQ Comparison")
                )
                
                # Step 6: Render Interactive Dashboard
                render_dashboard(calc_results, risk_summary, drawing_notes)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
