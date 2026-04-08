"""Cross-post Jekyll blog posts to Substack via email publishing."""

import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import frontmatter
import markdown
import yaml
from dotenv import load_dotenv


def get_site_url(config_path="_config.yml"):
    """Read the site URL from Jekyll's _config.yml."""
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config.get("url", "")


def parse_post(filepath):
    """Parse a Jekyll post file and return its metadata and content.

    Returns a dict with keys: title, date, tags, substack, body.
    """
    post = frontmatter.load(filepath)
    return {
        "title": post.get("title", ""),
        "date": str(post.get("date", "")),
        "tags": post.get("tags", []),
        "substack": post.get("substack", False),
        "body": post.content,
    }


def markdown_to_html(body, site_url=""):
    """Convert markdown body to HTML, resolving relative image URLs."""
    extensions = ["fenced_code", "tables", "codehilite"]
    html = markdown.markdown(body, extensions=extensions)

    if site_url:
        # Resolve relative src="/images/..." and href="/images/..." to absolute URLs
        html = re.sub(
            r'(src|href)="(/[^"]*)"',
            lambda m: f'{m.group(1)}="{site_url}{m.group(2)}"',
            html,
        )

    return html


def send_to_substack(title, html_body, is_draft=False):
    """Send an email to the Substack publishing address."""
    substack_email = os.environ["SUBSTACK_EMAIL_ADDRESS"]
    smtp_host = os.environ.get("SMTP_HOST", "127.0.0.1")
    smtp_port = int(os.environ.get("SMTP_PORT", "1025"))
    smtp_user = os.environ["SMTP_USER"]
    smtp_password = os.environ["SMTP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    subject = f"[draft] {title}" if is_draft else title
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = substack_email

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

    print(f"{'Draft' if is_draft else 'Post'} sent to Substack: {title}")
    return True


def crosspost(filepath, force=False, draft=False):
    """Cross-post a Jekyll blog post to Substack.

    Args:
        filepath: Path to the Jekyll markdown post.
        force: If True, send even if substack frontmatter flag is not set.
        draft: If True, send as a Substack draft regardless of frontmatter value.

    Returns:
        True if sent, False if skipped.
    """
    load_dotenv()

    post = parse_post(filepath)

    substack_flag = post["substack"]
    if not force and not substack_flag:
        print(f"Skipping {filepath} (no substack flag, use --force to override)")
        return False

    is_draft = draft or substack_flag == "draft"

    site_url = get_site_url()
    html_body = markdown_to_html(post["body"], site_url)

    return send_to_substack(post["title"], html_body, is_draft=is_draft)
