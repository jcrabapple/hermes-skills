#!/usr/bin/env python3
"""Mastodon signup approval assistant for dmv.community.

Fetches pending account registrations, classifies them based on whether
the invite request mentions a DMV-area location, auto-rejects clear spam,
auto-approves DMV-area applicants, and escalates borderline cases to Jason.

DMV area = Maryland, Virginia, Washington DC, and nearby areas.

Exit codes: always 0 (never blocks the cron job)
Output: JSON on stdout
"""

import json
import os
import re
import time
import urllib.request
import urllib.error
import uuid
from datetime import datetime, timezone

INSTANCE = "dmv.community"
API_BASE = f"https://{INSTANCE}/api/v1"
TOKEN_FILE = os.path.expanduser("~/.hermes/secrets/mastodon_token")

DMV_STATES = [
    r'\bmaryland\b', r'\bmd\b', r'\bvirginia\b', r'\bva\b',
    r'\bwashington\s+dc\b', r'\bdc\b', r'\bd\.?c\.?\b',
    r'\bwest\s+virginia\b', r'\bwv\b',
    r'\bdelaware\b', r'\bde\b',
    r'\bpennsylvania\b', r'\bpa\b',
]

# Location tokens that commonly appear in Mastodon usernames. Used as a
# secondary approval signal when the invite text doesn't mention a DMV
# location but the username clearly does (e.g. "vegan_baltimore",
# "dmvartist", "nova_writer"). Patterns must be unambiguous — no
# overlap with NON_DMV_LOCATIONS — to prevent spammer gaming.
#
# Rules of thumb for this list:
#   1. Only full city/region names — no state abbreviations (md/va/dc
#      collide with too many words like "admin", "vaper", "vacation").
#   2. No full state names (maryland/virginia could appear in non-location
#      usernames via topic keywords).
#   3. Drop names that are common surnames or generic English words
#      (fairfax, shaw, bowie, laurel, norfolk) — too easy to game.
#   4. Names must not collide with NON_DMV_LOCATIONS (no Portland, no
#      Cambridge, no Richmond TX, etc.).
#   5. Match as standalone tokens bounded by underscores, hyphens, or
#      string boundaries — never mid-word.
DMV_USERNAME_PATTERNS = [
    # Maryland
    r'(?:^|_|-)baltimore(?:_|-|$)',
    r'(?:^|_|-)silver[_-]?spring(?:_|-|$)',
    r'(?:^|_|-)bethesda(?:_|-|$)',
    r'(?:^|_|-)rockville(?:_|-|$)',
    r'(?:^|_|-)takoma[_-]?park(?:_|-|$)',
    r'(?:^|_|-)hyattsville(?:_|-|$)',
    r'(?:^|_|-)hagerstown(?:_|-|$)',
    r'(?:^|_|-)annapolis(?:_|-|$)',
    r'(?:^|_|-)gaithersburg(?:_|-|$)',
    r'(?:^|_|-)greenbelt(?:_|-|$)',
    r'(?:^|_|-)frederick(?:_|-|$)',  # MD city — most common usage in usernames
    # Virginia
    r'(?:^|_|-)arlington(?:_|-|$)',
    r'(?:^|_|-)alexandria(?:_|-|$)',
    r'(?:^|_|-)winchester(?:_|-|$)',
    r'(?:^|_|-)reston(?:_|-|$)',
    r'(?:^|_|-)herndon(?:_|-|$)',
    r'(?:^|_|-)mclean(?:_|-|$)',
    r'(?:^|_|-)tysons(?:_|-|$)',
    r'(?:^|_|-)manassas(?:_|-|$)',
    r'(?:^|_|-)leesburg(?:_|-|$)',
    r'(?:^|_|-)charlottesville(?:_|-|$)',
    r'(?:^|_|-)cville(?:_|-|$)',
    r'(?:^|_|-)harrisonburg(?:_|-|$)',
    r'(?:^|_|-)staunton(?:_|-|$)',
    r'(?:^|_|-)vabeach(?:_|-|$)',
    r'(?:^|_|-)va[_-]?beach(?:_|-|$)',
    r'(?:^|_|-)virginia[_-]?beach(?:_|-|$)',
    r'(?:^|_|-)fredericksburg(?:_|-|$)',
    r'(?:^|_|-)frontroyal(?:_|-|$)',
    r'(?:^|_|-)warrenton(?:_|-|$)',
    r'(?:^|_|-)culpeper(?:_|-|$)',
    # DC
    r'(?:^|_|-)georgetown(?:_|-|$)',
    r'(?:^|_|-)capitol[_-]?hill(?:_|-|$)',
    r'(?:^|_|-)navyyard(?:_|-|$)',
    r'(?:^|_|-)navy[_-]?yard(?:_|-|$)',
    r'(?:^|_|-)adamsmorgan(?:_|-|$)',
    r'(?:^|_|-)adams[_-]?morgan(?:_|-|$)',
    r'(?:^|_|-)columbia[_-]?heights(?:_|-|$)',
    r'(?:^|_|-)anacostia(?:_|-|$)',
    r'(?:^|_|-)dupont[_-]?circle(?:_|-|$)',
    r'(?:^|_|-)foggy[_-]?bottom(?:_|-|$)',
    # Regional shorthand
    r'(?:^|_|-)dmv(?:_|-|$)',
    r'(?:^|_|-)nova(?:_|-|$)',
    # WV panhandle (close enough to DMV community)
    r'(?:^|_|-)martinsburg(?:_|-|$)',
    r'(?:^|_|-)harpersferry(?:_|-|$)',
    r'(?:^|_|-)harper[_-]?s[_-]?ferry(?:_|-|$)',
    r'(?:^|_|-)charles[_-]?town(?:_|-|$)',
]

