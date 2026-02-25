
# Async ComfyUI Image Fetcher in Gradio
# Python

import httpx
import gradio as gr

COMFYUI_URL = "http://localhost:8188/view"  # Change to your ComfyUI server
IMAGE_ID = "example.png"  # Default image ID

async def fetch_image_async(image_id: str):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Fetch image bytes directly
            resp = await client.get(f"{COMFYUI_URL}?filename={image_id}")
            resp.raise_for_status()
            return resp.content  # Gradio can handle raw bytes for images

    except httpx.RequestError as e:
        return f"❌ Network error: {e}"
    except httpx.HTTPStatusError as e:
        return f"❌ Server error {e.response.status_code}: {e.response.text}"

# Gradio UI
with gr.Blocks() as demo:
    image_id_input = gr.Textbox(value=IMAGE_ID, label="Image ID")
    output_image = gr.Image(type="pil", label="Downloaded Image")
    fetch_btn = gr.Button("Fetch from ComfyUI (Async)")

    # Gradio supports async functions directly
    fetch_btn.click(fn=fetch_image_async, inputs=image_id_input, outputs=output_image)

if __name__ == "__main__":
    demo.launch()


# Why This Works Well

# Non-blocking: Uses httpx.AsyncClient so downloads happen without freezing the UI.
# Direct bytes → Gradio: No temp files, no extra processing.
# Error handling: Still catches both network and HTTP errors.
# Drop-in: Works exactly like the sync version, just faster for multiple requests.


# 💡 Pro Tip: If you expect to fetch multiple images in parallel (e.g., a gallery), you can await asyncio.gather() inside the async function to download them concurrently.

# If you want, I can extend this so it downloads multiple ComfyUI images at once and displays them in a Gradio gallery — which is great for batch outputs.
# Do you want me to make that version next?
