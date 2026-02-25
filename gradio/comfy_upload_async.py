
# Async Version — Gradio + httpx + ComfyUI
# Python

import gradio as gr
import httpx
import io
import numpy as np
from PIL import Image

COMFYUI_UPLOAD_URL = "http://127.0.0.1:8188/upload"  # Change to your ComfyUI server

async def upload_to_comfyui_async(img):
    """
    Async upload to ComfyUI from Gradio Image component.
    img can be: file path (str), PIL.Image.Image, or NumPy array.
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

    # Async upload
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            files = {"image": ("upload.png", buffer, "image/png")}
            response = await client.post(COMFYUI_UPLOAD_URL, files=files)
            response.raise_for_status()
        return f"Upload successful: {response.text}"
    except httpx.RequestError as e:
        return f"Request error: {e}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error {e.response.status_code}: {e.response.text}"

# Gradio async interface
demo = gr.Interface(
    fn=upload_to_comfyui_async,
    inputs=gr.Image(type="numpy"),  # Can be "numpy", "pil", or "filepath"
    outputs="text",
    title="Async Upload Image to ComfyUI"
)

if __name__ == "__main__":
    demo.launch()


# Key Notes

# Gradio supports async functions directly — if your fn is async def, Gradio will await it automatically.
# httpx.AsyncClient is used instead of httpx.Client.
# This approach is non-blocking — multiple uploads can happen in parallel if your server supports it.
# The files dict is still the same as in the sync version — ComfyUI’s /upload endpoint doesn’t care whether the request is sync or async.


# ✅ When to use async

# If you expect large images or multiple concurrent uploads.
# If your Gradio app will also be doing other network calls in parallel (e.g., triggering ComfyUI workflows after upload).


# If you want, I can extend this so that after uploading, it immediately triggers a ComfyUI workflow in the same async function — that way the upload and processing happen in one step.
# Do you want me to make that combined upload + workflow trigger version?
