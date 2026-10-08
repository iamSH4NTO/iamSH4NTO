#!/usr/bin/env python3
"""
gen_profile_assets.py - Generate GitHub profile SVG assets.
Stdlib-only implementation.
"""

import argparse
import datetime
import html
import json
import os
import re
import sys
import urllib.request
import urllib.error
import xml.sax.saxutils

# -------------------------------------------------------------------------
# Config block
# -------------------------------------------------------------------------
LOGIN   = "iamSH4NTO"
NAME    = "MD ZAHIRUL ISLAM"
HANDLE  = "@iamSH4NTO"
TAGLINE = "Senior Software Engineer · production mobile & web products"
CHIPS   = ["Go", "Node.js", "Next.js", "Vue", "TypeScript",
           "React Native (Expo)", "Cloudflare Workers + D1", "MySQL"]
PILL    = ("Live on Google Play", "https://play.google.com/store/apps/details?id=com.skf.duty")
LANG_COLORS = {"TypeScript": "#3178C6", "JavaScript": "#F1E05A", "Python": "#3572A5",
               "Vue": "#41B883", "Go": "#00ADD8", "HTML": "#E34C26", "CSS": "#563D7C",
               "PHP": "#4F5D95", "Dart": "#00B4AB", "Shell": "#89E051"}
PINNED = [
    {"repo": None, "title": "SKF Duty Calculator", "monogram": "SK", "badge": "LIVE",
     "grad": ("#8250df", "#c297ff"),
     "desc": "Employee shift, overtime and leave tracking app, live in production on Google Play.",
     "lang": "TypeScript", "url": "https://play.google.com/store/apps/details?id=com.skf.duty"},
    {"repo": "BloodDonation", "title": "BloodDonation", "monogram": "BD",
     "grad": ("#ec4899", "#f9a8d4"),
     "desc": "Open-source blood donation platform.",
     "lang": "Vue", "url": "https://github.com/iamSH4NTO/BloodDonation"},
    {"repo": "CircleNetwork", "title": "CircleNetwork", "monogram": "CN",
     "grad": ("#3b82f6", "#93c5fd"),
     "desc": "Full-featured Expo React Native app with WebViews.",
     "lang": "TypeScript", "url": "https://github.com/iamSH4NTO/CircleNetwork"},
]

# -------------------------------------------------------------------------
# Design tokens
# -------------------------------------------------------------------------
PAGE        = "#0d1117"
CARD        = "#161b22"
CARD2       = "#1c2128"
BORDER      = "#21262d"
BORDER2     = "#30363d"
TEXT        = "#e6edf3"
MUTED       = "#8b949e"
DIM         = "#6e7681"
ACCENT      = "#a371f7"
ACCENT2     = "#8250df"
ACCENT_SOFT = "#c297ff"
PINK        = "#ec4899"
BLUE        = "#3b82f6"
GREEN       = "#10b981"

# Octicons (16x16)
OCTICON_REPO = "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"
OCTICON_STAR = "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"
OCTICON_PERSON = "M10.561 8.073a6.005 6.005 0 0 1 3.432 5.142.75.75 0 1 1-1.498.07 4.5 4.5 0 0 0-8.99 0 .75.75 0 0 1-1.498-.07 6.004 6.004 0 0 1 3.431-5.142 3.999 3.999 0 1 1 5.123 0ZM10.5 5a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0Z"
OCTICON_PEOPLE = "M2 5.5a3.5 3.5 0 1 1 5.898 2.549 5.508 5.508 0 0 1 3.034 4.084.75.75 0 1 1-1.482.235 4 4 0 0 0-7.9 0 .75.75 0 0 1-1.482-.236A5.507 5.507 0 0 1 3.102 8.05 3.493 3.493 0 0 1 2 5.5ZM11 4a3.001 3.001 0 0 1 2.22 5.018 5.01 5.01 0 0 1 2.56 3.012.749.749 0 0 1-.885.954.752.752 0 0 1-.549-.514 3.507 3.507 0 0 0-2.522-2.372.75.75 0 0 1-.574-.73v-.352a.75.75 0 0 1 .416-.672A1.5 1.5 0 0 0 11 5.5.75.75 0 0 1 11 4Zm-5.5-.5a2 2 0 1 0-.001 3.999A2 2 0 0 0 5.5 3.5Z"
OCTICON_FORK = "M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"

FONT_STACK = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