DMV_CITIES = [
    # DC
    r'\bwashington\b', r'\bgeorgetown\b', r'\bnavy\s+yard\b', r'\bcapitol\s+hill\b',
    r'\badams\s+morgan\b', r'\bdupont\b', r'\bduPont\b', r'\bshaw\b',
    r'\banacostia\b', r'\bcolumbia\s+heights\b',
    r'\bnoma\b', r'\bpenn\s+quarter\b', r'\bfoggy\s+bottom\b',
    r'\blogan\s+circle\b', r'\bu\s+street\b',
    # Maryland
    r'\bbaltimore\b', r'\bsilver\s+spring\b', r'\bcollege\s+park\b', r'\bfrederick\b',
    r'\bgaithersburg\b', r'\brockville\b', r'\bbethesda\b', r'\bchevy\s+chase\b',
    r'\btakoma\s+park\b', r'\bgreenbelt\b', r'\blaurel\b', r'\bbowie\b',
    r'\bannapolis\b', r'\bcolumbia\b', r'\bellicott\s+city\b', r'\bhoward\s+county\b',
    r'\bmontgomery\s+county\b', r'\bprince\s+george', r'\bpg\s+county\b',
    r'\bcharles\s+county\b', r'\bfrederick\s+county\b', r'\bcarroll\s+county\b',
    r'\bharford\s+county\b', r'\bwicomico\b', r'\bsalisbury\b', r'\bocean\s+city\b',
    r'\bhagerstown\b', r'\bcumberland\b', r'\baberdeen\b', r'\bbeltsville\b',
    r'\bclinton\b', r'\bupper\s+marlboro\b', r'\bglen\s+arden\b', r'\bseabrook\b',
    r'\blandover\b', r'\bhyattsville\b', r'\bmount\s+rainier\b', r'\bnew\s+carrollton\b',
    r'\beaston\b', r'\bst\s+michaels\b', r'\bcambridge\b', r'\boxford\b',
    r'\bbaltimore\s+county\b', r'\bharford\b', r'\bcalvert\b', r'\bst\s+mary',
    # Virginia
    r'\barlington\b', r'\balexandria\b', r'\bfairfax\b', r'\breston\b', r'\bherndon\b',
    r'\bvienna\b', r'\bfalls\s+church\b', r'\bmclean\b', r'\btysons\b', r'\bchantilly\b',
    r'\bcentreville\b', r'\bmanassas\b', r'\bwoodbridge\b', r'\bdale\s+city\b',
    r'\bfredericksburg\b', r'\brichmond\b', r'\bwinchester\b', r'\blynchburg\b',
    r'\bcharlottesville\b', r'\bharrisonburg\b', r'\bstaunton\b', r'\broanoke\b',
    r'\bblacksburg\b', r'\bnewport\s+news\b', r'\bhampton\b', r'\bnorfolk\b',
    r'\bvirginia\s+beach\b', r'\bchesapeake\b', r'\bsuffolk\b', r'\bportsmouth\b',
    r'\bfairfax\s+county\b', r'\bloudoun\b', r'\bprince\s+william\b',
    r'\barlington\s+county\b', r'\bhenrico\b', r'\bchesterfield\b',
    r'\bspringfield\b', r'\bburke\b', r'\bfranconia\b', r'\bkingstowne\b',
    r'\bleesburg\b', r'\bashburn\b', r'\bsterling\b', r'\bpurcellville\b',
    r'\bfront\s+royal\b', r'\bwarrenton\b', r'\bculpeper\b', r'\borange\b',
    r'\bclarendon\b', r'\bcrystal\s+city\b', r'\bpentagon\b',
    # WV panhandle
    r'\bmartinsburg\b', r'\bharpers\s+ferry\b', r'\bcharles\s+town\b',
    # General
    r'\bdmv\b', r'\bdmv\s+area\b', r'\bdmv\s+community\b',
    r'\bnational\s+capital\s+region\b', r'\bnova\b',
    r'\bmo\s+county\b',
    r'\bjhu\b', r'\bhopkins\b',
    r'\bgeorge\s+(mason|washington)\b', r'\bgmu\b',
    r'\bumd\b',
]

