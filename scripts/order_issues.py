"""
Script to add execution order numbers to GitHub issue titles within each milestone.

For each milestone, issues are sorted by issue number (creation order) and their
titles are updated to include "[N/Total] " as a prefix after the project tag.

Example:
  Before: "P01 - Definir escopo e comandos do CLI"
  After:  "P01 - [01/12] Definir escopo e comandos do CLI"

Usage:
  GITHUB_TOKEN=<token> GITHUB_REPOSITORY=owner/repo python scripts/order_issues.py
"""

import os
import re
import sys
import time
import urllib.request
import urllib.error
import json


def github_request(method, path, data=None):
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        print("Error: GITHUB_TOKEN and GITHUB_REPOSITORY must be set.")
        sys.exit(1)

    url = f"https://api.github.com/repos/{repo}{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode(errors="replace")
        print(f"GitHub API error {exc.code} on {method} {url}: {error_body}")
        raise


def get_all_issues():
    """Fetch all open and closed issues (excluding pull requests)."""
    issues = []
    page = 1
    while True:
        batch = github_request("GET", f"/issues?state=all&per_page=100&page={page}")
        if not batch:
            break
        for issue in batch:
            if "pull_request" not in issue:
                issues.append(issue)
        if len(batch) < 100:
            break
        page += 1
    return issues


ORDER_PATTERN = re.compile(r"^(P\d+\s+-\s+)\[(\d+/\d+)\]\s+")
BARE_PREFIX_PATTERN = re.compile(r"^(P\d+\s+-\s+)")


def strip_order_prefix(title):
    """Remove existing order prefix like '[01/12] ' from a title."""
    m = ORDER_PATTERN.match(title)
    if m:
        return m.group(1) + title[m.end():]
    return title


def build_new_title(title, position, total):
    """Build updated title with order prefix inserted after 'PXX - '."""
    clean = strip_order_prefix(title)
    m = BARE_PREFIX_PATTERN.match(clean)
    if m:
        prefix = m.group(1)
        rest = clean[m.end():]
        return f"{prefix}[{position:02d}/{total:02d}] {rest}"
    # Fallback: prepend to full title
    return f"[{position:02d}/{total:02d}] {clean}"


def update_issue_title(number, new_title):
    """PATCH the issue title on GitHub."""
    github_request("PATCH", f"/issues/{number}", {"title": new_title})


def main():
    print("Fetching all issues...")
    all_issues = get_all_issues()
    print(f"Found {len(all_issues)} issues.")

    # Group by milestone
    milestones = {}
    no_milestone = []
    for issue in all_issues:
        ms = issue.get("milestone")
        if ms:
            ms_title = ms["title"]
            milestones.setdefault(ms_title, []).append(issue)
        else:
            no_milestone.append(issue)

    if no_milestone:
        print(f"\nSkipping {len(no_milestone)} issues without a milestone.")

    for ms_title, issues in sorted(milestones.items()):
        # Sort by issue number ascending (creation order = execution order)
        issues.sort(key=lambda i: i["number"])
        total = len(issues)
        print(f"\nMilestone: {ms_title} ({total} issues)")

        for position, issue in enumerate(issues, start=1):
            number = issue["number"]
            current_title = issue["title"]
            new_title = build_new_title(current_title, position, total)

            if new_title == current_title:
                print(f"  #{number} — unchanged: {current_title}")
                continue

            print(f"  #{number} — updating:")
            print(f"    Before: {current_title}")
            print(f"    After:  {new_title}")
            update_issue_title(number, new_title)
            time.sleep(0.3)  # Respect rate limits

    print("\nDone.")


if __name__ == "__main__":
    main()
