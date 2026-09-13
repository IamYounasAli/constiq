import pandas as pd

def compute_boq_variances(parsed_json, boq_df=None):
    """
    Pure Python calculation engine.
    Computes exact Old Qty, New Qty, Delta Qty, and Cost Impact.
    Works seamlessly with single BOQ and Dual-PDF BOQ extractions.
    """
    results = []
    total_cost_impact = 0.0
    
    affected_items = parsed_json.get("affected_items", [])
    
    for item in affected_items:
        item_id = str(item.get("item_id", "")).strip()
        description = item.get("description", "BOQ Item")
        unit = item.get("unit", "units")
        rate = float(item.get("rate") or 0.0)
        
        # Look for matching row in BOQ DataFrame if provided
        if boq_df is not None and not boq_df.empty and 'item_id' in boq_df.columns:
            boq_matches = boq_df[boq_df['item_id'].astype(str).str.strip() == item_id]
            if not boq_matches.empty:
                boq_row = boq_matches.iloc[0]
                rate = float(boq_row.get('rate', rate))
                unit = str(boq_row.get('unit', unit))
                description = str(boq_row.get('description', description))
                
        # Extract Old and New quantities safely
        calc_type = item.get("calculation_type", "direct_qty")
        if calc_type == "area":
            old_q = float(item.get("old_dim_a") or 0.0) * float(item.get("old_dim_b") or 0.0)
            new_q = float(item.get("new_dim_a") or 0.0) * float(item.get("new_dim_b") or 0.0)
        else:
            old_q = float(item.get("old_qty") if item.get("old_qty") is not None else item.get("old_direct_qty") or 0.0)
            new_q = float(item.get("new_qty") if item.get("new_qty") is not None else item.get("new_direct_qty") or 0.0)
            
        delta_q = new_q - old_q
        cost_impact = delta_q * rate
        total_cost_impact += cost_impact
        
        results.append({
            "item_id": item_id,
            "description": description,
            "unit": unit,
            "rate": rate,
            "old_qty": old_q,
            "new_qty": new_q,
            "delta_qty": delta_q,
            "cost_impact": cost_impact,
            "delta_cost": cost_impact
        })
        
    return {
        "items": results,
        "total_cost_impact": total_cost_impact
    }
