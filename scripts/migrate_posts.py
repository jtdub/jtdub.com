"""One-shot migration: Jekyll _posts/*.md → Astro src/content/posts/*.md.

Reads every post, remaps frontmatter to the Astro Zod schema, normalizes
tag casing, drops legacy domain tags, infers zone from tag vocabulary,
and writes to the Astro content collection with a filename slug matching
the Jekyll post's URL slug.

Run from the repo root:
    poetry run python astro-site/scripts/migrate_posts.py
"""

from __future__ import annotations

import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
JEKYLL_POSTS = REPO_ROOT / "_posts"
ASTRO_POSTS = REPO_ROOT / "astro-site" / "src" / "content" / "posts"

FILENAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$")

# Legacy / meta tags that shouldn't carry into the new site.
DROP_TAGS = {
    "packetgeek.net",
    "jtdub.com",
}

# Manual casing overrides for tags that shouldn't just be .title()-ified.
TAG_OVERRIDES = {
    "ios": "IOS",
    "ios-xr": "IOS-XR",
    "ios-xe": "IOS-XE",
    "sdn": "SDN",
    "vlan": "VLAN",
    "vlans": "VLANs",
    "vpn": "VPN",
    "api": "API",
    "apis": "APIs",
    "ai": "AI",
    "llm": "LLM",
    "llms": "LLMs",
    "ccna": "CCNA",
    "ccnp": "CCNP",
    "ccna study notes": "CCNA Study Notes",
    "ccnp sp study notes": "CCNP SP Study Notes",
    "rhce": "RHCE",
    "rhcsa": "RHCSA",
    "rhce study notes": "RHCE Study Notes",
    "selinux": "SELinux",
    "devops": "DevOps",
    "network devops": "Network DevOps",
    "openvswitch": "Open vSwitch",
    "tcp/ip": "TCP/IP",
    "tcpdump": "tcpdump",
    "iptables": "iptables",
    "bgp": "BGP",
    "ospf": "OSPF",
    "eigrp": "EIGRP",
    "mpls": "MPLS",
    "qos": "QoS",
    "nat": "NAT",
    "dhcp": "DHCP",
    "dns": "DNS",
    "ssh": "SSH",
    "tls": "TLS",
    "ssl": "SSL",
    "json": "JSON",
    "xml": "XML",
    "yaml": "YAML",
    "http": "HTTP",
    "https": "HTTPS",
    "ipv4": "IPv4",
    "ipv6": "IPv6",
    "json-rpc": "JSON-RPC",
    "rest": "REST",
    "grpc": "gRPC",
    "sdlc": "SDLC",
    "qoyllur rit'i": "Qoyllur Rit'i",
    "qoyllurriti": "Qoyllur Rit'i",
}

# Tags that indicate the post is a field/research piece.
FIELD_TAGS = {
    # Anthropology / archaeology
    "anthropology", "archaeology", "ethnography", "cultural anthropology",
    "indigenous knowledge", "indigenous", "oral tradition",
    # Places and peoples
    "peru", "cordillera vilcanota", "quechua", "peruvian andes", "andes",
    "andean culture", "ausangate", "sibinacocha", "cusco", "paqchanta",
    "mexico", "baja", "yucatan",
    # Climate / environment / research
    "climate change", "glaciology", "climate policy", "climate",
    "renewable energy", "energy transition", "sustainability", "decarbonization",
    "environmental science", "water quality", "community science",
    "research", "fieldwork", "field research", "field notes",
    # Expedition / outdoors
    "expedition", "exploration", "adventure", "travel", "trail running",
    "ultra running", "running", "mountaineering", "canyoneering",
    "high altitude", "altitude sickness", "ams",
    # Diving
    "scuba diving", "cave diving", "technical diving", "rebreather diving",
    "underwater archaeology", "underwater photography", "diving",
    # Photography / media
    "photography", "aerial photography",
    # Cosmology / religion / history
    "cosmology", "pilgrimage", "qoyllur rit'i", "catholic",
    "history", "pre-columbian", "pre-incan", "incan",
    # Poetry / essays (will be tie-broken by other tags)
    "poetry",
}

# Tags that indicate the post is an engineering/code piece.
ENGINEERING_TAGS = {
    # Languages / runtimes
    "python", "python tips", "perl", "perl tips", "bash", "shell",
    "ruby", "go", "rust", "c", "c++", "javascript", "typescript",
    # OS / platforms
    "linux", "freebsd", "openbsd", "unix", "macos",
    "system administration", "selinux", "kernel",
    # Networking gear / protocols
    "cisco", "juniper", "arista", "ios", "ios-xr", "ios-xe",
    "cisco administration python scripting",
    "bgp", "ospf", "eigrp", "mpls", "vlan", "vlans",
    # Networking practice
    "network programmability", "network devops", "network automation",
    "software defined networking", "sdn", "openvswitch", "openflow",
    "network connectivity", "networking",
    # Certs / study
    "rhce", "rhcsa", "ccna", "ccnp", "rhce study notes",
    "ccnp sp study notes", "certification",
    # Automation / devops
    "ansible", "puppet", "chef", "salt", "terraform", "docker",
    "kubernetes", "devops", "ci/cd", "automation",
    # Security / ops
    "security", "encryption", "firewall", "vpn", "ips/ids",
    "miscellaneous hacking",
    # Programming practice
    "programming", "code review", "test-driven development", "testing",
    "software engineering", "refactoring", "design patterns",
    "sdlc", "agile",
    # AI / ML
    "machine learning", "ai", "claude", "llm", "prompt engineering",
    "transformers", "dataloaders", "ai coding assistants",
    # Data / tools
    "virtualization", "openvswitch", "ovs", "nautobot", "netbox",
    "hierarchical configuration", "hier-config",
}


