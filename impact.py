import json
from config import get_groq_client, TEXT_MODEL

def analyze_ripple_impact(calc_results, change_summary, confidence_data=None):
    """
    Uses openai/gpt-oss-120b on Groq to perform qualitative project management analysis.
    Evaluates downstream schedule, material procurement, trades, and site risks.
    Attaches confidence ratings (MVP Features 10 & 11) when provided.
    """
    client = get_groq_client()
    
    system_prompt = """
    You are an expert Senior Construction Project Manager.
    Analyze the provided quantitative change metrics and write a professional qualitative risk & ripple impact analysis.
    
    Return pure valid JSON matching this schema:
    {
      "risk_level": "LOW" | "MEDIUM" | "HIGH",
      "supply_chain_impact": "Details on materials, lead times, or supplier batches",
      "labor_schedule_impact": "Details on trade coordination, man-hours, curing times, delay risk",
      "engineering_site_actions": "Key field verification steps or safety/structural checks required",
      "overall_recommendation": "Executive summary recommendation for approval or review"
    }
    """
    
    user_prompt = f"""
    Change Description Summary: {change_summary}
    Calculated Cost Impact: Rs. {calc_results['total_cost_impact']:,.2f}
    
    Item Variance Table Data:
    {json.dumps(calc_results['items'], indent=2)}
    """
    
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    
    try:
        risk_summary = json.loads(response.choices[0].message.content)
        
        # Attach confidence metadata if provided from the BOQ extraction stage
        if confidence_data and isinstance(confidence_data, dict):
            risk_summary["confidence_score"] = confidence_data.get("confidence_score", "HIGH")
            risk_summary["confidence_reasoning"] = confidence_data.get("confidence_reasoning", "Standard parametric extraction applied.")
        else:
            risk_summary["confidence_score"] = "HIGH"
            risk_summary["confidence_reasoning"] = "Standard parametric extraction applied."
            
        return risk_summary
    except Exception as e:
        raise Exception(f"Failed to parse Risk Analysis response: {str(e)}")