# -------------------------------------------------------------------------
# Typography and layout helpers
# -------------------------------------------------------------------------
def _char_units(ch, bold=False):
    """Return width in 1/1000 em units."""
    if ch in "ijl|'":
        w = 260
    elif ch in "!.,:;":
        w = 280
    elif ch in "frtI":
        w = 360
    elif ch in " ":
        w = 300
    elif ch in "-–—":
        w = 380
    elif ch in "abcdeghknopqsuvxyz":
        w = 550
    elif ch in "mw":
        w = 800
    elif ch in "MW":
        w = 880
    elif ch in "OQGD":
        w = 750
    elif ch in "ABCDEFHJKLNPQRSTUVXYZ":
        w = 680
    elif ch.isdigit():
        w = 560
    else:
        w = 600
    if bold:
        w = int(w * 1.08)
    return w

def text_width(s, size, weight=400):
    """Estimate advance width using system font metrics."""
    if not s:
        return 0.0
    is_bold = weight >= 600 if isinstance(weight, (int, float)) else str(weight).lower() in ("bold", "700", "800", "600")
    total_units = sum(_char_units(ch, is_bold) for ch in s)
    return total_units * (size / 1000.0)

def truncate_to_width(s, size, weight, max_w, ellipsis="…"):
    """Truncate text to fit within max_w with an ellipsis."""
    if not s or text_width(s, size, weight) <= max_w:
        return s
    ell_w = text_width(ellipsis, size, weight)
    if ell_w > max_w:
        return ""
    cur = s
    while cur and (text_width(cur, size, weight) + ell_w) > max_w:
        cur = cur[:-1]
    return cur.rstrip() + ellipsis

def wrap_to_width(s, size, weight, max_w, max_lines):
    """Wrap text to fit within max_w over at most max_lines."""
    if not s:
        return []
    words = s.split()
    if not words:
        return []
    lines = []
    curr_line = ""
    for idx, w in enumerate(words):
        test_line = f"{curr_line} {w}".strip() if curr_line else w
        if text_width(test_line, size, weight) <= max_w:
            curr_line = test_line
        else:
            if len(lines) == max_lines - 1:
                # Last allowed line: back up whole words if needed to fit ellipsis
                if curr_line:
                    while curr_line and text_width(curr_line + "…", size, weight) > max_w:
                        curr_line = curr_line.rsplit(" ", 1)[0] if " " in curr_line else curr_line[:-1]
                    lines.append((curr_line + "…") if curr_line else "…")
                else:
                    lines.append(truncate_to_width(w, size, weight, max_w))
                return lines
            else:
                if curr_line:
                    lines.append(curr_line)
                    curr_line = w
                else:
                    lines.append(w)
                    curr_line = ""
    if curr_line and len(lines) < max_lines:
        lines.append(curr_line)
    return lines[:max_lines]

def fmt_compact(n):
    """Format integers compactly: 999 / 1.2k / 26k."""
    try:
        val = int(n)
    except (ValueError, TypeError):
        return str(n)
    if val < 1000:
        return str(val)
    if val < 10000:
        formatted = f"{val / 1000:.1f}k"
        return formatted.replace(".0k", "k")
    return f"{round(val / 1000)}k"

def xml_escape(s):
    return xml.sax.saxutils.escape(str(s))

# -------------------------------------------------------------------------
# Default baked-in fallback snapshot
# -------------------------------------------------------------------------
FALLBACK_SNAPSHOT = {
    "login": LOGIN,
    "name": NAME,
    "public_repos": 9,
    "total_stars": 0,
    "followers": 1,
    "following": 1,
    "pinned": [
        {"title": "SKF Duty Calculator", "monogram": "SK", "badge": "LIVE",
         "grad": ("#8250df", "#c297ff"),
         "desc": "Employee shift, overtime and leave tracking app, live in production on Google Play.",
         "lang": "TypeScript", "stars": 0, "forks": 0},
        {"title": "BloodDonation", "monogram": "BD", "badge": None,
         "grad": ("#ec4899", "#f9a8d4"),
         "desc": "Open-source blood donation platform.",
         "lang": "Vue", "stars": 0, "forks": 0},
        {"title": "CircleNetwork", "monogram": "CN", "badge": None,
         "grad": ("#3b82f6", "#93c5fd"),
         "desc": "Full-featured Expo React Native app with WebViews.",
         "lang": "TypeScript", "stars": 0, "forks": 0},
    ],
    "contributions": {
        "total": 2871,
        "weeks": []  # Generated procedurally if missing
    }
}

