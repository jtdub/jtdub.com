import pytest
import bs4
import requests


def test_image(posts_path):
    for item in posts_path["files"]:
        with open(f"{posts_path['path']}/{item}") as f:
            data = f.read()

        soup = bs4.BeautifulSoup(data, "html.parser")

        for image in soup.find_all("img"):
            response = requests.get(f"http://localhost:4000/{image['src']}")
            assert response.ok
