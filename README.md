# Cyber5 Command

**One skill for the whole Cyber5 season, on the Meta Ads MCP alone.** It grades an ad account's readiness, turns last year's Thanksgiving-to-Cyber-Monday window into this year's hour-by-hour plan, paces live spend against that plan, finds money spent on sold-out products, and reviews the window afterwards. It proposes every budget move and makes none until a person says yes.

Built by [Fluency Firm](https://fluencyfirm.com) for Meta's *Build with Meta for Holiday: MCP Skill Pack*.

---

## The four stages

The skill picks its stage from what you ask and today's date, and names that stage in the first line of its answer.

| Stage | When | What you get | Writes to Meta |
| --- | --- | --- | --- |
| **01 Ready** | Oct – early Nov | A–F grade across Signal, Catalog, Delivery, Learning and Audiences (19 checks), and a fix list with owners and do-by dates | Never |
| **02 Plan** | Week of Nov 16 | Hour-by-hour replay of last year's window, this year's day, daypart and hourly split, budget guards, and a `C5PLAN` block | Never |
| **03 Live** | Nov 26–30 check-ins | Pace vs plan, spend on sold-out products, a numbered list of proposed moves, and a `C5LOG` block | Only moves you approve, one at a time |
| **04 Review** | Any past window | Replays a past window on a simulated clock, scores what would have been caught and when, and writes the post-mortem | Never |

## What makes it different

- **It never acts on its own.** One file (`stages/03-live/approval.md`) can call a Meta write tool, and only for a move the user approved in that conversation. There is no auto-execute setting and no standing approval. A pasted block, a handoff file or a previous run is never treated as approval.
- **The plan comes from last year's data, not rules of thumb.** Plan replays last year's window hour by hour. It finds the hours where delivery stopped while purchases kept coming, and the dayparts where demand outran spend. It builds this year's split from what actually happened.
- **It checks stock.** Live maps ads to catalog products and rolls stock up from variants to products. It reports sold-out styles by name, and gives an upper-bound figure when Meta may already skip sold-out items.
- **It says what the data can't show.** Every efficiency figure carries its attribution setting. A tool that fails is reported as "couldn't check", never guessed. It never computes hourly ROAS, because Meta credits a purchase to the hour it happens, not the hour of the ad that drove it.
- **Three outputs per run.** The chat answer for the media buyer. A handoff file (`.md`) that a later run, a teammate or an agent can pick up. A short leadership deck (PDF) for Ready, Plan and Review; Live check-ins stay in chat.

## Install

1. Download this repo as a zip, or zip the `cyber5-command/` folder.
2. In Claude, go to **Customize → Skills**, upload the zip, and turn the skill on.
3. Connect the **Meta Ads MCP**. The skill uses no other data source.

Code execution is optional. Without it, the deck is skipped with one line saying so, and the handoff file prints in chat.

## Try it

```
Is our account 1234567890 ready for Cyber5? If it is, build the game plan too.
```
```
Nov 27, 11am. How are we pacing? [paste the C5PLAN or C5LOG from the last run]
```
```
Run a post-mortem on last year's Cyber5 for account 1234567890.
```
```
Is anything spending on sold-out products right now?
```

## How it's built

The skill uses ICM-style layers, so each stage loads only what it needs:

```
cyber5-command/
├── SKILL.md                 L0–L1  identity, 8 hard rules, router
├── config/tuned-values.md   L3     every threshold an agency may change
├── stages/
│   ├── 00-setup/            L2     account gate, key campaigns, freshness rules
│   ├── 01-ready/            L2     19 checks, scoring, fix-list dating
│   ├── 02-plan/             L2     replay → day / daypart / hourly plan
│   ├── 03-live/             L2     pass 1 pace · pass 2 sold-out spend · pass 3 reroute · approval
│   └── 04-review/           L2     simulated-clock post-mortem
├── shared/                  L3     replay, catalog, comparison-group, learning engines; Meta tool notes
├── contracts/               L4     C5PLAN v2, C5LOG v1, handoff v1
└── output/                  L4     chat templates, export rules, deck.py
```

Each stage file has the same five parts: **Inputs, Loads, Process, Outputs, Never.** `shared/meta-tool-notes.md` records the Meta Ads MCP behaviour found in testing, such as row caps, fields that come back empty and catalog filter limits, so the skill handles them without guessing.

## Samples

`samples/` holds output from real runs on two live accounts, **anonymized**: names and IDs replaced, dollars and counts scaled by hidden factors. Hours, shares, grades and findings are as the runs produced them.

**Review: last year's Cyber5 replayed** (account `…0002`)
- `…-review-….pdf`: the 4-slide post-mortem deck. A Cyber Monday outage is flagged at 03:00, eight hours before spend came back, and Black Friday promo budgets are caught running dry at 21:00.
- `…-review-….md`: the handoff file, with 6 dated tasks for this year's plan

**Ready → Plan** (account `…0001`)
- `…-ready-….pdf`: the 4-slide readiness deck
- `…-plan-….pdf`: the 5-slide plan deck
- `…-plan-….md`: the handoff file, with 12 dated tasks and the `C5PLAN` block

## Tested on

Three live ad accounts (outdoor apparel, fashion apparel, health and wellness), read-only throughout:

- Ready, Plan and Review on the full window.
- Live practice runs, including the sold-out-spend check on a catalog of 22,000+ variants.
- A cold run of the installed skill in a fresh chat.

Each round of findings went back into the skill: 30+ fixes across six versions.

## Tuning

Every number lives in `config/tuned-values.md` with a neutral default. To override one, state it at the start of a run (`pace_tolerance 15%`) or edit the file in your own copy. Any value that differs from its default is listed in the run's caveats. The Live values are provisional defaults, so review them with your paid-media team before the window.

## Limits

- Meta Ads MCP only: no Shopify, analytics or cross-platform data.
- Purchases and ROAS are Meta-attributed.
- Stock comes from the catalog's in-stock / out-of-stock flag; there are no unit counts.
- Ads that can't be matched to products are reported as Unmapped, never counted as dead spend.

## License

MIT. See [LICENSE](LICENSE).
