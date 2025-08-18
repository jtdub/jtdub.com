#!/usr/bin/env python3

import re
import os

dirs = ["../_posts", "../_drafts"]

for dir in dirs:
    os.chdir(dir)

    for item in os.listdir():
        if os.path.isfile(item):
            with open(item) as f:
                data = re.sub(
                    "(\d{4}-\d{1,2}-\d{1,2})(\w\d+:\d+\d:\d+\.\d+-\d+:\d+)",
                    "\\1",
                    f.read(),
                )

            with open(item, "w") as f:
                f.write(data)
