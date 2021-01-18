#!/usr/bin/env python

import libpy


for item in libpy.FILES:
    html = libpy.get_html(item)
    libpy.fetch_images(html)
    libpy.replace_image_url(item)
