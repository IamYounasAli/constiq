import json
import io
import base64
import pypdfium2 as pdfium
from PIL import Image
from config import get_groq_client, VISION_MODEL

def process_drawing_file(file_buffer):
    """
    Helper function: Accepts an uploaded file buffer (PNG, JPG, or PDF).
    If PDF, converts the first page to a high-res PNG image.
    Returns a valid Data URL string for Groq Vision API.
    """
    if not file_buffer:
        return None

    file_name = getattr(file_buffer, 'name', '').lower()

    if hasattr(file_buffer, 'seek'):
        file_buffer.seek(0)

    # 1. Handle PDF Drawings
    if file_name.endswith('.pdf'):
        pdf = pdfium.PdfDocument(file_buffer)
        first_page = pdf[0]
        # Render at 200 DPI for high architectural clarity
        rendered_img = first_page.render(scale=200 / 72).to_pil()

        img_byte_arr = io.BytesIO()
        rendered_img.save(img_byte_arr, format='PNG')
        encoded_string = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{encoded_string}"

    # 2. Handle PNG, JPG, JPEG Images
    else:
        file_bytes = file_buffer.read()
        encoded_string = base64.b64encode(file_bytes).decode('utf-8')
        mime_type = "image/png" if file_name.endswith('.png') else "image/jpeg"
        return f"data:{mime_type};base64,{encoded_string}"


def analyze_drawing(image_file):
    """
    Legacy single-drawing inspector (backward compatible).
    """
    return analyze_drawing_comparison(image_file, None)


def analyze_drawing_comparison(old_img_file, new_img_file=None):
    """
    Uses Groq Multimodal Vision Model to inspect single or dual architectural drawings.
    Supports PNG, JPG, and PDF formats seamlessly.
    """
    if not old_img_file and not new_img_file:
        return "No drawing files provided for visual verification."

    client = get_groq_client()

    # Case 1: Single Drawing Uploaded
    if not old_img_file or not new_img_file:
        single_img = old_img_file or new_img_file
        data_url = process_drawing_file(single_img)

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
                                "url": data_url
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
    old_data_url = process_drawing_file(old_img_file)
    new_data_url = process_drawing_file(new_img_file)

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
                            "url": old_data_url
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": new_data_url
                        }
                    }
                ]
            }
        ],
        temperature=0.1,
        max_tokens=1000
    )
    return response.choices[0].message.content