SPAM_PHRASES = [
    r'looking\s+to\s+connect\s+with\s+others',
    r'join\s+a\s+(friendly\s+)?community',
    r'participate\s+in\s+discussions',
    r'share\s+my\s+thoughts',
    r'looking\s+for\s+a\s+new\s+home',
    r'explore\s+(new\s+)?content',
    r'engage\s+with\s+(like-minded|others)',
    r'looking\s+for\s+a\s+place\s+to',
    r'connect\s+with\s+like\s*-?\s*minded',
    # Mastodon follower-farming / self-promotion patterns
    r'boosts?\s+(are\s+)?appreciated',
    r'please\s+boost',
    r'boost\s+for\s+boost',
    r'b4b\b',
    r'follow\s+for\s+follow',
    r'f4f\b',
    r'looking\s+for\s+mutuals',
    r'art\s+tag\s*:',  # self-promotional "art tag:" prefix
    r'commissions?\s+open',
    r'comms?\s+open',
    r'boost\s+my\s+',
]

SPAM_TOPICS = [
    r'crypto', r'nft', r'blockchain', r'trading', r'forex', r'bitcoin',
    r'mining', r'airdrop', r'defi', r'seo', r'digital\s+marketing',
    r'backlink', r'affiliate',
    # vtuber / streaming promotion (common Mastodon spam on local instances)
    r'\bvtuber\b', r'\benvtuber\b', r'envtube',
    r'\bstan\s+account\b',
]

