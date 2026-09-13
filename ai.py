import json
from config import get_groq_client, TEXT_MODEL

def parse_pdf_boq_changes(old_boq_text, new_boq_text, drawing_context=""):
    """
    Uses Groq text model to compare Old BOQ text vs New BOQ text
    and correlate changes with drawing notes.
    """
    client = get_groq_client()
    
    system_prompt = """
    You are an expert Quantity Surveyor and Construction AI Assistant for CONSTRIQ.
    Compare the text from an OLD BOQ PDF and a NEW BOQ PDF, identify all changed items,
    and correlate them with architectural drawing notes if available.
    
    CRITICAL RULE: Extract exact item IDs, descriptions, old quantities, and new quantities.
    
    Return pure valid JSON matching this schema:
    {
      "change_summary": "Brief overall summary of revisions identified between the BOQs",
      "affected_items": [
        {
          "item_id": "BOQ Item ID or matched identifier",
          "description": "Item description",
          "unit": "Unit of measurement",
          "rate": float,
          "old_qty": float,
          "new_qty": float
        }
      ]
    }
    """
    
    user_prompt = f"""
    --- OLD BOQ PDF CONTENT ---
    {old_boq_text[:4000]}
    
    --- NEW BOQ PDF CONTENT ---
    {new_boq_text[:4000]}
    
    --- DRAWING VISION NOTES ---
    {drawing_context if drawing_context else "No drawing diagram provided."}
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
