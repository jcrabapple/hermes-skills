#!/usr/bin/env python3
"""Mastodon report monitor for dmv.community.

Fetches unresolved reports, classifies them, auto-acts on clear violations,
and outputs a JSON summary for the cron agent to format and deliver.

Exit codes: always 0 (never blocks the cron job)
Output: JSON on stdout
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

INSTANCE = "dmv.community"
API_BASE = f"https://{INSTANCE}/api/v1/admin"
TOKEN_FILE = os.path.expanduser("~/.hermes/secrets/mastodon_token")
ADMIN_ACCOUNT_ID = os.environ.get("MASTODON_ADMIN_ID", "")  # Set to your account ID - never moderate this

# Rule IDs that trigger auto-action
AUTO_SUSPEND_RULES = {"3", "5"}  # violence, illegal content
AUTO_SILENCE_RULES = {"2", "4"}  # hate speech, harassment/doxxing
AUTO_SPAM_RULES = {"7"}  # spam
# Rules that always require escalation: 1 (sensitive media), 6 (misinfo), 8 (AI art), 9 (AI music)

# Keywords that strengthen severity assessment
SEVERE_KEYWORDS = [
    "kill", "murder", "rape", "threat", "terror", "bomb", "weapon",
    "csam", "cp", "pedo", "child abuse", "loli", "shota",
    "doxx", "dox", "home address", "phone number", "ssn",
    "nigger", "faggot", "tranny", "spic", "kike", "wetback",
]


def load_token():
    with open(TOKEN_FILE) as f:
        return f.read().strip()


def api_request(endpoint, method="GET", fields=None):
    """Make an admin API request using multipart form data."""
    import uuid

    url = f"{API_BASE}/{endpoint}"
    token = load_token()
    headers = {"Authorization": f"Bearer {token}"}

    if fields:
        boundary = uuid.uuid4().hex
        body = b""
        for key, value in fields:
            body += f"--{boundary}\r\n".encode()
            body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode()
            body += f"{value}\r\n".encode()
        body += f"--{boundary}--\r\n".encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode()), resp.status
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            return json.loads(error_body), e.code
        except json.JSONDecodeError:
            return {"error": error_body[:500]}, e.code
    except Exception as e:
        return {"error": str(e)}, 0


def strip_html(text):
    """Remove HTML tags from text."""
    if not text:
        return ""
    return re.sub(r'<[^>]+>', '', text).strip()


def get_report_context(report):
    """Extract key fields from a report for classification."""
    target = report.get("target_account", {})
    target_acct = target.get("account", {}).get("acct", "unknown")
    target_id = target.get("id", "")

    reporter = report.get("account", {})
    reporter_acct = reporter.get("account", {}).get("acct", "unknown") if isinstance(reporter.get("account"), dict) else reporter.get("acct", "unknown")

    statuses = report.get("statuses", [])
    status_texts = [strip_html(s.get("content", "")) for s in statuses]
    status_urls = [s.get("url", "") for s in statuses]

    rules = report.get("rules", [])
    rule_ids = {r.get("id", "") for r in rules}

    comment = report.get("comment", "")
    category = report.get("category", "other")

    # Combine all text for keyword analysis
    all_text = f"{comment} {' '.join(status_texts)}".lower()

    has_severe_keywords = any(kw in all_text for kw in SEVERE_KEYWORDS)

    return {
        "report_id": report.get("id", ""),
        "category": category,
        "comment": comment,
        "target_acct": target_acct,
        "target_id": target_id,
        "reporter_acct": reporter_acct,
        "rule_ids": rule_ids,
        "status_texts": status_texts,
        "status_urls": status_urls,
        "has_severe_keywords": has_severe_keywords,
        "statuses_count": len(statuses),
    }


def classify_report(ctx):
    """Classify a report into an action category.

    Returns: dict with 'action' and 'reason'.
    """
    # Never moderate the admin account
    if ctx["target_id"] == ADMIN_ACCOUNT_ID:
        return {
            "action": "escalated",
            "reason": "Report targets the instance admin account - requires human review"
        }

    # Empty report with no content
    if not ctx["comment"] and ctx["statuses_count"] == 0 and not ctx["rule_ids"]:
        return {
            "action": "dismissed",
            "reason": "Empty report - no comment, no statuses, no rules cited"
        }

    rule_ids = ctx["rule_ids"]

    # Check for auto-suspend rules (violence, illegal content)
    if rule_ids & AUTO_SUSPEND_RULES:
        rule_nums = ", ".join(sorted(rule_ids & AUTO_SUSPEND_RULES))
        action = "suspended"
        reason = f"Rule {rule_nums}: clear violation (violence/illegal content)"
        if ctx["has_severe_keywords"]:
            reason += " - severe keywords detected"
        return {"action": action, "reason": reason}

    # Check for spam (rule 7)
    if rule_ids & AUTO_SPAM_RULES:
        return {
            "action": "suspended",
            "reason": "Rule 7: spam/advertising"
        }

    # Check for hate speech / harassment (rules 2, 4)
    if rule_ids & AUTO_SILENCE_RULES:
        rule_nums = ", ".join(sorted(rule_ids & AUTO_SILENCE_RULES))
        # Severe keywords or repeat offenses escalate to suspend
        if ctx["has_severe_keywords"]:
            return {
                "action": "suspended",
                "reason": f"Rule {rule_nums}: severe hate speech/harassment with threatening language"
            }
        return {
            "action": "silenced",
            "reason": f"Rule {rule_nums}: hate speech/harassment (first offense, silenced)"
        }

    # Rules that always need human judgment
    escalation_rules = {"1", "6", "8", "9"}
    if rule_ids & escalation_rules:
        rule_nums = ", ".join(sorted(rule_ids & escalation_rules))
        return {
            "action": "escalated",
            "reason": f"Rule {rule_nums}: requires human judgment"
        }

    # No rules cited but has content - escalate
    if ctx["statuses_count"] > 0 or ctx["comment"]:
        return {
            "action": "escalated",
            "reason": "No specific rule cited - requires human review"
        }

    # Default: dismiss
    return {
        "action": "dismissed",
        "reason": "No actionable content found"
    }


def execute_action(report_id, ctx, decision):
    """Execute the moderation action."""
    action = decision["action"]
    reason = decision["reason"]
    target_id = ctx["target_id"]
    results = {"action": action, "reason": reason}

    if action == "suspended":
        # Suspend the account
        resp, code = api_request(
            f"accounts/{target_id}/action",
            method="POST",
            fields=[("type", "suspend"), ("warning", "0")]
        )
        results["suspend_response"] = resp
        results["suspend_status"] = code

        # Resolve the report
        resp, code = api_request(
            f"reports/{report_id}/resolve",
            method="POST",
            fields=[]
        )
        results["resolve_response"] = resp
        results["resolve_status"] = code

    elif action == "silenced":
        # Silence the account
        resp, code = api_request(
            f"accounts/{target_id}/action",
            method="POST",
            fields=[("type", "silence"), ("warning", "0")]
        )
        results["silence_response"] = resp
        results["silence_status"] = code

        # Resolve the report
        resp, code = api_request(
            f"reports/{report_id}/resolve",
            method="POST",
            fields=[]
        )
        results["resolve_response"] = resp
        results["resolve_status"] = code

    elif action == "dismissed":
        # Resolve the report with a comment
        resp, code = api_request(
            f"reports/{report_id}/resolve",
            method="POST",
            fields=[]
        )
        results["resolve_response"] = resp
        results["resolve_status"] = code

    # For "escalated" - do nothing, just report it
    return results


def main():
    # Fetch unresolved reports
    reports_data, code = api_request("reports?resolved=false&limit=40")

    if code != 200 or not isinstance(reports_data, list):
        # API error - output error and exit 0
        output = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": f"Failed to fetch reports: HTTP {code}",
            "api_response": reports_data if isinstance(reports_data, dict) else None,
            "total_reports": 0,
            "auto_actioned": 0,
            "escalated": 0,
            "dismissed": 0,
            "details": []
        }
        print(json.dumps(output, indent=2))
        return

    if not reports_data:
        # No reports - silent
        output = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_reports": 0,
            "auto_actioned": 0,
            "escalated": 0,
            "dismissed": 0,
            "details": []
        }
        print(json.dumps(output, indent=2))
        return

    details = []
    auto_actioned = 0
    escalated = 0
    dismissed = 0

    for report in reports_data:
        ctx = get_report_context(report)
        decision = classify_report(ctx)

        if decision["action"] in ("suspended", "silenced"):
            results = execute_action(ctx["report_id"], ctx, decision)
            auto_actioned += 1
            details.append({
                "report_id": ctx["report_id"],
                "target": ctx["target_acct"],
                "action": decision["action"],
                "reason": decision["reason"],
                "statuses_reported": ctx["statuses_count"],
                "status_urls": ctx["status_urls"][:3],
                "api_results": results
            })
        elif decision["action"] == "dismissed":
            results = execute_action(ctx["report_id"], ctx, decision)
            dismissed += 1
            details.append({
                "report_id": ctx["report_id"],
                "target": ctx["target_acct"],
                "action": "dismissed",
                "reason": decision["reason"],
                "api_results": results
            })
        else:  # escalated
            escalated += 1
            details.append({
                "report_id": ctx["report_id"],
                "target": ctx["target_acct"],
                "reporter": ctx["reporter_acct"],
                "action": "escalated",
                "reason": decision["reason"],
                "comment": ctx["comment"][:500],
                "status_texts": ctx["status_texts"][:3],
                "status_urls": ctx["status_urls"][:3],
                "rules_cited": sorted(ctx["rule_ids"]),
                "admin_url": f"https://dmv.community/admin/reports/{ctx['report_id']}"
            })

    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_reports": len(reports_data),
        "auto_actioned": auto_actioned,
        "escalated": escalated,
        "dismissed": dismissed,
        "details": details
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
