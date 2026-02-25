# Load an image from your local filesystem into a NumPy array using PIL (Pillow) and NumPy.
# This is useful if you already have the image saved locally and want to process it in Python.
from PIL import Image
import numpy as np
import os
import anyio

def load_async_image(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    
    # Open the image with PIL and ensure RGB format
    img = Image.open(file_path).convert("RGB")
    # Convert to NumPy array
    img_array = np.array(img)

    return img_array


async def load_image_file_to_numpy(file_path):
    """
    Loads an image from the filesystem into a NumPy array.
    :param file_path: Path to the image file.
    :return: NumPy array (H, W, C) or None if loading fails.
    """
    try:
        img_array = await anyio.to_thread.run_sync(load_async_image, file_path)
        print(f"Image loaded: shape={img_array.shape}, dtype={img_array.dtype}")
        return img_array

    except (OSError, IOError) as e:
        print(f"Error loading image: {e}")
        return None


# Example usage
if __name__ == "__main__":
    pass
    # image_path = "example.jpg"  # Replace with your local image path
    # img_array = load_image_file_to_numpy(image_path)

    # if img_array is not None:
    #     print("First pixel RGB values:", img_array[0, 0])

    # How it works

    # Check file existence with os.path.isfile() to avoid errors.
    # Open the image with PIL.Image.open() and convert to "RGB" for consistent color channels.
    # Convert to a NumPy array with np.array(img).
    # The resulting array has shape (height, width, channels).

    # Install dependencies
    # pip install pillow numpy
