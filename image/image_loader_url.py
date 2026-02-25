# Got it ✅ — here’s how you can load an image directly from a URL into PIL without saving it to disk first.
# We’ll use requests to fetch the image and BytesIO to treat it like a file in memory.
# Python

from PIL import Image
import requests
from io import BytesIO

def load_image_from_url(url):
    """
    Loads an image from a given URL into a PIL Image object.
    :param url: Direct link to the image.
    :return: PIL Image object or None if loading fails.
    """
    try:
        # Fetch the image from the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes

        # Open the image from the response content
        img = Image.open(BytesIO(response.content))
        img.load()  # Ensure it's fully loaded into memory

        print(f"Image loaded successfully: {img.format}, {img.size}, {img.mode}")
        return img

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except (OSError, IOError) as e:
        print(f"Error loading image: {e}")
    return None


# Example usage
if __name__ == "__main__":
    image_url = "https://www.example.com/sample.jpg"  # Replace with a real image URL
    image = load_image_from_url(image_url)

    if image:
        image.show()  # Opens in default image viewer

# How it works:

# requests.get(url) → Downloads the image data.
# BytesIO(response.content) → Wraps the raw bytes in a file-like object.
# Image.open() → Reads the image directly from memory.
# .show() → Opens it in your default viewer.

# Install dependencies:
# pip install pillow requests
