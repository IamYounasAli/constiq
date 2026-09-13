import streamlit as st
import pandas as pd
from utils import format_currency

def render_dashboard(calc_results, risk_data, drawing_notes=None):
    """
    Renders clean Streamlit output widgets for the complete CONSTRIQ summary.
    Includes AI Confidence scoring and User Verification points (MVP Features 10 & 11).
    """
    st.divider()
    st.header("📊 Executive Impact Dashboard")
    
    # Feature 10 & 11: AI Confidence & User Verification Point
    confidence = risk_data.get("confidence_score", "HIGH")
    reasoning = risk_data.get("confidence_reasoning", "Standard parametric match applied.")
    
    if confidence == "LOW":
        st.warning(f"⚠️ **Low AI Confidence Detected:** {reasoning}\n\n*Action Required:* Please manually verify the BOQ line items below before finalizing decisions.")
    elif confidence == "MEDIUM":
        st.info(f"🟡 **Medium AI Confidence:** {reasoning}")
    else:
        st.success(f"🎯 **High AI Confidence Rating:** {reasoning}")
    
    # 1. KPI Top Cards
    c1, c2, c3 = st.columns(3)
    
    cost_val = calc_results['total_cost_impact']
    cost_str = format_currency(cost_val)
    
    with c1:
        st.metric("Net Cost Variance", cost_str, delta=f"{cost_val:,.2f}", delta_color="inverse")
        
    with c2:
        total_items_affected = len(calc_results['items'])
        st.metric("BOQ Line Items Affected", f"{total_items_affected} items")
        
    with c3:
        risk_level = risk_data.get("risk_level", "MEDIUM")
        badge_color = "🟢" if risk_level == "LOW" else "🟡" if risk_level == "MEDIUM" else "🔴"
        st.metric("Overall Risk Rating", f"{badge_color} {risk_level}")

    # 2. Vision / Drawing Summary if present
    if drawing_notes:
        with st.expander("🖼️ Drawing Inspection Observations", expanded=False):
            st.write(drawing_notes)

    # 3. BOQ Quantity & Cost Impact Table
    st.subheader("📋 BOQ Quantity & Cost Variance Breakdown")
    if calc_results['items']:
        df_table = pd.DataFrame(calc_results['items'])
        df_display = df_table.rename(columns={
            "item_id": "Item ID",
            "description": "Description",
            "unit": "Unit",
            "rate": "Unit Rate (Rs.)",
            "old_qty": "Old Qty",
            "new_qty": "New Qty",
            "delta_qty": "Delta Qty",
            "cost_impact": "Cost Impact (Rs.)"
        })
        
        st.dataframe(
            df_display.style.format({
                "Unit Rate (Rs.)": "{:,.2f}",
                "Old Qty": "{:,.2f}",
                "New Qty": "{:,.2f}",
                "Delta Qty": "{:+,.2f}",
                "Cost Impact (Rs.)": "{:+,.2f}"
            }),
            use_container_width=True
        )
    else:
        st.info("No matching BOQ line items affected.")

    # 4. Multi-Category Qualitative Analysis
    st.subheader("🤖 AI Ripple Effect & Risk Synthesis")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"**📦 Supply Chain & Procurement:**\n\n{risk_data.get('supply_chain_impact')}")
        st.warning(f"**⏱️ Labor & Schedule Effects:**\n\n{risk_data.get('labor_schedule_impact')}")
        
    with col_b:
        st.error(f"**🏗️ Engineering & Field Actions:**\n\n{risk_data.get('engineering_site_actions')}")
        st.success(f"**📋 Final Recommendation:**\n\n{risk_data.get('overall_recommendation')}")
