
# Asynchronous Upload
# Python

import httpx
import asyncio
import os

async def upload_image_async(url: str, image_path: str):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            with open(image_path, "rb") as img_file:
                files = {"file": (os.path.basename(image_path), img_file, "image/jpeg")}
                response = await client.post(url, files=files)

            response.raise_for_status()
            print("✅ Upload successful:", response.text)

        except httpx.RequestError as e:
            print(f"❌ Request error: {e}")
        except httpx.HTTPStatusError as e:
            print(f"❌ Server returned error {e.response.status_code}: {e.response.text}")

# Example usage
if __name__ == "__main__":
    asyncio.run(upload_image_async("https://example.com/upload", "my_image.jpg"))


# Key Points

# files parameter:

# Format: {"field_name": (filename, file_object, content_type)}
# "file" should match the server’s expected form field name.


# Timeouts: Always set a timeout to avoid hanging requests.
# Error Handling:

# httpx.RequestError → Network issues.
# httpx.HTTPStatusError → Server returned a non-2xx status.


# Content Type: Change "image/jpeg" to "image/png" or another type if needed.


# If you want, I can also show you how to send an image as raw binary instead of multipart/form-data using httpx — which is useful for APIs that expect raw uploads.
# Do you want me to include that?