# -------------------------------------------------------------------------
# Data fetchers
# -------------------------------------------------------------------------
def make_headers(token=None):
    h = {"User-Agent": "ProfileAssetGenerator/1.0 (iamSH4NTO profile tool)"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def fetch_json(url, token=None, post_data=None):
    headers = make_headers(token)
    if post_data is not None:
        headers["Content-Type"] = "application/json"
        data_bytes = json.dumps(post_data).encode("utf-8")
    else:
        data_bytes = None
    req = urllib.request.Request(url, data=data_bytes, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fetch_api_data(login, token):
    """Fetch user stats, repos, pinned repos, and contributions via REST + GraphQL."""
    user_url = f"https://api.github.com/users/{login}"
    user_data = fetch_json(user_url, token)
    public_repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    following = user_data.get("following", 0)
    name = user_data.get("name") or NAME

    # Fetch owner repos to sum stars
    repos_url = f"https://api.github.com/users/{login}/repos?per_page=100&type=owner"
    repos_data = fetch_json(repos_url, token)
    total_stars = sum(r.get("stargazers_count", 0) for r in repos_data)

    # Pinned repos live info
    pinned_list = []
    for p in PINNED:
        item = {
            "title": p["title"],
            "monogram": p["monogram"],
            "badge": p.get("badge"),
            "grad": p["grad"],
            "desc": p["desc"],
            "lang": p["lang"],
            "stars": 0,
            "forks": 0,
        }
        repo_name = p.get("repo")
        if repo_name:
            try:
                r_info = fetch_json(f"https://api.github.com/repos/{login}/{repo_name}", token)
                if r_info.get("language"):
                    item["lang"] = r_info["language"]
                item["stars"] = r_info.get("stargazers_count", 0)
                item["forks"] = r_info.get("forks_count", 0)
                if r_info.get("description"):
                    item["desc"] = r_info["description"]
            except Exception:
                pass
        pinned_list.append(item)

    # GraphQL contributions
    gql_url = "https://api.github.com/graphql"
    gql_query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                contributionLevel
                date
                weekday
              }
            }
          }
        }
      }
    }
    """
    gql_res = fetch_json(gql_url, token, {"query": gql_query, "variables": {"login": login}})
    cal = gql_res["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    total_contribs = cal.get("totalContributions", 0)
    raw_weeks = cal.get("weeks", [])

    level_map = {
        "NONE": 0,
        "FIRST_QUARTILE": 1,
        "SECOND_QUARTILE": 2,
        "THIRD_QUARTILE": 3,
        "FOURTH_QUARTILE": 4,
    }

    weeks = []
    for w in raw_weeks:
        days = []
        for d in w.get("contributionDays", []):
            lvl = level_map.get(d.get("contributionLevel"), 0)
            days.append({
                "date": d.get("date"),
                "level": lvl,
                "count": d.get("contributionCount", 0),
                "weekday": d.get("weekday", 0),
            })
        weeks.append(days)

    return {
        "login": login,
        "name": name,
        "public_repos": public_repos,
        "total_stars": total_stars,
        "followers": followers,
        "following": following,
        "pinned": pinned_list,
        "contributions": {
            "total": total_contribs,
            "weeks": weeks
        }
    }

def fetch_html_data(login):
    """Scrape public contributions page and public REST."""
    headers = make_headers()
    # REST user
    req = urllib.request.Request(f"https://api.github.com/users/{login}", headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        user_data = json.loads(resp.read().decode("utf-8"))
    public_repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    following = user_data.get("following", 0)
    name = user_data.get("name") or NAME

    # REST repos
    req = urllib.request.Request(f"https://api.github.com/users/{login}/repos?per_page=100&type=owner", headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        repos_data = json.loads(resp.read().decode("utf-8"))
    total_stars = sum(r.get("stargazers_count", 0) for r in repos_data)

    # Scrape contributions
    contrib_req = urllib.request.Request(f"https://github.com/users/{login}/contributions", headers=headers)
    with urllib.request.urlopen(contrib_req, timeout=15) as resp:
        html_text = resp.read().decode("utf-8")

    # Match total
    total_match = re.search(r"([0-9,]+)\s+contributions", html_text)
    total_contribs = int(total_match.group(1).replace(",", "")) if total_match else 0

    # Match days
    raw_cells = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d+)"', html_text)
    if not raw_cells:
        raw_cells = re.findall(r'data-level="(\d+)"[^>]*data-date="(\d{4}-\d{2}-\d{2})"', html_text)
        raw_cells = [(d, lvl) for lvl, d in raw_cells]

    # Organize days into 53 weeks
    date_dict = {d: int(lvl) for d, lvl in raw_cells}
    all_dates = sorted(date_dict.keys())

    weeks = []
    if all_dates:
        # Group into columns
        # Each column in GitHub contributions is a Sunday-Saturday week
        # Build 53 columns
        last_date = datetime.date.fromisoformat(all_dates[-1])
        # Find ending Sunday or current date
        start_date = last_date - datetime.timedelta(days=53*7 - 1)
        # Adjust start_date to Sunday
        # Python weekday: Mon=0, Sun=6. Days since Sunday = (start_date.weekday() + 1) % 7
        sun_offset = (start_date.weekday() + 1) % 7
        start_sunday = start_date - datetime.timedelta(days=sun_offset)

        cur = start_sunday
        for w_idx in range(53):
            week_days = []
            for d_idx in range(7):
                cur_str = cur.strftime("%Y-%m-%d")
                lvl = date_dict.get(cur_str, 0)
                week_days.append({
                    "date": cur_str,
                    "level": lvl,
                    "count": 0,
                    "weekday": d_idx
                })
                cur += datetime.timedelta(days=1)
            weeks.append(week_days)

    pinned_list = []
    for p in PINNED:
        item = {
            "title": p["title"],
            "monogram": p["monogram"],
            "badge": p.get("badge"),
            "grad": p["grad"],
            "desc": p["desc"],
            "lang": p["lang"],
            "stars": 0,
            "forks": 0,
        }
        pinned_list.append(item)

    return {
        "login": login,
        "name": name,
        "public_repos": public_repos,
        "total_stars": total_stars,
        "followers": followers,
        "following": following,
        "pinned": pinned_list,
        "contributions": {
            "total": total_contribs,
            "weeks": weeks
        }
    }

def build_procedural_weeks(total):
    """Build 53 fallback weeks ending today."""
    today = datetime.datetime.now(datetime.timezone.utc).date()
    # 53 weeks * 7 days
    # Align so that week 52 ends on today
    today_weekday = (today.weekday() + 1) % 7  # Sun=0, ..., Sat=6
    # Last week's Sunday
    last_sunday = today - datetime.timedelta(days=today_weekday)
    first_sunday = last_sunday - datetime.timedelta(weeks=52)

    weeks = []
    cur = first_sunday
    for w in range(53):
        days = []
        for d in range(7):
            if cur <= today:
                # Mock distribution
                seed = (cur.year * 1000 + cur.timetuple().tm_yday)
                lvl = (seed % 5) if total > 0 else 0
                days.append({"date": cur.strftime("%Y-%m-%d"), "level": lvl, "count": lvl * 2, "weekday": d})
            cur += datetime.timedelta(days=1)
        weeks.append(days)
    return weeks

def ensure_weeks_structure(data):
    """Ensure data['contributions']['weeks'] has 53 weeks."""
    contribs = data.get("contributions", {})
    weeks = contribs.get("weeks", [])
    if len(weeks) != 53 or not any(weeks):
        weeks = build_procedural_weeks(contribs.get("total", 2871))
        data["contributions"]["weeks"] = weeks
    return data

# -------------------------------------------------------------------------
# SVG Renderers
# -------------------------------------------------------------------------
def render_header_svg(data):
    w, h = 880, 200
    name = xml_escape(data.get("name") or NAME)
    handle = xml_escape(HANDLE)
    tagline = xml_escape(TAGLINE)
    pill_text = xml_escape(PILL[0])

    # Pill sizing & positioning
    # Pill right edge x=836, height=34, y=52, rx=17
    # Circle glyph: r=3.5, gap 7, text 13px weight 700
    tw = text_width(PILL[0], 13, 700)
    inner_w = 7 + 8 + tw
    pill_pad = 18
    pill_w = int(inner_w + pill_pad * 2)
    pill_x = 836 - pill_w
    circle_cx = pill_x + pill_pad + 3.5
    circle_cy = 52 + 17
    pill_text_x = circle_cx + 3.5 + 8
    pill_text_y = 52 + 21.5

    # Chip layout
    # Row 1: y=146, height=30, rx=15, left=44, gaps=10, right edge <= 836
    chips_svg = []
    cur_x = 44
    cur_y = 146
    for chip in CHIPS:
        ctw = text_width(chip, 12.5, 500)
        chip_w = int(ctw + 22)
        if cur_x + chip_w > 836:
            cur_x = 44
            cur_y = 182
        chips_svg.append(
            f'    <rect x="{cur_x}" y="{cur_y}" width="{chip_w}" height="30" rx="15" fill="{CARD2}" stroke="{BORDER2}"/>\n'
            f'    <text x="{cur_x + chip_w / 2:.1f}" y="{cur_y + 19.5:.1f}" text-anchor="middle" font-family="{FONT_STACK}" font-size="12.5" font-weight="500" fill="{MUTED}">{xml_escape(chip)}</text>'
        )
        cur_x += chip_w + 10

    chips_markup = "\n".join(chips_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
  <title>Header - {name}</title>
  <defs>
    <linearGradient id="header-glow" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="pill-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{ACCENT2}"/>
      <stop offset="100%" stop-color="{ACCENT}"/>
    </linearGradient>
    <clipPath id="card-clip">
      <rect width="{w}" height="{h}" rx="16"/>
    </clipPath>
  </defs>

  <rect width="{w}" height="{h}" fill="{PAGE}"/>
  <rect width="{w}" height="{h}" rx="16" fill="{CARD}" stroke="{BORDER}"/>

  <g clip-path="url(#card-clip)">
    <rect width="{w}" height="100" fill="url(#header-glow)"/>
  </g>

  <!-- Name -->
  <text x="44" y="80" font-family="{FONT_STACK}" font-size="32" font-weight="800" fill="{TEXT}" letter-spacing="-0.5">{name}</text>

  <!-- Violet Pill -->
  <rect x="{pill_x}" y="52" width="{pill_w}" height="34" rx="17" fill="url(#pill-grad)"/>
  <circle cx="{circle_cx:.1f}" cy="{circle_cy:.1f}" r="3.5" fill="#ffffff"/>
  <text x="{pill_text_x:.1f}" y="{pill_text_y:.1f}" font-family="{FONT_STACK}" font-size="13" font-weight="700" fill="#ffffff">{pill_text}</text>

  <!-- Handle & Tagline -->
  <text x="44" y="108" font-family="{FONT_STACK}">
    <tspan font-size="15" font-weight="600" fill="{ACCENT}">{handle}</tspan>
    <tspan font-size="15" font-weight="400" fill="{MUTED}">  ·  {tagline}</tspan>
  </text>

  <!-- Divider -->
  <line x1="44" y1="128" x2="836" y2="128" stroke="{BORDER}"/>

  <!-- Chips -->
{chips_markup}
</svg>
"""
    return svg

