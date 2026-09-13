import json
from config import get_groq_client, TEXT_MODEL

def parse_change_to_parameters(change_description, boq_items, drawing_context=""):
    """
    Uses openai/gpt-oss-120b on Groq to parse text description + drawing notes
    into structured JSON parameters. DO NOT perform math calculations here.
    """
    client = get_groq_client()
    
    system_prompt = """
    You are a Construction AI Assistant for CONSTRIQ.
    Your task is to identify affected BOQ items and extract dimension / quantity shift parameters.
    
    CRITICAL RULE: DO NOT CALCULATE COSTS OR FINAL TOTAL QUANTITIES. 
    Only extract structured initial and target dimensions/quantities.
    
    Return pure valid JSON matching this schema:
    {
      "change_summary": "Brief explanation of change",
      "affected_items": [
        {
          "item_id": "BOQ Item ID from provided list",
          "calculation_type": "area" OR "volume" OR "direct_qty",
          "old_dim_a": float or null,
          "old_dim_b": float or null,
          "new_dim_a": float or null,
          "new_dim_b": float or null,
          "old_direct_qty": float or null,
          "new_direct_qty": float or null
        }
      ]
    }
    """
    
    user_prompt = f"""
    BOQ Available Items:
    {json.dumps(boq_items, indent=2)}
    
    Drawing Vision Analysis Notes:
    {drawing_context if drawing_context else "No drawing provided."}
    
    User Change Description:
    "{change_description}"
    """
    
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Failed to parse AI JSON response: {str(e)}")