NON_DMV_LOCATIONS = [
    # International
    r'\buk\b', r'\bunited\s+kingdom\b', r'\blondon\b', r'\bscotland\b', r'\bglasgow\b',
    r'\bgermany\b', r'\bbrazil\b', r'\bindia\b', r'\bnigeria\b', r'\bpakistan\b',
    r'\bphilippines\b', r'\bjapan\b', r'\baustralia\b', r'\bnew\s+zealand\b',
    r'\bwight\b', r'\blanguedoc\b', r'\baotearoa\b', r'\bwellington\b',
    r'\bho\s+chi\s+minh\b', r'\bvietnam\b', r'\bsaigon\b',
    r'\blagos\b', r'\bkenya\b', r'\bnairobi\b',
    r'\bdubai\b', r'\bsydney\b', r'\bmelbourne\b',
    r'\btoronto\b', r'\bontario\b', r'\bcanada\b',
    # US states outside DMV area
    r'\bcalifornia\b', r'\bcali\b', r'\blos\s+angeles\b', r'\bla\b',
    r'\bsan\s+francisco\b', r'\bsf\b', r'\bsan\s+diego\b',
    r'\bsacramento\b', r'\bsan\s+jose\b', r'\boakland\b', r'\bfresno\b',
    r'\bnew\s+york\b', r'\bnyc\b', r'\bmanhattan\b', r'\brooklyn\b',
    r'\bqueens\b', r'\bbronx\b', r'\bbuffalo\b', r'\balbany\b',
    r'\btexas\b', r'\btx\b', r'\baustin\b', r'\bhouston\b',
    r'\bdallas\b', r'\bsan\s+antonio\b', r'\bfort\s+worth\b', r'\bel\s+paso\b',
    r'\bflorida\b', r'\bfl\b', r'\bmiami\b', r'\borlando\b',
    r'\btampa\b', r'\bjacksonville\b', r'\btallahassee\b',
    r'\bchicago\b', r'\billinois\b', r'\bil\b', r'\baurora\b', r'\bnaperville\b',
    r'\bseattle\b', r'\bwashington\s+state\b', r'\bportland\b', r'\boregon\b', r'\bor\b',
    r'\bphoenix\b', r'\barizona\b', r'\baz\b', r'\btucson\b', r'\bmesa\b',
    r'\bdenver\b', r'\bcolorado\b', r'\bco\b', r'\bboulder\b',
    r'\batlanta\b', r'\bgeorgia\b', r'\bga\b', r'\bsavannah\b',
    r'\bboston\b', r'\bmassachusetts\b', r'\bma\b', r'\bcambridge\b',
    r'\bdetroit\b', r'\bmichigan\b', r'\bmi\b', r'\bgrand\s+rapids\b',
    r'\bminneapolis\b', r'\bminnesota\b', r'\bmn\b', r'\bst\s+paul\b',
    r'\bkansas\s+city\b', r'\bmissouri\b', r'\bmo\b', r'\bst\s+louis\b',
    r'\bnew\s+orleans\b', r'\blouisiana\b', r'\bla\b',
    r'\bnashville\b', r'\btennessee\b', r'\btn\b', r'\bmemphis\b',
    r'\bnorth\s+carolina\b', r'\bnc\b', r'\bcharlotte\b', r'\braleigh\b',
    r'\bsouth\s+carolina\b', r'\bsc\b', r'\bcharleston\b', r'\bcolumbia\s+sc\b',
    r'\bohio\b', r'\boh\b', r'\bcleveland\b', r'\bcolumbus\b', r'\bcincinnati\b',
    r'\bindianapolis\b', r'\bindiana\b', r'\bin\b',
    r'\bmilwaukee\b', r'\bwisconsin\b', r'\bwi\b', r'\bmadison\b',
    r'\blas\s+vegas\b', r'\bnevada\b', r'\bnv\b', r'\breno\b',
    r'\bsalt\s+lake\s+city\b', r'\butah\b', r'\but\b',
    r'\balbuquerque\b', r'\bnew\s+mexico\b', r'\bnm\b',
    r'\bomaha\b', r'\bnebraska\b', r'\bne\b',
    r'\boklahoma\b', r'\bok\b', r'\boklahoma\s+city\b', r'\btulsa\b',
    r'\bhonolulu\b', r'\bhawaii\b', r'\bhi\b',
    r'\banchorage\b', r'\balaska\b', r'\bak\b',
    # Common non-DMV US cities
    r'\bphilly\b', r'\bphiladelphia\b', r'\bpittsburgh\b', r'\bpgh\b',
    r'\bnew\s+jersey\b', r'\bnj\b', r'\bnewark\b', r'\bjersey\s+city\b',
    r'\bconnecticut\b', r'\bct\b', r'\bhartford\b',
    r'\brhode\s+island\b', r'\bri\b', r'\bprovidence\b',
    r'\bvermont\b', r'\bvt\b', r'\bburlington\b',
    r'\bnew\s+hampshire\b', r'\bnh\b',
    r'\bmaine\b', r'\bme\b', r'\bportland\s+me\b',
    r'\biowa\b', r'\bia\b', r'\bdes\s+moines\b',
    r'\bkansas\b', r'\bks\b', r'\bwichita\b',
    r'\barkansas\b', r'\bar\b', r'\blittle\s+rock\b',
    r'\bmississippi\b', r'\bms\b', r'\bjackson\s+ms\b',
    r'\balabama\b', r'\bal\b', r'\bbirmingham\b', r'\bmontgomery\b',
    r'\bkentucky\b', r'\bky\b', r'\blouisville\b', r'\blexington\b',
    r'\bidaho\b', r'\bid\b', r'\bboise\b',
    r'\bmontana\b', r'\bmt\b', r'\bbillings\b',
    r'\bwyoming\b', r'\bwy\b', r'\bcheyenne\b',
    r'\bsouth\s+dakota\b', r'\bsd\b', r'\bnorth\s+dakota\b', r'\bnd\b',
]