def render_stats_svg(data):
    w, h = 880, 100
    cards_cfg = [
        {"label": "Repositories", "val": data.get("public_repos", 0), "color": ACCENT2, "icon": OCTICON_REPO},
        {"label": "Stars", "val": data.get("total_stars", 0), "color": PINK, "icon": OCTICON_STAR},
        {"label": "Followers", "val": data.get("followers", 0), "color": BLUE, "icon": OCTICON_PERSON},
        {"label": "Following", "val": data.get("following", 0), "color": GREEN, "icon": OCTICON_PEOPLE},
    ]

    card_w = 208
    card_h = 92
    card_y = 4
    xs = [0, 224, 448, 672]

    cards_markup = []
    for i, cfg in enumerate(cards_cfg):
        cx = xs[i]
        val_str = fmt_compact(cfg["val"])
        tile_x = cx + 18
        tile_y = card_y + 24
        icon_tx = tile_x + 11
        icon_ty = tile_y + 11
        cards_markup.append(f"""  <!-- Stat: {cfg['label']} -->
  <rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" rx="14" fill="{CARD}" stroke="{BORDER}"/>
  <rect x="{tile_x}" y="{tile_y}" width="44" height="44" rx="13" fill="{cfg['color']}"/>
  <g transform="translate({icon_tx} {icon_ty}) scale(1.375)" fill="#ffffff">
    <path d="{cfg['icon']}"/>
  </g>
  <text x="{cx + 76}" y="{card_y + 42}" font-family="{FONT_STACK}" font-size="14.5" font-weight="500" fill="{MUTED}">{cfg['label']}</text>
  <text x="{cx + 76}" y="{card_y + 76}" font-family="{FONT_STACK}" font-size="26" font-weight="700" fill="{TEXT}">{val_str}</text>""")

    joined_cards = "\n".join(cards_markup)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
  <title>GitHub Statistics</title>
  <rect width="{w}" height="{h}" fill="{PAGE}"/>
{joined_cards}
</svg>
"""
    return svg

def render_repos_svg(data):
    w, h = 880, 240
    pinned_list = data.get("pinned", FALLBACK_SNAPSHOT["pinned"])

    # Gradients for pinned thumbnails
    defs_markup = []
    for i, p in enumerate(pinned_list[:3]):
        g0, g1 = p.get("grad", (ACCENT2, ACCENT_SOFT))
        defs_markup.append(f"""    <linearGradient id="repo-grad-{i}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{g0}"/>
      <stop offset="100%" stop-color="{g1}"/>
    </linearGradient>""")

    # 3 repo cards: width=266, gap=17, x = 24, 307, 590, y=44, height=184
    xs = [24, 307, 590]
    card_w = 266
    card_h = 184
    card_y = 44

    cards_markup = []
    for i, p in enumerate(pinned_list[:3]):
        cx = xs[i]
        title = p.get("title", "Repository")
        title_disp = truncate_to_width(title, 14.5, 700, 150)

        # Monogram
        mono = p.get("monogram", title[:2].upper())
        badge = p.get("badge")

        badge_markup = ""
        if badge:
            # Badge pinned to thumbnail bottom-left
            # Thumbnail is at (cx + 16, card_y + 16) = (cx + 16, 60), size 84x84
            # Bottom edge of thumbnail is y = 144
            bw = int(text_width(badge, 8.5, 700) + 12)
            badge_markup = f"""      <rect x="{cx + 20}" y="126" width="{bw}" height="16" rx="4" fill="{GREEN}"/>
      <text x="{cx + 20 + bw/2:.1f}" y="137.5" text-anchor="middle" font-family="{FONT_STACK}" font-size="8.5" font-weight="700" fill="#ffffff">{xml_escape(badge)}</text>"""

        # Description wrapped to max 3 lines (baselines: card_y+52=96, card_y+69=113, card_y+86=130)
        desc = p.get("desc", "")
        desc_lines = wrap_to_width(desc, 11.5, 400, 138, max_lines=3)
        desc_markup = []
        for line_idx, line in enumerate(desc_lines):
            line_y = 96 + line_idx * 17
            desc_markup.append(f'      <text x="{cx + 112}" y="{line_y}" font-family="{FONT_STACK}" font-size="11.5" font-weight="400" fill="{MUTED}">{xml_escape(line)}</text>')
        desc_xml = "\n".join(desc_markup)

        # Footer baseline card_y + 160 = 204
        # Items: language dot + name, stars octicon + count, forks octicon + count
        lang = p.get("lang", "Code")
        lang_color = LANG_COLORS.get(lang, MUTED)
        stars_str = fmt_compact(p.get("stars", 0))
        forks_str = fmt_compact(p.get("forks", 0))

        # Measure widths
        lang_name_w = text_width(lang, 11, 400)
        lang_item_w = 12 + lang_name_w
        stars_item_w = 14 + text_width(stars_str, 11, 400)
        forks_item_w = 14 + text_width(forks_str, 11, 400)

        # Maximum width available is 138px (cx+112 to cx+250)
        total_items_w = lang_item_w + stars_item_w + forks_item_w
        avail_w = 138.0
        gap = 14.0
        if total_items_w + gap * 2 > avail_w:
            # shrink gap or truncate lang
            gap = max(6.0, (avail_w - total_items_w) / 2.0)
            if total_items_w + gap * 2 > avail_w:
                # truncate lang
                max_lang_name_w = avail_w - gap * 2 - stars_item_w - forks_item_w - 12
                lang = truncate_to_width(lang, 11, 400, max_lang_name_w)
                lang_name_w = text_width(lang, 11, 400)
                lang_item_w = 12 + lang_name_w

        fx1 = cx + 112
        fx2 = fx1 + lang_item_w + gap
        fx3 = fx2 + stars_item_w + gap

        footer_markup = f"""      <!-- Footer: Language, Stars, Forks -->
      <circle cx="{fx1 + 4:.1f}" cy="200.5" r="4" fill="{lang_color}"/>
      <text x="{fx1 + 12:.1f}" y="204" font-family="{FONT_STACK}" font-size="11" font-weight="400" fill="{MUTED}">{xml_escape(lang)}</text>

      <g transform="translate({fx2:.1f} 193.5) scale(0.75)" fill="{MUTED}">
        <path d="{OCTICON_STAR}"/>
      </g>
      <text x="{fx2 + 15:.1f}" y="204" font-family="{FONT_STACK}" font-size="11" font-weight="400" fill="{MUTED}">{stars_str}</text>

      <g transform="translate({fx3:.1f} 193.5) scale(0.75)" fill="{MUTED}">
        <path d="{OCTICON_FORK}"/>
      </g>
      <text x="{fx3 + 15:.1f}" y="204" font-family="{FONT_STACK}" font-size="11" font-weight="400" fill="{MUTED}">{forks_str}</text>"""

        cards_markup.append(f"""    <!-- Repo card {i+1}: {title} -->
    <rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" rx="14" fill="{PAGE}" stroke="{BORDER2}"/>

    <!-- Thumbnail -->
    <rect x="{cx + 16}" y="60" width="84" height="84" rx="10" fill="url(#repo-grad-{i})"/>
    <text x="{cx + 58}" y="113" text-anchor="middle" font-family="{FONT_STACK}" font-size="34" font-weight="800" fill="#ffffff" fill-opacity="0.92">{xml_escape(mono)}</text>
{badge_markup}

    <!-- Title -->
    <text x="{cx + 112}" y="74" font-family="{FONT_STACK}" font-size="14.5" font-weight="700" fill="{TEXT}">{xml_escape(title_disp)}</text>

    <!-- Description -->
{desc_xml}

