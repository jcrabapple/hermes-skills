# Organizational Contact Lookup

Finding a specific person's email or phone at a university, company, or institution when it's not publicly listed.

## Strategy (ordered by reliability)

### 1. Official Directory Pages
Most universities and large orgs have staff directories. They often hide emails behind web forms ("Send X an e-mail") or obfuscate them with JavaScript.

**Technique — curl the raw HTML:**
```bash
curl -sL "https://university.edu/directory/?dept_id=XXX" | grep -i -A30 "personname"
```
Look for:
- `mailto:` links in `<a>` tags
- `dept_person_email` divs with form links (email not exposed)
- `data-email` attributes on elements
- JavaScript email decryption patterns (hex-encoded `&#xx;` entities)

**When the directory uses a relay form** (no direct email in HTML):
- The form URL often contains an encoded user ID: `?webAction=showEmailForm&up=285BE2F852CBC4`
- This confirms the person exists but doesn't reveal the email

### 2. Infer from Naming Convention
Every org has a standard email format. Discover it by finding ONE person with a known email, then apply the pattern.

**Common patterns:**
| Pattern | Example | Common at |
|---------|---------|-----------|
| `firstname.lastname@` | `john.smith@uni.edu` | Most universities |
| `firstnamelastname@` (no dot) | `johnsmith@uni.edu` | GWU, some state schools |
| `firstinitiallastname@` | `jsmith@uni.edu` | Corporate, older systems |
| `lastname@` | `smith@uni.edu` | Small orgs, faculty |
| `firstinitialmiddlInitiallastname@` | `jaesmith@uni.edu` | Large universities with name collisions |

**How to discover the pattern:**
1. Search `site:uni.edu "@uni.edu"` — faculty pages often list emails in plain text
2. Check faculty/staff bio pages — they usually expose emails directly (unlike IT/admin directories)
3. Look at the directory page for OTHER people in the same department — sometimes the pattern is visible for some but not all

**GWU specifically:** Uses `firstnamelastname@gwu.edu` (no dot separator), e.g., `badies@gwu.edu`, `lfarhadi@gwu.edu`, `hamdar@gwu.edu`, `danmengshuai@gwu.edu`

### 3. Email Finder Sites (use as confirmation, not primary)
Sites like anymailfinder, hunter.io, rocketreach aggregate emails but:
- Usually paywalled behind registration
- The free preview often shows `abcdefgh@domain.edu` (placeholder)
- Can confirm the domain pattern even when hiding the specific address
- Sometimes reveal the pattern in the "Wondering if it's X, Y, or Z?" copy

### 4. LinkedIn
- Profile URL often discoverable via `"Person Name" site:linkedin.com "Company"`
- Can message directly to ask for email
- Some profiles show email in contact info section (requires connection)

### 5. Social / Other Public Records
- Twitter/X bios sometimes include work email
- Conference speaker bios often list institutional email
- Published papers list corresponding author email
- GitHub profiles may have email in commit history

## Pitfalls

- **Don't guess and blast.** If you infer `firstname.lastname@domain.edu`, verify it won't bounce. Some orgs use middle initials, hyphens, or numbers for disambiguation.
- **University relay forms are a dead end for getting the actual address.** They confirm the person exists but the reply comes from a noreply address.
- **anymailfinder/hunter.io free tiers** show the domain pattern but hide the specific email. Don't waste time clicking through — note the pattern and move on.
- **People change orgs.** Verify the person is still at the institution (LinkedIn, recent directory listing) before using as a reference.

## Output Format

When presenting findings to the user:
1. Confirm the person's name, title, and department (verified from official source)
2. State the org's email naming convention (with evidence)
3. Give the most likely email (with confidence level)
4. Provide fallback: directory form link, LinkedIn profile, or phone number
