# Username as Location Signal — Design Rationale

When the `mastodon_signups.py` classifier should accept a DMV-related token in
the **username** as an approval signal, even when the invite request text says
nothing about location. This explains the rules-of-thumb and the rejected-token
decisions so future agents know which tokens to add and which to leave out.

## Why usernames

A real DMV-area applicant whose invite text is short or generic (e.g. "Looking
to migrate our Instagram community") was being escalated to Jason even when
their username was unambiguously local (`vegan_baltimore`). The classifier
checked only the invite text. Adding a username check reduced false escalations
without changing the spam-rejection behavior.

## Threat model

A spammer who knows the username check exists will pick a DMV-flavored
username to game approval. The conservative token list is the defense: only
include tokens that are **unambiguously DMV-area place names** and not
collision-prone in non-location contexts.

## Rules of thumb for `DMV_USERNAME_PATTERNS`

For each token, ask: "Could a non-location username plausibly contain this
string as a substring?" If yes, exclude or rephrase.

| Rule | Why | Examples of excluded tokens |
|------|-----|------------------------------|
| Full city names only | Standalone city names rarely collide with non-location words | included: `baltimore`, `reston`, `hagerstown` |
| No state abbreviations | `md`/`va`/`dc` collide with too many English words | excluded: `md` (admin, vram, admin), `va` (vaper, vacation, vague) |
| No free-standing state names | `maryland`/`virginia` could appear in non-location context | excluded: both |
| No surnames | `fairfax`, `bowie`, `shaw` are real surnames | excluded: all three |
| No common English words | `circle`, `foggy`, `fresh`, `morgan` collision-prone as words | excluded: any neighborhood whose name is also an English word |
| No collision with `NON_DMV_LOCATIONS` | Same name in different states (Portland OR vs ME) | excluded: `portland`, `cambridge`, `richmond` (could be KY/CA not VA) |

## Deliberately-excluded tokens and reasons

- `va` — collides with `vape`, `vacation`, `vagrant`, every word starting Va-
- `md` — collides with `admin`, `md5`, `admin`, `adm`
- `dc` — too short, also valid initials
- `fairfax` — Lord Fairfax was a person; common surname in DMV area
- `shaw` — common surname, also a Shaw neighborhood name in DC
- `bowie` — David Bowie, surname, also Bowie MD
- `laurel` — also Laurel & Hardy, a name
- `richmond` — Richmond KY, Richmond CA exist; "richmond" used in non-location phrases
- `norfolk` — Norfolk NE/UK exist; common English surname
- `vienna` — Vienna Austria; also a surname
- `columbia` — Columbia Records, Columbia University, Columbia SC
- `loudoun` — uncommon enough that spammers would spot it as a signal
- `mclean` — could be a surname (McLean); ambiguous
- `princewilliam` — too long to game unintentionally but also unusual
- `leonardtown`, `waldorf`, `la plata` etc. — too obscure to bother (low false-positive risk but also low true-positive catch rate)

## Order of precedence in `classify_account()`

The username signal is the LAST approval check, after all reject paths have
had a chance to fire:

1. Invite text mentions DMV location → approve (primary signal)
2. Invite text mentions non-DMV location → reject (overrides username)
3. Disposable email → reject (overrides username)
4. Spam phrases ≥ 2 → reject (overrides username)
5. Single spam phrase → reject (overrides username)
6. Empty invite → reject
7. **Username has DMV location → approve** (secondary signal, only fires if all above are clear)
8. Otherwise → escalate

This ordering prevents a spammer from gaming the username check by stuffing a
DMV city name into their username while their invite text says "I live in New
York, looking for NYC community managers" — that one gets rejected at step 2,
not approved at step 7.

## When to add a new token

Add when ALL of these are true:

- The token is unambiguous in English as a DMV location (not a name or word)
- Real DMV-area users actually use it in usernames (check recent escalations)
- You've seen at least one escalation that would have been auto-approved with this token

If the answer to any of these is "not sure," leave it out. Manual escalation
is cheap; false auto-approval trains the system to be untrustworthy.

## Pre-existing `NON_DMV_LOCATIONS` bug to fix separately

The list at lines ~113-175 contains entries like `\bin\b` (Indiana) and
`\bhi\b` (Hawaii) that match common English words ("in the area", "Hi all").
This causes legitimate signups to be auto-rejected with confusing reasons
(`Non-DMV location: in`). Symptom: invite text contains a 2-letter state
abbreviation as a substring of an English word and gets killed.

Likely fix (in a separate pass):

- Tighten: change `\bin\b` to `(?<![a-z])\bin(?![a-z])` etc.
- Or: move 2-letter abbreviations to a "weak signals" tier that doesn't block username approval

Not in scope of the username-classifier change.