{footer_markup}""")

    joined_defs = "\n".join(defs_markup)
    joined_cards = "\n".join(cards_markup)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
  <title>Pinned Repositories</title>
  <defs>
{joined_defs}
  </defs>

  <rect width="{w}" height="{h}" fill="{PAGE}"/>
  <rect width="{w}" height="{h}" rx="16" fill="{CARD}" stroke="{BORDER}"/>

  <!-- Heading -->
  <g transform="translate(24 13) scale(1.0)" fill="{TEXT}">
    <path d="{OCTICON_REPO}"/>
  </g>
  <text x="48" y="26" font-family="{FONT_STACK}" font-size="16" font-weight="600" fill="{TEXT}">Pinned Repository</text>

  <!-- Circular chevron buttons -->
  <circle cx="816" cy="20" r="12" fill="{CARD2}" stroke="{BORDER2}"/>
  <path d="M818 16 L814 20 L818 24" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="844" cy="20" r="12" fill="{CARD2}" stroke="{BORDER2}"/>
  <path d="M842 16 L846 20 L842 24" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Pinned Cards -->
{joined_cards}
</svg>
"""
    return svg

def render_contributions_svg(data):
    w, h = 880, 196
    contribs = data.get("contributions", {})
    total = contribs.get("total", 0)
    weeks = contribs.get("weeks", [])

    today_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    # Colors
    LEVEL_COLORS = {
        0: "#1b1f27",
        1: "#4c3a7a",
        2: "#6b4bb5",
        3: "#8b5cf6",
        4: "#c4a7fb",
    }

    # Grid parameters
    # 53 columns x 7 rows
    # Cell 11x11, rx 2.5, horizontal pitch 15, vertical pitch 15
    # Total grid width = 52 * 15 + 11 = 791px
    # Ends at x = 856 -> starts at x = 856 - 791 = 65
    grid_x = 65
    grid_y = 56

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_labels = []
    last_month = None
    last_label_x = -100

    # Grid cells
    cells_markup = []
    for w_idx in range(min(53, len(weeks))):
        col_days = weeks[w_idx]
        col_x = grid_x + w_idx * 15

        # Check for month label at the first day of each month
        for day_info in col_days:
            date_str = day_info.get("date")
            if date_str:
                parts = date_str.split("-")
                if len(parts) == 3:
                    m_idx = int(parts[1]) - 1
                    if m_idx != last_month:
                        # Place month label if spacing allows
                        if col_x - last_label_x >= 28 and col_x <= 830:
                            month_labels.append((col_x, month_names[m_idx]))
                            last_label_x = col_x
                        last_month = m_idx

        # Render 7 day cells
        for day_info in col_days:
            weekday = day_info.get("weekday", 0)
            if weekday < 0 or weekday > 6:
                continue
            cell_y = grid_y + weekday * 15
            lvl = day_info.get("level", 0)
            lvl_clamped = max(0, min(4, lvl))
            fill_color = LEVEL_COLORS[lvl_clamped]
            stroke_attr = f' stroke="{BORDER}"' if lvl_clamped == 0 else ""
            cells_markup.append(
                f'    <rect x="{col_x}" y="{cell_y}" width="11" height="11" rx="2.5" fill="{fill_color}"{stroke_attr}/>'
            )

    cells_str = "\n".join(cells_markup)

    # Month text markup
    months_str = "\n".join(
        f'    <text x="{mx}" y="47" font-family="{FONT_STACK}" font-size="10.5" font-weight="400" fill="{DIM}">{mname}</text>'
        for mx, mname in month_labels
    )

    # Legend at bottom right: Less + 5 swatches + More
    # Ending at x = 856, y = 171
    legend_markup = f"""  <!-- Legend -->
  <text x="743" y="180" text-anchor="end" font-family="{FONT_STACK}" font-size="10.5" font-weight="400" fill="{DIM}">Less</text>
  <rect x="751" y="171" width="11" height="11" rx="2.5" fill="{LEVEL_COLORS[0]}" stroke="{BORDER}"/>
  <rect x="766" y="171" width="11" height="11" rx="2.5" fill="{LEVEL_COLORS[1]}"/>
  <rect x="781" y="171" width="11" height="11" rx="2.5" fill="{LEVEL_COLORS[2]}"/>
  <rect x="796" y="171" width="11" height="11" rx="2.5" fill="{LEVEL_COLORS[3]}"/>
  <rect x="811" y="171" width="11" height="11" rx="2.5" fill="{LEVEL_COLORS[4]}"/>
  <text x="856" y="180" text-anchor="end" font-family="{FONT_STACK}" font-size="10.5" font-weight="400" fill="{DIM}">More</text>"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
  <title>Contribution Activity</title>
  <rect width="{w}" height="{h}" fill="{PAGE}"/>
  <rect width="{w}" height="{h}" rx="16" fill="{CARD}" stroke="{BORDER}"/>

  <!-- Heading -->
  <text x="24" y="30" font-family="{FONT_STACK}" font-size="16" font-weight="600" fill="{TEXT}">{total:,} contributions in this year</text>
  <text x="856" y="30" text-anchor="end" font-family="{FONT_STACK}" font-size="12" font-weight="400" fill="{DIM}">Updated {today_utc}</text>

  <!-- Weekday Labels -->
  <text x="36" y="80" font-family="{FONT_STACK}" font-size="10" font-weight="400" fill="{DIM}">Mon</text>
  <text x="36" y="110" font-family="{FONT_STACK}" font-size="10" font-weight="400" fill="{DIM}">Wed</text>
  <text x="36" y="140" font-family="{FONT_STACK}" font-size="10" font-weight="400" fill="{DIM}">Fri</text>

  <!-- Month Labels -->
{months_str}

  <!-- Grid Cells -->
{cells_str}

{legend_markup}
</svg>
"""
    return svg