SPAM_EMAIL_DOMAINS = {
    'tmail.lt', 'tmail.com', 'ssanphone.me', 'thiefness.com', 'paratrabajar.xyz',
    'groklan.com', 'tmpmail.net', 'guerrillamail.com', 'mailinator.com',
    'tempmail.net', 'throwaway.email', 'getnada.com', 'temp-mail.org',
    'yopmail.com', 'sharklasers.com', 'guerrillamailblock.com', 'spam4.me',
    'dispostable.com', 'mintemail.com', 'mailnesia.com', 'trbvm.com',
    'fakeinbox.com', 'mailcatch.com', 'tempinbox.com', 'tmpmail.org',
    'emailfake.com', 'tempr.email', 'mohmal.com', 'dayrep.com',
    'i-love-you-3000.net', 'mozmail.com', 'passmail.net',
    # .nf disposable domains
    'free.nf', 'spammail.free.nf', 'cc.spammail.free.nf',
    # Anonymous/disposable domains seen in the wild
    'onionmail.org', '2mail.co', 'mail2tor.co',
    # .money TLD throwaway subdomains (seen 2026-07-09: sphinx.launders.money)
    'sphinx.launders.money',
}

# Substrings that, if found in the email domain, indicate spam/disposable.
# Catches variants like cc.spammail.free.nf, anything.spammail.xyz, etc.
SPAM_EMAIL_DOMAIN_SUBSTRINGS = [
    'spammail', 'tempmail', 'tmpmail', 'throwaway', 'disposable',
    'fakeinbox', 'mailnesia', 'guerrilla', '10minutemail', 'mail2tor',
    # Catch-all for throwaway subdomains under sketchy TLDs (seen 2026-07-09:
    # sphinx.launders.money). "launders" is non-standard and only appears in
    # these disposable schemes. ".money" TLD is heavily abused for one-off
    # throwaway inboxes — block the whole TLD substring.
    'launders', '.money',
]

ADMIN_ACCOUNT_ID = os.environ.get("MASTODON_ADMIN_ID", "")


def load_token():
    with open(TOKEN_FILE) as f:
        return f.read().strip()


def api_request(endpoint, method="GET", fields=None):
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


def find_matches(text, patterns):
    matches = []
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            clean = pattern.replace(r'\b', '').replace(r'\s+', ' ')
            clean = clean.replace(r'\.', '').replace(r'-?\s*', ' ')
            clean = clean.strip()
            if clean not in matches:
                matches.append(clean)
    return matches


def classify_account(account):
    username = account.get("username", "unknown")
    email = account.get("email", "")
    invite_request = account.get("invite_request", "") or ""
    text_lower = invite_request.lower()
    username_lower = username.lower()
    email_domain = email.lower().split("@")[-1] if "@" in email.lower() else ""

    if account.get("id") == ADMIN_ACCOUNT_ID:
        return {"action": "skip", "reason": "Admin account"}

    dmv_matches = find_matches(text_lower, DMV_STATES + DMV_CITIES)
    spam_phrase_matches = find_matches(text_lower, SPAM_PHRASES)
    spam_topic_matches = find_matches(text_lower, SPAM_TOPICS)
    all_spam_matches = spam_phrase_matches + spam_topic_matches
    non_dmv_matches = find_matches(text_lower, NON_DMV_LOCATIONS)
    username_dmv_matches = find_matches(username_lower, DMV_USERNAME_PATTERNS)
    is_spam_email = email_domain in SPAM_EMAIL_DOMAINS
    # Also check for spam keywords anywhere in the email domain
    if not is_spam_email and email_domain:
        for substr in SPAM_EMAIL_DOMAIN_SUBSTRINGS:
            if substr in email_domain:
                is_spam_email = True
                email_domain = f"{email_domain} (matched: {substr})"
                break

    # Primary: invite text mentions a DMV location.
    if dmv_matches:
        return {"action": "approve", "reason": f"DMV area mentioned: {', '.join(dmv_matches[:3])}"}

    # Reject if invite text explicitly names a non-DMV location — even if
    # the username contains a DMV city name. Prevents gaming the username
    # check by hiding a real location in invite text.
    if non_dmv_matches:
        return {"action": "reject", "reason": f"Non-DMV location: {', '.join(non_dmv_matches[:2])}"}

    # Reject if disposable email — spammer incentive outweighs location signal.
    if is_spam_email:
        return {"action": "reject", "reason": f"Disposable email domain: {email_domain}"}

    # Reject obvious spam indicators even if username looks DMV-local.
    if len(all_spam_matches) >= 2:
        return {"action": "reject", "reason": f"Multiple spam indicators: {', '.join(all_spam_matches[:3])}"}

    if len(all_spam_matches) >= 1:
        return {"action": "reject", "reason": f"Spam indicator: {all_spam_matches[0]}"}

    if not invite_request.strip():
        return {"action": "reject", "reason": "Empty invite request"}

    # Secondary: username clearly references a DMV location. Only used when
    # invite text has no conflicting signals (non-DMV locations, spam,
    # disposable email all checked above).
    if username_dmv_matches:
        return {"action": "approve", "reason": f"DMV location in username: {', '.join(username_dmv_matches[:2])}"}

    return {"action": "escalate", "reason": "No DMV area mentioned, no clear spam indicators"}


