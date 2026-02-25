import asyncio
from pathlib import Path
from typing import Callable, Any, Optional
from PIL import Image


class AsyncPillow:
    """Async wrapper for common Pillow operations."""

    @staticmethod
    async def open(path: str | Path) -> Image.Image:
        """Open an image asynchronously."""
        return await asyncio.to_thread(Image.open, path)

    @staticmethod
    async def save(image: Image.Image, path: str | Path, **kwargs) -> None:
        """Save an image asynchronously."""
        await asyncio.to_thread(image.save, path, **kwargs)

    @staticmethod
    async def process(path_in: str | Path, path_out: str | Path,
                      processor: Optional[Callable[[Image.Image], Image.Image]] = None,
                      **save_kwargs) -> None:
        """
        Open, optionally process, and save an image asynchronously.

        :param path_in: Input image path
        :param path_out: Output image path
        :param processor: Function that takes and returns a Pillow Image
        :param save_kwargs: Extra arguments for Image.save()
        """
        def _task():
            with Image.open(path_in) as img:
                if processor:
                    img = processor(img)
                img.save(path_out, **save_kwargs)

        await asyncio.to_thread(_task)


# ---------------- Example Usage ----------------
async def main():
    # Example 1: Open and save without blocking
    img = await AsyncPillow.open("input.jpg")
    img = img.convert("L")  # Convert to grayscale
    await AsyncPillow.save(img, "output_gray.jpg")

    # Example 2: Use processor function
    async def resize_example():
        await AsyncPillow.process(
            "input.jpg",
            "output_resized.jpg",
            processor=lambda im: im.resize((300, 300)),
            quality=90
        )

    await resize_example()
    print("Images processed asynchronously without blocking the event loop.")


if __name__ == "__main__":
    asyncio.run(main())