# -------------------------------------------------------------------------
# CLI & Pipeline
# -------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate GitHub profile SVG assets.")
    parser.add_argument("--out", default="assets", help="Output directory (default: assets)")
    parser.add_argument("--login", default=None, help=f"GitHub login (default: GITHUB_LOGIN or {LOGIN})")
    parser.add_argument("--source", choices=["auto", "api", "html", "fixture"], default="auto", help="Data source")
    parser.add_argument("--fixture", default=None, help="Path to fixture JSON file")
    parser.add_argument("--print-report", action="store_true", help="Print report of numbers used")

    args = parser.parse_args()

    login = args.login or os.environ.get("GITHUB_LOGIN") or LOGIN
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    data = None

    # Source resolution
    if args.fixture:
        try:
            with open(args.fixture, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load fixture file {args.fixture}: {e}", file=sys.stderr)

    if data is None:
        if args.source == "fixture":
            data = dict(FALLBACK_SNAPSHOT)
        elif args.source == "api":
            try:
                data = fetch_api_data(login, token)
            except Exception as e:
                print(f"Warning: API fetch failed: {e}. Falling back to default snapshot.", file=sys.stderr)
                data = dict(FALLBACK_SNAPSHOT)
        elif args.source == "html":
            try:
                data = fetch_html_data(login)
            except Exception as e:
                print(f"Warning: HTML scrape failed: {e}. Falling back to default snapshot.", file=sys.stderr)
                data = dict(FALLBACK_SNAPSHOT)
        elif args.source == "auto":
            # Try API first if token present, or HTML
            if token:
                try:
                    data = fetch_api_data(login, token)
                except Exception as e:
                    print(f"Warning: Authenticated API fetch failed: {e}. Trying HTML scraper...", file=sys.stderr)
            if data is None:
                try:
                    data = fetch_html_data(login)
                except Exception as e:
                    print(f"Warning: HTML scraper failed: {e}. Falling back to default snapshot.", file=sys.stderr)
                    data = dict(FALLBACK_SNAPSHOT)

    if data is None:
        data = dict(FALLBACK_SNAPSHOT)

    data = ensure_weeks_structure(data)

    # Output directory
    try:
        os.makedirs(args.out, exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory {args.out}: {e}", file=sys.stderr)
        sys.exit(1)

    # Render SVGs
    header_svg = render_header_svg(data)
    stats_svg = render_stats_svg(data)
    repos_svg = render_repos_svg(data)
    contribs_svg = render_contributions_svg(data)

    # Write files
    header_path = os.path.join(args.out, "header.svg")
    stats_path = os.path.join(args.out, "stats.svg")
    repos_path = os.path.join(args.out, "repos.svg")
    contribs_path = os.path.join(args.out, "contributions.svg")

    with open(header_path, "w", encoding="utf-8") as f:
        f.write(header_svg)
    with open(stats_path, "w", encoding="utf-8") as f:
        f.write(stats_svg)
    with open(repos_path, "w", encoding="utf-8") as f:
        f.write(repos_svg)
    with open(contribs_path, "w", encoding="utf-8") as f:
        f.write(contribs_svg)

    # Report
    if args.print_report:
        c_total = data.get("contributions", {}).get("total", 0)
        p_repos = data.get("public_repos", 0)
        stars = data.get("total_stars", 0)
        followers = data.get("followers", 0)
        following = data.get("following", 0)
        print("=" * 60)
        print("PROFILE ASSET GENERATOR REPORT")
        print("=" * 60)
        print(f"User:           {data.get('login', login)} ({data.get('name', NAME)})")
        print(f"Repositories:   {p_repos}")
        print(f"Total Stars:    {stars}")
        print(f"Followers:      {followers}")
        print(f"Following:      {following}")
        print(f"Contributions:  {c_total:,}")
        print("Pinned Repositories:")
        for idx, pr in enumerate(data.get("pinned", []), 1):
            print(f"  {idx}. {pr.get('title')} ({pr.get('lang')}) - Stars: {pr.get('stars', 0)}, Forks: {pr.get('forks', 0)}")
        print("=" * 60)

if __name__ == "__main__":
    main()
