import pytest
import bs4
import requests

def test_external_images(posts_path):
    for item in posts_path["files"]:
        with open(f"{posts_path['path']}/{item}") as f:
            data = f.read()

        soup = bs4.BeautifulSoup(data, "html.parser")

        for image in soup.find_all("img"):
            image_url = image["src"]

            # Ensure the image URL is a fully qualified URL (e.g., starts with http:// or https://)
            if not image_url.startswith(("http://", "https://")):
                pytest.fail(f"Image URL is not fully qualified: {image_url}")

            try:
                # Request the image URL
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()  # Raise an error for HTTP codes >= 400
            except requests.RequestException as e:
                pytest.fail(f"Failed to fetch image: {image_url} - {e}")
