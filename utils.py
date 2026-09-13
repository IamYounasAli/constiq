import base64
from PIL import Image
import io

def encode_image_to_base64(image_file):
    """Converts uploaded Streamlit image file to Base64 string."""
    image = Image.open(image_file)
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def format_currency(amount, currency="Rs."):
    """Formats numerical value to clean currency standard."""
    if amount >= 0:
        return f"{currency} {amount:,.2f}"
    else:
        return f"- {currency} {abs(amount):,.2f}"
