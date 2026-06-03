# LastFM API Endpoints Reference

Full endpoint reference for Last.fm API. All requests: `GET https://ws.audioscrobbler.com/2.0/?method=METHOD&api_key=KEY&format=json`

## User Methods

| Method | Description | Required Params | Optional Params |
|--------|-------------|-----------------|-----------------|
| `user.getinfo` | Get user profile info | user, api_key | - |
| `user.getrecenttracks` | Get recent scrobbles | user, api_key | limit, page, from, to, extended (0/1) |
| `user.gettopartists` | Get top artists | user, api_key | period, limit, page |
| `user.gettopalbums` | Get top albums | user, api_key | period, limit, page |
| `user.gettoptracks` | Get top tracks | user, api_key | period, limit, page |
| `user.getweeklychartlist` | Get weekly chart date ranges | user, api_key | - |
| `user.getweeklyartistchart` | Get weekly artist chart | user, api_key, from, to | - |
| `user.getnewreleases` | Get new releases for user | user, api_key | **NOTE:** Returns limited data without reliable release dates. Use MusicBrainz API instead. |

## Chart Methods

| Method | Description | Required Params | Optional Params |
|--------|-------------|-----------------|-----------------|
| `chart.gettopartists` | Get site-wide top artists | api_key | limit, page |
| `chart.gettoptracks` | Get site-wide top tracks | api_key | limit, page |
| `chart.gethypedtracks` | Get hyped/up-and-coming tracks | api_key | limit, page |
| `chart.getlovedtracks` | Get loved tracks site-wide | api_key | limit, page |

## Artist Methods

| Method | Description | Required Params | Optional Params |
|--------|-------------|-----------------|-----------------|
| `artist.getinfo` | Get artist info | artist, api_key | autocorrections (0/1), lang |
| `artist.gettoptags` | Get top tags for artist | artist, api_key | - |
| `artist.getsimilar` | Get similar artists | artist, api_key | limit |
| `artist.search` | Search artists | artist, api_key | limit, page |

## Album Methods

| Method | Description | Required Params | Optional Params |
|--------|-------------|-----------------|-----------------|
| `album.getinfo` | Get album info | artist, album, api_key | - |
| `album.search` | Search albums | album, api_key | artist, limit, page |

## Common Error Codes

| Code | Meaning |
|------|---------|
| 4 | Authentication Failed |
| 6 | Invalid parameters (missing required param) |
| 9 | Invalid session key (for authenticated methods) |
| 10 | Invalid API key |
| 12 | User not found |

## Rate Limits

- ~3 requests/second per API key
- No daily quota documented
