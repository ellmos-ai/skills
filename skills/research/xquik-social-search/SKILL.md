---
name: xquik-social-search
version: 1.0.0
type: skill
author: Xquik Contributors
created: 2026-06-30
updated: 2026-06-30
description: >
  Research public X posts with Xquik's authenticated tweet search API when a task needs source-backed social signals.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: research
tags: [x, twitter, social-search, api, research]
language: en
status: active

dependencies:
  tools: [curl]
  services: [Xquik]
  protocols: []
  python: []

provenance:
  origin: "community"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/Xquik-dev/x-twitter-scraper"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Xquik Social Search

## Purpose

Use this skill to gather public X posts through Xquik for research, monitoring,
or evidence collection tasks. It keeps API access explicit, authenticated, and
bounded to source-backed search results.

## When To Activate

Use this skill when:
- The user asks to research public X posts, hashtags, accounts, or status URLs.
- The task needs recent social signals from X.
- The workflow needs a reproducible API call instead of a browser scrape.
- An MCP or agent workflow needs normalized X search input.

Do not use this skill for private account access, credential handling, automated
engagement, or claims that require non-public data.

## Requirements

Set an API key in the shell environment before making requests:

```bash
export XQUIK_API_KEY="your_api_key"
```

The public endpoint used by this skill is:

```text
GET https://xquik.com/api/v1/x/tweets/search
```

Authentication uses the `x-api-key` header.

## Workflow

1. Define the research question and the smallest useful query.
2. Choose `Latest` for time-sensitive monitoring or `Top` for relevance checks.
3. Keep `limit` small at first, then expand only when the result set is useful.
4. Save the exact query, query type, timestamp, and cursor if continuing.
5. Summarize results with source caveats instead of treating social posts as verified facts.

## Example

```bash
curl -sS "https://xquik.com/api/v1/x/tweets/search?q=from%3Avercel%20nextjs&queryType=Latest&limit=10" \
  -H "x-api-key: $XQUIK_API_KEY" \
  -H "accept: application/json"
```

## Result Handling

- Keep raw JSON when auditability matters.
- Extract post IDs, URLs, authors, timestamps, and text into a table for reports.
- Preserve cursors when pagination is needed.
- Re-run with the same query before finalizing time-sensitive findings.

## Limitations

- An API key is required.
- Results reflect public X data available through the API at request time.
- Search output should support research conclusions, not replace verification from primary sources.

## Changelog

### 1.0.0 (2026-06-30)
- Initial standalone Xquik social search skill.
