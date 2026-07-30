---
name: privat-mail-writer
version: 0.2.0
type: skill
author: Lukas Geiger + GPT
created: 2026-06-19
updated: 2026-06-19
description: This skill should be used when the user wants to write, reply to, decline, follow up on, shorten, rephrase, or draft private or semi-formal emails in their own style, especially for appointments, official cancellations, friendly short replies, and contact-dependent tone. Start profile analysis only upon a specific email writing request.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [mail, email, privat, antwort, absage, termin, schreibstil, kontaktprofil]
language: en
status: active
dependencies: {'tools': [], 'optional_tools': [{'name': 'mail-connector', 'path': '.AI/.MODULES/mail-connector/', 'cli': 'mailc', 'python_module': 'mail_connector.cli', 'usage': 'mailc context <kontakt> --mode reply --json  # Liefert Mail-Kontext als JSON für Profilaufbau', 'note': 'Optionales lokales IMAP-CLI-Tool. Nur nutzen wenn installiert (`pip install -e .` im Modulordner). Ohne dieses Tool arbeitet der Skill ohne Mailzugriff.'}], 'services': ['mail-backend-optional'], 'protocols': ['kontaktprofil', 'usecase-registry'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'None', 'origin_version': 'None', 'origin_repo': 'None', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

> **English** — Official English version of `privat-mail-writer`.


# Privat-Mail-Writer (English)

## Overview & Purpose

Privat-Mail-Writer creates short, friendly, and contact-appropriate email drafts. The skill is designed to be user-neutral: it contains no real contacts, no real signatures, and no real email contents.

The core is lazy and empirical: create or update the profile for a contact only when the user wants to write a specific email to that contact. Do not generate profiles in advance. If no email history is available, do not invent style claims; instead, write neutrally and briefly, or specifically ask for examples.

## Resources

- `CONFIG.md` - central preferences, if-then rules, permission gates, and blacklist toggles.
- `BLACKLIST.md` - exclusions for newsletters, system senders, and contacts without profiles.
- `USECASES.md` - usecase registry and rules for new usecases.
- `SIGNATURES.md` - neutral signature and greeting rules.
- `MUSTER-BLOCKS.md` - short reusable text blocks.
- `kontaktprofile.json` - empty, user-neutral schema for contact profiles. Maintain real profiles only locally and with data minimization.

## Workflow

1. **Load config:** Read `CONFIG.md`. If the blacklist is active, additionally check `BLACKLIST.md`.
2. **Check triggers:** Only profile during a concrete writing task for a specific contact, e.g., "write an email to brother Simon". No inbox sweeps just to create profiles.
3. **Check blacklist:** Newsletters, no-reply, system senders, and excluded domains/contacts do not get a contact profile. For such cases, reply neutrally or do not reply.
4. **Identify email task:** Determine goal, recipient, occasion, desired brevity, language, tone, and necessary facts.
5. **Determine usecase:** Read `USECASES.md` and select the most appropriate usecase. If no usecase fits, create a new reusable usecase or briefly ask in case of missing required information.
6. **Check contact profile:** For every non-excluded recipient, search for an existing profile in `kontaktprofile.json` or in a private local profile copy.
7. **Create or update profile:** If no robust profile exists, read up to the last ten relevant emails with that specific contact from the available email backend. Sent emails carry more weight for writing style than received emails.
8. **Save empirical data:** Store only summarizing, verifiable style, relationship, and category signals in the contact profile. Do not store raw emails, long quotes, or unnecessary personal details.
9. **Apply permission gate:** Respect the gates in `CONFIG.md` before sending, handling sensitive content, or in case of missing required information.
10. **Write draft:** Combine usecase form, contact profile, and current task. Imitate the style without inventing false intimacy, false commitments, or unverified reasons.
11. **Deliver output:** Output subject and email text by default. Only send if the user has explicitly authorized sending and a matching email tool is available.

## Contact Profiles

A contact profile does not describe the person per se, but rather the observed communication relationship and the account holder's writing style towards this person.

Profile fields should remain concise:

- last contact time
- number and timeframe of evaluated emails
- greeting and closing phrase
- informal/formal address (Du/Sie/formality)
- sentence length and typical brevity
- level of warmth, directness, commitment
- relationship assessment with confidence score
- contact category, e.g., `family`, `inner-circle`, `friends`, `colleagues`, `services`, `official`, `unknown`
- category source: user statement, email text, address book, signature, or inference
- category evidence level: `user-confirmed`, `strong`, `medium`, `weak`
- short paraphrased evidence such as "several sent emails end with 'Viele Grüße'" or "replies remain under five sentences"

Check monthly if an age check is due. If the month of the current date differs from the stored `last_age_check`, delete profiles whose `last_contact_at` is more than one year ago, and set `last_age_check` to the current date. The initial value in the neutral JSON is `2026-06-18`.

## Style Rules

- Keep it brief. Private emails rarely need long introductions.
- Stay friendly, but do not overexplain.
- State real reasons only if specified by the user or certain from context.
- For official rejections/cancellations: polite, clear, without a long novel of justification.
- In case of uncertainty about facts: ask a brief follow-up question before finalizing the draft.
- Write German texts with genuine umlauts: ä, ö, ü, Ä, Ö, Ü, ß.

## New Usecases

If an email task seems reusable and is not yet covered in `USECASES.md`, add the usecase:

- stable ID, e.g., `UC-002`
- name and typical triggers
- goal of the email
- required and optional details
- default length and tone
- short template or block sequence
- open follow-up questions if required details are missing

A one-off special case should not be bloated into a usecase. In that case, simply deliver the current draft.

## Output Format

For regular drafts:

```text
Betreff: ...

Sehr geehrte ...

...

Mit freundlichen Grüßen
[Signatur]
```

If the user only wants text without a subject line, deliver only the email text. If multiple variants make sense, offer at most two variants: "very short" and "slightly warmer".

## Limitations

Do not invent contact profiles. Do not copy confidential details from emails into the reply unnecessarily. Do not send any email without explicit authorization. Do not formulate legal, medical, or financial commitments unless explicitly specified by the user.

## Changelog

### 0.2.0 (2026-06-19)
- Added `CONFIG.md` and `BLACKLIST.md`.
- Restricted profile creation to concrete email writing tasks.
- Included contact categories with source and evidence level in the profile schema.

### 0.1.0 (2026-06-19)
- Initial version with usecase registry, signature rules, sample blocks, and empty contact profile JSON.
