#!/usr/bin/env python

import os
import bs4
import shutil
import requests
import html2markdown


CWD = os.getcwd()
PATH = CWD.split("/")[:-1]
PATH.append("_posts")
PATH = "/".join(PATH)
FILES = os.listdir(PATH)


def convert_html(html: str):
    return html2markdown.convert(html)


def get_html(file_name: str):
    with open("/".join([PATH, file_name])) as f:
        header = 0
        while header <= 1:
            line = f.readline()
            if "---" in line:
                header += 1
        html = f.readlines()[-1]
    return html

def fetch_images(html_data: str, output_dir: str = "images"):
    soup = bs4.BeautifulSoup(html_data, "html.parser")

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for item in soup.find_all("a"):
        if item["href"].lower().endswith("png") or item["href"].lower().endswith("jpg"):
            image = requests.get(item["href"], stream=True)
            if image.ok:
                image.raw.decode_content = True
                file_name = item["href"].split("/")[-1]
                print(f"saving {file_name}")
                with open(f"{output_dir}/{file_name}", "wb") as f:
                    shutil.copyfileobj(image.raw, f)
            else:
                print(f"error downloading {item['href']} with status code {image.status_code}")
    


for item in FILES:
    html = get_html(item)
    fetch_images(html)

