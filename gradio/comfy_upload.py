
# Gradio → ComfyUI Upload with httpx
# Python

import gradio as gr
import httpx
import io
import numpy as np
from PIL import Image

# ComfyUI upload endpoint
COMFYUI_UPLOAD_URL = "http://127.0.0.1:8188/upload"  # Change to your ComfyUI server

def upload_to_comfyui(img):
    """
    img: Can be a file path (str), PIL.Image.Image, or NumPy array
    """
    # Convert to PIL.Image if needed
    if isinstance(img, str):
        image = Image.open(img)
    elif isinstance(img, np.ndarray):
        image = Image.fromarray(img)
    elif isinstance(img, Image.Image):
        image = img
    else:
        return "Unsupported image type"

    # Save image to in-memory buffer as PNG
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    # Send to ComfyUI
    try:
        with httpx.Client(timeout=30.0) as client:
            files = {"image": ("upload.png", buffer, "image/png")}
            response = client.post(COMFYUI_UPLOAD_URL, files=files)
            response.raise_for_status()
        return f"✅ Upload successful: {response.text}"
    except httpx.RequestError as e:
        return f"❌ Request error: {e}"
    except httpx.HTTPStatusError as e:
        return f"❌ HTTP error {e.response.status_code}: {e.response.text}"

# Gradio UI
demo = gr.Interface(
    fn=upload_to_comfyui,
    inputs=gr.Image(type="numpy"),  # Can be "numpy", "pil", or "filepath"
    outputs="text",
    title="Upload Image to ComfyUI"
)

if __name__ == "__main__":
    demo.launch()


# How It Works


# Gradio Image Component

# type="numpy" → NumPy array
# type="pil" → PIL.Image.Image
# type="filepath" → string path to file
# The function handles all three.



# Conversion to PNG

# We use Pillow to ensure the image is in a standard format.
# Save to an in-memory BytesIO buffer (no temp files needed).



# Upload with httpx

# Send as multipart/form-data with the correct MIME type.
# ComfyUI’s /upload endpoint will receive it as if it was uploaded from a browser.




# Tip for ComfyUI

# The field name in files ("image") must match what ComfyUI expects.
# If ComfyUI’s /upload expects "file", change:Pythonfiles = {"file": ("upload.png", buffer, "image/png")}


# If you want to send JPEG instead of PNG, just change:Pythonimage.save(buffer, format="JPEG")




# If you want, I can give you a version that streams the upload so it works for very large images without loading the whole file into memory.
# Do you want me to make that streaming version for ComfyUI? That would make it more efficient for big uploads.
