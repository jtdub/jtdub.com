#!/usr/bin/env python3

import os
import re
from datetime import datetime

# Archive notice template
ARCHIVE_NOTICE = """
<div class="alert alert-warning" role="alert">
  <strong>📚 Archived Content:</strong> This post is part of my historical study notes archive. While some concepts may remain relevant, the specific technologies, procedures, and certifications mentioned may be outdated. For current technical content, visit the <a href="/technology/" class="alert-link">Technology</a> section.
</div>
"""


def add_archive_notice(file_path):
    """Add archive notice to a post file if it doesn't already have one."""

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if archive notice already exists
    if "Archived Content:" in content:
        print(f"Archive notice already exists in {file_path}")
        return False

    # Find the end of the front matter and the start of content
    front_matter_end = content.find("---", 3)  # Find second occurrence of ---
    if front_matter_end == -1:
        print(f"Could not find front matter end in {file_path}")
        return False

    # Find the start of the first content section
    content_start = front_matter_end + 3
    while content_start < len(content) and content[content_start] in ["\n", "\r"]:
        content_start += 1

    # Insert archive notice
    new_content = (
        content[:content_start] + ARCHIVE_NOTICE + "\n" + content[content_start:]
    )

    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Added archive notice to {file_path}")
    return True


def main():
    posts_dir = "/Users/jtdub/Documents/code/jtdub.com/_posts"

    # Get all posts from 2009-2014 with "Study Notes" in them
    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md"):
            continue

        # Check if it's from 2009-2014
        year_match = re.match(r"(\d{4})-", filename)
        if not year_match:
            continue

        year = int(year_match.group(1))
        if year > 2014:
            continue

        file_path = os.path.join(posts_dir, filename)

        # Check if it contains study notes
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "Study Notes" in content:
            add_archive_notice(file_path)


if __name__ == "__main__":
    main()
