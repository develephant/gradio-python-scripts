# Unified image loader that can handle both local filesystem paths and URLs and return a NumPy array.
# It will:

# Detect if the input is a URL or a local file.
# Load the image using PIL.
# Convert it to RGB for consistency.
# Return it as a NumPy array.
from PIL import Image
import numpy as np
import requests
from io import BytesIO
import os

def load_image_to_numpy(source):
    """
    Loads an image from a local file or URL into a NumPy array (RGB).
    
    :param source: File path or URL string.
    :return: NumPy array (H, W, C) or None if loading fails.
    """
    try:
        # Check if source is a URL
        if isinstance(source, str) and source.lower().startswith(("http://", "https://")):
            # Load from URL
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            # Load from local file
            if not os.path.isfile(source):
                print(f"Error: File '{source}' not found.")
                return None
            img = Image.open(source).convert("RGB")

        # Convert to NumPy array
        img_array = np.array(img)
        print(f"Image loaded: shape={img_array.shape}, dtype={img_array.dtype}")
        return img_array

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except (OSError, IOError) as e:
        print(f"Error loading image: {e}")
    return None


# Example usage
if __name__ == "__main__":
    # Local file example
    # local_path = "example.jpg"  # Replace with your local image path
    # arr_local = load_image_to_numpy(local_path)

    # URL example
    # image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/640px-PNG_transparency_demonstration_1.png"
    # arr_url = load_image_to_numpy(image_url)


# How it works

# Detects source type:

# If it starts with http:// or https:// → treat as URL.
# Otherwise → treat as local file path.

# Loads image:

# From URL → requests.get() + BytesIO.
# From file → Image.open().

# Converts to RGB for consistent color channels.
# Converts to NumPy array for processing.

# Install dependencies
# pip install pillow numpy requests
