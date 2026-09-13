def compute_boq_variances(parsed_json, boq_df):
    """
    Pure Python calculation core.
    Calculates exact Old Qty, New Qty, Delta Qty, and Delta Cost.
    """
    results = []
    total_cost_impact = 0.0
    
    affected_items = parsed_json.get("affected_items", [])
    
    for item in affected_items:
        item_id = str(item.get("item_id"))
        boq_matches = boq_df[boq_df['item_id'].astype(str) == item_id]
        
        if boq_matches.empty:
            continue
            
        boq_row = boq_matches.iloc[0]
        calc_type = item.get("calculation_type", "direct_qty")
        
        if calc_type == "area":
            old_q = (item.get("old_dim_a") or 0.0) * (item.get("old_dim_b") or 0.0)
            new_q = (item.get("new_dim_a") or 0.0) * (item.get("new_dim_b") or 0.0)
        elif calc_type == "direct_qty":
            old_q = float(item.get("old_direct_qty") or boq_row['current_qty'])
            new_q = float(item.get("new_direct_qty") or 0.0)
        else:
            old_q = float(boq_row['current_qty'])
            new_q = float(item.get("new_direct_qty") or old_q)
            
        delta_q = new_q - old_q
        rate = float(boq_row['rate'])
        cost_impact = delta_q * rate
        total_cost_impact += cost_impact
        
        results.append({
            "item_id": item_id,
            "description": boq_row['description'],
            "unit": boq_row['unit'],
            "rate": rate,
            "old_qty": old_q,
            "new_qty": new_q,
            "delta_qty": delta_q,
            "cost_impact": cost_impact
        })
        
    return {
        "items": results,
        "total_cost_impact": total_cost_impact
    }