def execute_action(account_id, decision):
    action = decision["action"]
    results = {"action": action}

    if action == "approve":
        time.sleep(2)
        resp, code = api_request(f"admin/accounts/{account_id}/approve", method="POST")
        if code == 403:
            results["api_status"] = 200
            results["note"] = "Already approved"
        else:
            results["api_status"] = code

    elif action == "reject":
        time.sleep(2)
        resp, code = api_request(
            f"admin/accounts/{account_id}/reject",
            method="POST",
            fields=[("comment", decision["reason"])]
        )
        if code == 403:
            results["api_status"] = 200
            results["note"] = "Already rejected"
        else:
            results["api_status"] = code

    return results


def main():
    accounts_data, code = api_request("admin/accounts?status=pending&limit=40")

    if code != 200 or not isinstance(accounts_data, list):
        print(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": f"Failed to fetch pending accounts: HTTP {code}",
            "total_pending": 0, "auto_approved": 0, "auto_rejected": 0,
            "escalated": 0, "skipped": 0, "details": []
        }, indent=2))
        return

    if not accounts_data:
        print(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_pending": 0, "auto_approved": 0, "auto_rejected": 0,
            "escalated": 0, "skipped": 0, "details": []
        }, indent=2))
        return

    details = []
    auto_approved = 0
    auto_rejected = 0
    escalated = 0
    skipped = 0

    for account in accounts_data:
        username = account.get("username", "unknown")
        account_id = account.get("id", "")
        email = account.get("email", "")
        invite_request = account.get("invite_request", "") or ""
        ip = account.get("ip", "")
        created_at = account.get("created_at", "")
        already_approved = account.get("approved", False)

        # Mastodon 4.6 returns already-approved accounts in status=pending
        # results. Skip them entirely before classifying to avoid
        # re-reporting accounts that have already been handled.
        if already_approved:
            skipped += 1
            details.append({
                "username": username, "account_id": account_id,
                "action": "skip", "reason": "Already approved",
            })
            continue

        decision = classify_account(account)

        if decision["action"] in ("approve", "reject"):
            results = execute_action(account_id, decision)
            if decision["action"] == "approve":
                auto_approved += 1
            else:
                auto_rejected += 1
            details.append({
                "username": username, "account_id": account_id,
                "email": email, "invite_request": invite_request[:300],
                "ip": ip, "created_at": created_at,
                "action": decision["action"], "reason": decision["reason"],
                "api_status": results.get("api_status"), "note": results.get("note", ""),
            })
        elif decision["action"] == "skip":
            skipped += 1
            details.append({
                "username": username, "account_id": account_id,
                "action": "skip", "reason": decision["reason"],
            })
        else:
            escalated += 1
            details.append({
                "username": username, "account_id": account_id,
                "email": email, "invite_request": invite_request[:300],
                "ip": ip, "created_at": created_at,
                "action": "escalated", "reason": decision["reason"],
                "admin_url": f"https://dmv.community/admin/accounts/{account_id}",
            })

    print(json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_pending": len(accounts_data),
        "auto_approved": auto_approved,
        "auto_rejected": auto_rejected,
        "escalated": escalated,
        "skipped": skipped,
        "details": details
    }, indent=2))


if __name__ == "__main__":
    main()
