# Test plan: <feature> (beeper/line#<issue>)

**Goal:** <the feature in one or two sentences>

## Scope

Copy what the LINE Chrome Extension does, nothing extra. Anything the extension cannot do is out of scope; write down that it cannot.

## Platforms

- Chrome extension (LINE Chrome Extension <version>)
- Beeper Desktop
- Beeper mobile
- LINE iOS
- LINE Android

Use a test chat. Every change may post a notice that all members see.

## Test data

Every dummy string used in the tests. `line-evidence` treats these as safe text.

- `<group name>`
- `<message text>`
- `<sample file labels, from samples/MANIFEST.txt>`

## Run order

LINE allows one Chrome Extension session, so the capture logs the bridge out.

1. `before`: Beeper, bridge logged in: <sections>
2. `capture`: log the bridge out, start `line-capture`, then: <sections>. Quit Chrome when done.
3. `after`: deploy, log the bridge in again: <sections>

**Pacing:** wait about 10 s between steps (about 15 s after a step on another device). Write what happened in the **Result** column: ✅ worked, ❌ rejected (copy the error text), `n/a` with the reason, plus notes.

## A. Beeper baseline today

| # | Platform | Phase | Action | Checks | Evidence | Result |
|---|----------|-------|--------|--------|----------|--------|
| A1 | Beeper Desktop | before | <action> | <what this shows> | shot: <screen> | |

## B. Sending from Chrome

| # | Platform | Phase | Action | Checks | Evidence | Result |
|---|----------|-------|--------|--------|----------|--------|
| B1 | Chrome extension | capture | <action> | <call, fields, flags> | shot: <screen>; req: <method> | |

## C. Changes made on another device

Keep the extension open on the test chat. Make each change in the LINE app on your phone, then wait about 15 s. This is what the bridge receives.

| # | Platform | Phase | Action | Checks | Evidence | Result |
|---|----------|-------|--------|--------|----------|--------|
| C1 | LINE iOS | capture | <action> | <event type and fields> | shot: Chrome shows it; req: <operation> | |

## D. Edge cases

| # | Platform | Phase | Action | Checks | Evidence | Result |
|---|----------|-------|--------|--------|----------|--------|
| D1 | Chrome extension | capture | <empty input> | blocked in the UI or by the server? | shot: <screen> | |

## E. Beeper after deploy

| # | Platform | Phase | Action | Checks | Evidence | Result |
|---|----------|-------|--------|--------|----------|--------|
| E1 | Beeper Desktop | after | <same as A1> | matches Chrome | shot: Beeper; shot: LINE shows it | |

## Findings

[FINDINGS.md](FINDINGS.md) (written by the agent in the analyze phase, after `line-analyze` parses the capture).
