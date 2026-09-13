import json
from config import get_groq_client, VISION_MODEL
from utils import encode_image_to_base64

def analyze_drawing(image_file):
    """
    Legacy single-drawing inspector (backward compatible).
    """
    return analyze_drawing_comparison(image_file, None)

def analyze_drawing_comparison(old_img_file, new_img_file=None):
    """
    Uses Groq Multimodal Vision Model to inspect single or dual architectural drawings.
    Compares Old vs Revised drawings when both are provided.
    """
    if not old_img_file and not new_img_file:
        return "No drawing files provided for visual verification."

    client = get_groq_client()

    # Case 1: Single Drawing Uploaded
    if not old_img_file or not new_img_file:
        single_img = old_img_file or new_img_file
        base64_image = encode_image_to_base64(single_img)

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

    # Case 2: Dual Drawing Comparison (Old vs. Revised)
    old_b64 = encode_image_to_base64(old_img_file)
    new_b64 = encode_image_to_base64(new_img_file)

    comparison_prompt = """
    You are an expert Civil & Architectural Drawing Inspector for CONSTRIQ.
    Compare these TWO architectural drawings (Image 1: Old Drawing vs Image 2: Revised Drawing).

    Identify and list all visual changes between the two:
    1. Spatial & structural layout modifications (wall shifts, room size changes, door/window additions).
    2. Dimension differences (e.g., Old Room 101: 4m x 5m vs Revised: 5m x 5m).
    3. Revision clouds, modified annotations, or updated material callouts.

    Provide a concise, factual change summary to help quantity surveyors trace BOQ impacts.
    """

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": comparison_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{old_b64}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{new_b64}"
                        }
                    }
                ]
            }
        ],
        temperature=0.1,
        max_tokens=1000
    )
    return response.choices[0].message.content
