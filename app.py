import streamlit as st
import pandas as pd
from boq import load_boq_data, get_boq_summary_list
from vision import analyze_drawing
from ai import parse_change_to_parameters
from calculations import compute_boq_variances
from impact import analyze_ripple_impact
from report import render_dashboard

st.set_page_config(page_title="CONSTRIQ | Change Impact Analyzer", page_icon="🏗️", layout="wide")

st.title("🏗️ CONSTRIQ")
st.caption("Smart Construction Change Impact & Ripple Effect Analyzer (Powered by Groq)")

st.sidebar.header("📁 Project Data Upload")
boq_file = st.sidebar.file_uploader("Upload Project BOQ (CSV/Excel)", type=["csv", "xlsx"])
drawing_file = st.sidebar.file_uploader("Upload Drawing/Diagram (Optional)", type=["png", "jpg", "jpeg"])

# Sample BOQ option
use_sample = st.sidebar.checkbox("Use Sample BOQ Data")

boq_df = None
if boq_file:
    try:
        boq_df = load_boq_data(boq_file)
        st.sidebar.success(f"✅ BOQ Loaded ({len(boq_df)} items)")
    except Exception as e:
        st.sidebar.error(f"Error loading BOQ: {e}")
elif use_sample:
    try:
        boq_df = load_boq_data("data/sample_boq.csv")
        st.sidebar.success(f"✅ Sample BOQ Loaded ({len(boq_df)} items)")
    except Exception as e:
        st.sidebar.error("Sample BOQ file not found in data/ folder.")

st.subheader("✍️ Enter Proposed Construction Change")
change_description = st.text_area(
    "Describe the architectural or structural change:",
    placeholder="e.g., Client increased Room 101 from 4m x 5m to 5m x 5m. Includes ceramic floor tiling, cement plastering, and brickwork.",
    height=120
)

if st.button("🚀 ANALYZE RIPPLE IMPACT", type="primary", use_container_width=True):
    if boq_df is None:
        st.error("Please upload a valid BOQ file or enable Sample BOQ.")
    elif not change_description.strip():
        st.error("Please enter a change description before running analysis.")
    else:
        with st.spinner("Analyzing inputs, performing calculations, and assessing risk..."):
            try:
                # Step 1: Drawing Analysis if provided
                drawing_notes = None
                if drawing_file:
                    st.toast("Inspecting drawing diagram...", icon="🖼️")
                    drawing_notes = analyze_drawing(drawing_file)
                
                # Step 2: AI Parameter Extraction
                st.toast("Extracting change parameters via Groq...", icon="🤖")
                boq_summary = get_boq_summary_list(boq_df)
                parsed_params = parse_change_to_parameters(change_description, boq_summary, drawing_notes)
                
                # Step 3: Deterministic Python Math
                st.toast("Computing exact quantities & costs in Python...", icon="🔢")
                calc_results = compute_boq_variances(parsed_params, boq_df)
                
                # Step 4: Qualitative Risk Analysis
                st.toast("Synthesizing downstream schedule & trade impacts...", icon="⚠️")
                risk_summary = analyze_ripple_impact(calc_results, parsed_params.get("change_summary", change_description))
                
                # Step 5: Render Dashboard Report
                render_dashboard(calc_results, risk_summary, drawing_notes)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
