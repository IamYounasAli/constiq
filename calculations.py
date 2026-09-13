import pandas as pd

def compute_boq_variances(parsed_json, boq_df):
    """
    Pure Python calculation core.
    Computes exact Old Qty, New Qty, Delta Qty, and Delta Cost.
    Compatible with both single BOQ and Dual-PDF BOQ workflows.
    """
    results = []
    total_cost_impact = 0.0
    
    affected_items = parsed_json.get("affected_items", [])
    
    for item in affected_items:
        item_id = str(item.get("item_id", "")).strip()
        
        # Match with provided BOQ DataFrame if available
        boq_matches = pd.DataFrame()
        if boq_df is not None and not boq_df.empty and 'item_id' in boq_df.columns:
            boq_matches = boq_df[boq_df['item_id'].astype(str).str.strip() == item_id]
            
        rate = float(item.get("rate", 0.0))
        unit = item.get("unit", "units")
        description = item.get("description", "Unknown Line Item")
        
        if not boq_matches.empty:
            boq_row = boq_matches.iloc[0]
            rate = float(boq_row.get('rate', rate))
            unit = str(boq_row.get('unit', unit))
            description = str(boq_row.get('description', description))
            
        # Determine Old and New quantities
        calc_type = item.get("calculation_type", "direct_qty")
        if calc_type == "area":
            old_q = (float(item.get("old_dim_a") or 0.0)) * (float(item.get("old_dim_b") or 0.0))
            new_q = (float(item.get("new_dim_a") or 0.0)) * (float(item.get("new_dim_b") or 0.0))
        else:
            old_q = float(item.get("old_qty") or item.get("old_direct_qty") or 0.0)
            new_q = float(item.get("new_qty") or item.get("new_direct_qty") or 0.0)
            
        delta_q = new_q - old_q
        delta_cost = delta_q * rate
        total_cost_impact += delta_cost
        
        results.append({
            "item_id": item_id,
            "description": description,
            "unit": unit,
            "rate": rate,
            "old_qty": old_q,
            "new_qty": new_q,
            "delta_qty": delta_q,
            "cost_impact": delta_cost,  # Keeps report.py working smoothly
            "delta_cost": delta_cost
        })
        
    return {
        "items": results,
        "total_cost_impact": total_cost_impact
    }
