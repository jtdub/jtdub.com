"""Tests for the Substack cross-posting module."""

import os
from unittest.mock import MagicMock, patch

import pytest

from scripts.substack import crosspost, markdown_to_html, parse_post, send_to_substack


@pytest.fixture
def sample_post(tmp_path):
    """Create a sample Jekyll post file."""
    content = """---
layout: post
title: "Test Post Title"
date: '2026-04-08'
author: jtdub
tags:
  - python
  - testing
substack: true
---

This is the post body.

![An image](/images/test.png)

```python
print("hello")
```

| Col A | Col B |
|-------|-------|
| 1     | 2     |
"""
    post_file = tmp_path / "2026-04-08-test-post.md"
    post_file.write_text(content)
    return str(post_file)


@pytest.fixture
def sample_post_no_substack(tmp_path):
    """Create a sample Jekyll post without substack flag."""
    content = """---
layout: post
title: "No Substack Post"
date: '2026-04-08'
author: jtdub
tags:
  - misc
---

Just a regular post.
"""
    post_file = tmp_path / "2026-04-08-no-substack.md"
    post_file.write_text(content)
    return str(post_file)


@pytest.fixture
def sample_post_draft(tmp_path):
    """Create a sample Jekyll post with substack: draft."""
    content = """---
layout: post
title: "Draft Post"
date: '2026-04-08'
author: jtdub
substack: draft
---

A draft post for review.
"""
    post_file = tmp_path / "2026-04-08-draft-post.md"
    post_file.write_text(content)
    return str(post_file)


class TestParsePost:
    def test_with_substack_flag(self, sample_post):
        result = parse_post(sample_post)
        assert result["title"] == "Test Post Title"
        assert result["substack"] is True
        assert "python" in result["tags"]
        assert "This is the post body." in result["body"]

    def test_without_substack_flag(self, sample_post_no_substack):
        result = parse_post(sample_post_no_substack)
        assert result["title"] == "No Substack Post"
        assert result["substack"] is False

    def test_draft_substack_flag(self, sample_post_draft):
        result = parse_post(sample_post_draft)
        assert result["substack"] == "draft"


class TestMarkdownToHtml:
    def test_basic_conversion(self):
        html = markdown_to_html("Hello **world**")
        assert "<strong>world</strong>" in html

    def test_resolves_image_urls(self):
        body = '![alt](/images/photo.png)\n\n[link](/docs/file.pdf)'
        html = markdown_to_html(body, site_url="https://www.jtdub.com")
        assert 'src="https://www.jtdub.com/images/photo.png"' in html
        assert 'href="https://www.jtdub.com/docs/file.pdf"' in html

    def test_no_site_url_leaves_relative(self):
        body = "![alt](/images/photo.png)"
        html = markdown_to_html(body, site_url="")
        assert 'src="/images/photo.png"' in html

    def test_fenced_code_blocks(self):
        body = '```python\nprint("hi")\n```'
        html = markdown_to_html(body)
        assert "<code" in html

    def test_tables(self):
        body = "| A | B |\n|---|---|\n| 1 | 2 |"
        html = markdown_to_html(body)
        assert "<table>" in html


@pytest.fixture
def mock_smtp():
    """Mock SMTP server and set required env vars."""
    with patch("scripts.substack.smtplib.SMTP") as mock_smtp_cls:
        mock_server = MagicMock()
        mock_smtp_cls.return_value.__enter__ = MagicMock(return_value=mock_server)
        mock_smtp_cls.return_value.__exit__ = MagicMock(return_value=False)

        env = {
            "SUBSTACK_EMAIL_ADDRESS": "test@substack.com",
            "SMTP_HOST": "smtp.test.com",
            "SMTP_PORT": "587",
            "SMTP_USER": "user@test.com",
            "SMTP_PASSWORD": "secret",
        }
        with patch.dict(os.environ, env):
            yield mock_server


class TestSendToSubstack:
    def test_sends_email(self, mock_smtp):
        result = send_to_substack("My Title", "<p>Hello</p>")

        assert result is True
        mock_smtp.starttls.assert_called_once()
        mock_smtp.login.assert_called_once_with("user@test.com", "secret")
        mock_smtp.send_message.assert_called_once()

        sent_msg = mock_smtp.send_message.call_args[0][0]
        assert sent_msg["Subject"] == "My Title"
        assert sent_msg["To"] == "test@substack.com"

    def test_draft_prefix(self, mock_smtp):
        send_to_substack("My Title", "<p>Hello</p>", is_draft=True)

        sent_msg = mock_smtp.send_message.call_args[0][0]
        assert sent_msg["Subject"] == "[draft] My Title"


class TestCrosspost:
    @patch("scripts.substack.send_to_substack", return_value=True)
    @patch("scripts.substack.get_site_url", return_value="https://www.jtdub.com")
    def test_sends_when_flag_set(self, mock_url, mock_send, sample_post):
        result = crosspost(sample_post)
        assert result is True
        mock_send.assert_called_once()
        assert mock_send.call_args[1]["is_draft"] is False

    @patch("scripts.substack.send_to_substack", return_value=True)
    @patch("scripts.substack.get_site_url", return_value="https://www.jtdub.com")
    def test_skips_without_flag(self, mock_url, mock_send, sample_post_no_substack):
        result = crosspost(sample_post_no_substack)
        assert result is False
        mock_send.assert_not_called()

    @patch("scripts.substack.send_to_substack", return_value=True)
    @patch("scripts.substack.get_site_url", return_value="https://www.jtdub.com")
    def test_force_overrides_missing_flag(
        self, mock_url, mock_send, sample_post_no_substack
    ):
        result = crosspost(sample_post_no_substack, force=True)
        assert result is True
        mock_send.assert_called_once()

    @patch("scripts.substack.send_to_substack", return_value=True)
    @patch("scripts.substack.get_site_url", return_value="https://www.jtdub.com")
    def test_draft_flag_in_frontmatter(self, mock_url, mock_send, sample_post_draft):
        result = crosspost(sample_post_draft)
        assert result is True
        mock_send.assert_called_once()
        assert mock_send.call_args[1]["is_draft"] is True

    @patch("scripts.substack.send_to_substack", return_value=True)
    @patch("scripts.substack.get_site_url", return_value="https://www.jtdub.com")
    def test_draft_param_overrides(self, mock_url, mock_send, sample_post):
        result = crosspost(sample_post, draft=True)
        assert result is True
        assert mock_send.call_args[1]["is_draft"] is True
