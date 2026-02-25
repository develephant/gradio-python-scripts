# Got it ✅ — here’s a ready-to-use async wrapper for Pillow so you can safely use it inside asyncio applications (e.g., FastAPI, aiohttp) without blocking the event loop.
# This wrapper uses asyncio.to_thread() (Python 3.9+) to run Pillow’s blocking operations in a background thread.

# Async Pillow Helper
# Python

import asyncio
from pathlib import Path
from typing import Callable, Any
from PIL import Image


class AsyncImage:
    """Async wrapper for common Pillow operations."""

    def __init__(self, image: Image.Image):
        self.image = image

    @classmethod
    async def open(cls, path: str | Path) -> "AsyncImage":
        """Open an image asynchronously."""
        def _open():
            return Image.open(path)

        img = await asyncio.to_thread(_open)
        return cls(img)

    async def save(self, path: str | Path, **kwargs) -> None:
        """Save the image asynchronously."""
        await asyncio.to_thread(self.image.save, path, **kwargs)

    async def convert(self, mode: str) -> "AsyncImage":
        """Convert image mode asynchronously."""
        def _convert():
            return self.image.convert(mode)

        new_img = await asyncio.to_thread(_convert)
        return AsyncImage(new_img)

    async def apply(self, func: Callable[[Image.Image], Any]) -> Any:
        """
        Apply a custom Pillow function asynchronously.
        Example: await img.apply(lambda im: im.resize((100, 100)))
        """
        return await asyncio.to_thread(func, self.image)


# ---------------- Example Usage ----------------
async def main():
    pass

    # Open image without blocking event loop
    # img = await AsyncImage.open("input.jpg")

    # Convert to grayscale
    # img_gray = await img.convert("L")

    # Save result
    # await img_gray.save("output.jpg")

    # print("✅ Image processed asynchronously.")


if __name__ == "__main__":
    asyncio.run(main())


# Features

# Non-blocking: All Pillow calls run in a background thread.
# Chainable: You can open, convert, resize, and save without freezing async code.
# Custom operations: Use .apply() to run any Pillow function asynchronously.

# Python

# from fastapi import FastAPI, UploadFile
# import shutil

# app = FastAPI()

# @app.post("/upload/")
# async def upload_image(file: UploadFile):
#     temp_path = f"temp_{file.filename}"
#     with open(temp_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     img = await AsyncImage.open(temp_path)
#     img_gray = await img.convert("L")
#     output_path = f"gray_{file.filename}"
#     await img_gray.save(output_path)

#     return {"message": "Image processed", "output": output_path}


# If you want, I can extend this helper to automatically detect CPU-heavy operations and run them in a process pool for even better performance on large images.
# That would make it truly scalable for production async apps.
# Do you want me to upgrade it for thread + process pool hybrid async image processing?
