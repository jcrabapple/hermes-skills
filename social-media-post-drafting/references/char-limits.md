# Social Media Char Limits

Default and variable limits per platform. Verify the actual cap for the user's account/instance when possible.

| Platform | Default | Variable? | Notes |
|----------|---------|-----------|-------|
| Mastodon | 500 | **Yes — per instance** | Admin sets `MAX_TOOT_CHARS` in the config. Range seen in the wild: 500–10,000. |
| X (Twitter) | 280 (free) / 4000 (Premium) | Yes — by tier | Free: 280 chars OR 25,000 for Premium users (rolled out 2023+). URL always reserves 23 chars. |
| LinkedIn (post) | 3000 | No (effectively) | Comments capped at 1250. Articles are separate (110,000). |
| Bluesky | 300 | No | |
| Threads | 500 | No | |
| Facebook | 63,206 | No | Effectively no limit. First 480 chars show before "See more." |
| Instagram caption | 2200 | No | First 125 chars show before truncation. Hashtags: up to 30. |

## Verifying a Mastodon instance's cap

The compose box shows the live counter as the user types — the displayed maximum is the cap. For programmatic check:

```bash
curl -s https://INSTANCE/api/v1/instance | jq .max_toot_chars
# or v2:
curl -s https://INSTANCE/api/v2/instance | jq .configuration.statuses.max_characters
```

If unsure, ask. Don't assume 500.

## Verifying an X account's tier
Look for the badge in the compose UI or check `GET /2/users/me` with `user.fields=verified_type` and a Premium check. Free = 280, Premium = 25,000 (effectively unlimited for most posts). Don't assume 280.

## LinkedIn hard cap quirk
Posts hit a hard 3000-char limit and silently truncate. Comment-thread root posts also have a 1250-char cap. If the draft is meant to be a comment, count against 1250, not 3000.
