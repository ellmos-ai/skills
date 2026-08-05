# Privacy notice — template for a piggyback installation

> **On the name.** In English this pattern is called *piggyback*: the application
> rides on infrastructure it does not own. The literal mode values are still
> spelled `huckepack-gift` and `huckepack-only-host`, after the German working
> title the code was built under. Prose says piggyback; configuration says
> huckepack.

> **Template only — adaptation required.** This is not a deployable privacy
> notice and **not legal advice**. Whoever hosts replaces every
> `[REPLACE: ...]` marker, deletes the blocks that do not apply, verifies every
> provider fact from current contracts, and obtains a case-specific legal
> review before real data is processed.
>
> The pattern shortens this document. It does not remove it.

Last updated: `[REPLACE: date]`
Server mode of this installation: `[REPLACE: local | huckepack-gift | huckepack-only-host]`
— verifiable at `[REPLACE: URL]/huckepack/mode`

## 1. Controller

`[REPLACE: legal name of whoever decides why and how this service runs]`<br>
`[REPLACE: postal address]` · `[REPLACE: contact]`<br>
Data protection officer, if applicable: `[REPLACE or remove]`<br>
Hosting provider: `[REPLACE: name, address, role]`

**Storing nothing does not remove the role.** The operator decides that the
service exists, what it does and which provider it calls. `[REPLACE: document
the role analysis; do not assume that the absence of a database makes the
operator a bystander.]`

## 2. Who is affected

- the visitor who uses the service;
- **the people the service contacts on the visitor's behalf** — `[REPLACE:
  describe them: called parties, recipients, third parties named in a request]`;
- `[REPLACE: administrators, support, or remove]`.

The second group is the one this pattern does *not* help. Their data are
processed no matter where the visitor's records are stored.

## 3. Purposes and legal bases

| Purpose | Data used | Legal basis | Required or optional |
| --- | --- | --- | --- |
| `[REPLACE: what the visitor asks for]` | `[REPLACE]` | `[REPLACE: exact provision and reasoning]` | `[REPLACE]` |
| `[REPLACE: the action that touches a third party]` | `[REPLACE]` | `[REPLACE]` | `[REPLACE]` |
| Operating and securing the service | `[REPLACE: verified log fields]` | `[REPLACE]` | `[REPLACE]` |

Do not use consent as a generic fallback. Assess the third-party contact
separately from the visitor's own use — they are different processings with
different people affected.

## 4. Storage — the block that the mode decides

### 4a. If `local`

The database is a file on this machine. `[REPLACE: retention schedule per
record type, and the code that implements it.]`

### 4b. If `huckepack-gift` or `huckepack-only-host`

> We keep no database of what you do here. `[REPLACE: name the records]` are
> stored by your browser on your device. While you use the service, a copy is
> held in this server's working memory so that the same queries can run; it is
> discarded at the latest `[REPLACE: the actual TTL from the code]` after your
> last request, when you delete your data, and when the server restarts. No
> file is written on the server.
>
> Deleting your browser data deletes everything, and we cannot restore it —
> there is no copy here. Use the backup function. `[REPLACE: say what the
> backup file contains. If it holds phone numbers, addresses or anything else
> that identifies people, say that plainly: it is an unencrypted copy.]`

`[REPLACE: server, proxy and infrastructure logs exist regardless of where the
database is. Describe them here after checking the deployment.]`

## 5. What your browser stores

| Name | Purpose | Lifetime |
| --- | --- | --- |
| `[REPLACE: language cookie]` | Interface language | `[REPLACE]` |
| `huckepack.session` (local storage) | Addresses your working copy on the server | Until you delete your data |
| `huckepack` (IndexedDB) | **Your data**, and the receipt folder you chose | Until you delete it |
| `huckepack.calle-key` (local storage) | *Only in `only-host`:* your own API key | Until you press "forget" |
| `[REPLACE: anything else — check, do not assume]` | | |

Under `[REPLACE: the applicable implementation of Article 5(3) ePrivacy
Directive — in Germany § 25 TDDDG]`, storing on a user's device needs consent
unless it is strictly necessary for a service the user explicitly requested.
`[REPLACE: assess each row. "It is the user's own data" is an argument worth
making and not a finding — have it reviewed.]`

## 6. Recipients and transfers

| Recipient | Data and purpose | Role and location | Safeguard |
| --- | --- | --- | --- |
| `[REPLACE: the provider that performs the action]` | `[REPLACE]` | `[REPLACE: verified entity and countries]` | `[REPLACE: processing agreement; transfer mechanism if needed]` |
| `[REPLACE: hosting]` | `[REPLACE]` | `[REPLACE]` | `[REPLACE]` |
| `[REPLACE: anything the browser fetches from a third party]` | `[REPLACE]` | `[REPLACE]` | `[REPLACE]` |

An endpoint name proves nothing about the company behind it, its retention or
its subprocessors. Verify from contracts.

## 7. If the visitor brings their own key (`only-host`)

> You enter your own key. It stays in your browser, is shown only by its last
> four characters, and is sent to this server with a request so the action can
> be performed in your name. This server does not store it, does not log it and
> does not keep it afterwards. `[REPLACE: what is billed to whom.]`

`[REPLACE: who is controller for those actions? Passing a key through does not
settle the question by itself.]`

## 8. Information for the people you contact

`[REPLACE: Articles 13/14 analysis. Where data about a person were not obtained
from that person, the controller must inform them. State what is said during
the contact, and where the full notice is available.]`

**This section does not shrink with the mode.** It is usually the longest one.

## 9. Automated decisions

`[REPLACE: describe any ranking, selection or acceptance logic and its effects;
state whether a decision within Article 22 GDPR is made. Do not claim it is
inapplicable without review.]`

## 10. Rights — and the honest complication

Individuals may have rights of access, rectification, erasure, restriction,
objection and portability. Requests: `[REPLACE: channel and identity check]`.
Supervisory authority: `[REPLACE: name, address, URL]`.

**Where the operator holds no copy, the operator cannot look anything up.**
That is the price of the pattern, and it lands on the people who were
contacted, not on the visitor. `[REPLACE: describe who they turn to and how
that person is reached. "Not applicable" is not an answer — a right nobody can
exercise is a problem to solve.]`

## 11. Changes

`[REPLACE: how updates are announced and where previous versions live.]`

## Checklist before publishing

- [ ] Every placeholder replaced or removed; only the matching mode block left.
- [ ] Controller and processor roles documented, not assumed.
- [ ] Legal basis for the third-party contact assessed separately.
- [ ] Provider entity, location, retention, subprocessors and transfer safeguards verified.
- [ ] **Checked on the running installation** that no database file appears in a piggyback mode.
- [ ] In `only-host`: the key is nowhere in logs, storage or responses.
- [ ] Device-storage consent assessed per row of section 5.
- [ ] Written down how a contacted person exercises their rights.
- [ ] Reviewed by a qualified lawyer.
