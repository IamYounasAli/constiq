import json
from config import get_groq_client, VISION_MODEL
from utils import encode_image_to_base64

def analyze_drawing(image_file):
    """
    Uses Groq Multimodal Vision Model to extract drawing observations,
    modified dimensions, and annotations.
    """
    client = get_groq_client()
    base64_image = encode_image_to_base64(image_file)
    
    prompt = """
    You are an expert Civil & Architectural Drawing Inspector.
    Analyze this construction drawing / plan carefully.
    
    Extract and list all relevant architectural/structural details:
    1. Room/Area designations and explicit dimensions shown (e.g., Room 101: 4m x 5m).
    2. Any revision markers, cloudings, notes, or handwritten annotations.
    3. Material callouts (e.g., tile flooring, brickwork, plaster).
    
    Provide a concise, factual summary of what is visible in the drawing.
    """
    
    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.1,
        max_tokens=1000
    )
    
    return response.choices[0].message.content