@dataclass
class MigrationResult:
    written: int = 0
    skipped: int = 0
    field_zone: int = 0
    engineering_zone: int = 0
    tag_counter: Counter = field(default_factory=Counter)
    zone_by_slug: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def normalize_tag(tag: str) -> str | None:
    """Clean up a single tag. Returns None if the tag should be dropped."""
    if not tag:
        return None
    cleaned = tag.strip()
    if not cleaned:
        return None
    lower = cleaned.lower()
    if lower in DROP_TAGS:
        return None
    if lower in TAG_OVERRIDES:
        return TAG_OVERRIDES[lower]
    # Default: title case with small-word handling
    return cleaned.strip().title()


def normalize_tags(raw_tags) -> list[str]:
    """Normalize a tags list, de-duplicating while preserving first-seen order."""
    if not raw_tags:
        return []
    seen: dict[str, None] = {}
    for tag in raw_tags:
        cleaned = normalize_tag(tag)
        if cleaned and cleaned not in seen:
            seen[cleaned] = None
    return list(seen.keys())


def infer_zone(tags: list[str]) -> str:
    """Infer which zone a post belongs to from its normalized tags."""
    lowered = {t.lower() for t in tags}
    field_hit = bool(lowered & FIELD_TAGS)
    eng_hit = bool(lowered & ENGINEERING_TAGS)
    if field_hit and not eng_hit:
        return "field"
    if eng_hit and not field_hit:
        return "engineering"
    if field_hit and eng_hit:
        # Tie-break: field wins — it's the more distinctive category and
        # engineering content is the default baseline.
        return "field"
    # Nothing matched — default to engineering (the larger legacy corpus).
    return "engineering"


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    """Split a markdown file into (frontmatter dict, body string)."""
    if not raw.startswith("---"):
        raise ValueError("missing frontmatter fence")
    end = raw.find("\n---", 3)
    if end == -1:
        raise ValueError("missing frontmatter closing fence")
    fm_raw = raw[3:end].lstrip("\n")
    body = raw[end + 4 :].lstrip("\n")
    data = yaml.safe_load(fm_raw) or {}
    return data, body


def build_astro_frontmatter(data: dict, tags: list[str], zone: str) -> str:
    """Render the new frontmatter block as a YAML string."""
    out: dict = {
        "title": data["title"],
        "date": str(data["date"]),
        "zone": zone,
    }
    if data.get("author"):
        out["author"] = data["author"]
    if tags:
        out["tags"] = tags
    rendered = yaml.safe_dump(
        out,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,
    )
    return f"---\n{rendered}---\n\n"


def migrate() -> MigrationResult:
    if not JEKYLL_POSTS.is_dir():
        sys.exit(f"Expected Jekyll posts at {JEKYLL_POSTS}")
    if ASTRO_POSTS.exists():
        shutil.rmtree(ASTRO_POSTS)
    ASTRO_POSTS.mkdir(parents=True)

    result = MigrationResult()
    for path in sorted(JEKYLL_POSTS.glob("*.md")):
        match = FILENAME_RE.match(path.name)
        if not match:
            result.warnings.append(f"skip (bad filename): {path.name}")
            result.skipped += 1
            continue
        slug = match.group(4)
        try:
            data, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        except Exception as exc:
            result.warnings.append(f"skip (parse error): {path.name}: {exc}")
            result.skipped += 1
            continue

        if "title" not in data or "date" not in data:
            result.warnings.append(f"skip (missing title/date): {path.name}")
            result.skipped += 1
            continue

        tags = normalize_tags(data.get("tags", []))
        zone = infer_zone(tags)
        result.tag_counter.update(tags)
        if zone == "field":
            result.field_zone += 1
        else:
            result.engineering_zone += 1
        result.zone_by_slug[slug] = zone

        new_fm = build_astro_frontmatter(data, tags, zone)
        # Keep the Jekyll filename shape (YYYY-MM-DD-slug.md) so two posts
        # with the same slug on different dates don't collide.
        out_path = ASTRO_POSTS / path.name
        out_path.write_text(new_fm + body, encoding="utf-8")
        result.written += 1

    return result


def report(result: MigrationResult) -> None:
    print(f"Migrated:     {result.written}")
    print(f"Skipped:      {result.skipped}")
    print(f"Field zone:   {result.field_zone}")
    print(f"Engineering:  {result.engineering_zone}")
    print()
    print("Top 25 tags after normalization:")
    for tag, count in result.tag_counter.most_common(25):
        print(f"  {count:>4}  {tag}")
    if result.warnings:
        print()
        print("Warnings:")
        for w in result.warnings:
            print(f"  - {w}")


if __name__ == "__main__":
    report(migrate())
