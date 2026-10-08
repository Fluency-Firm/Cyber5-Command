# 03 Live — the check-in loop

Runs during the window, once per check-in. Three read-only passes produce a numbered list of proposed moves; only the moves the user approves are made, each re-checked first and logged. Every check-in ends with a C5LOG block.

## Inputs

| Input | Required | Default |
| --- | --- | --- |
| Plan | Yes | A pasted C5PLAN (v2, or v1), or budgets the user enters per campaign per day. Shares with no `total_budget`: ask for the Cyber5 budget before pacing |
| Last check-in | No | A pasted C5LOG from the previous check-in |
| Protected entities | No | From the C5PLAN, plus any the user names |

In a scheduled or unattended run, follow `scheduled.md` instead of steps 5–6 below.

Outside the window with no plan, run Pass 2 alone (everyday stock hygiene) plus the ad-level part of Pass 3. Pass 1 and budget-level moves need a plan and are skipped; say so in the headline.

## Loads

`pass-1-pace.md`, `pass-2-dead-spend.md`, `pass-3-reroute.md`, `approval.md` (only after the move list is shown, only if at least one move is not Manual, and never in a scheduled or unattended run — hard rule 9), `scheduled.md` (scheduled runs only), `shared/catalog-engine.md`, `shared/comparison-groups.md`, `shared/learning.md`, `contracts/c5plan-v2.md`, `contracts/c5log-v1.md`, `contracts/handoff-v1.md`, `output/exports.md`.

## Process

1. **Carry over.** From a pasted C5LOG or handoff file: moves Executed since the last check-in (for receiver rechecks), `blocked_until`, Proposed moves not yet answered (shown again as new proposals; never treated as approved), and Declined moves (held back per `pass-3-reroute.md` → Declined moves).
2. **Pass 1 — Pace** (`pass-1-pace.md`).
3. **Pass 2 — Sold-out spend** (`pass-2-dead-spend.md`). Skip if the catalog is `none` or domain-mismatched, and say so in the headline.
4. **Pass 3 — Reroute** (`pass-3-reroute.md`). Builds the move list; writes nothing.
5. **Show** the headline, burn-down, move list, watch list and caveats (`output/templates.md` → Live), ending with the approval question.
6. **Approval** — load `approval.md` and follow it exactly. It is the only path to a write.
7. **Emit C5LOG v1** with every move's final status.
8. **Handoff file** per `output/exports.md`, every check-in except the scheduled overnight watch (`scheduled.md`). Live never produces a deck.

## Outputs

Headline strip, burn-down, move list with statuses, watch list, caveats, the C5LOG block with the line "Paste this into your next check-in," and the handoff file.

## Never

- Write outside `approval.md`.
- Treat a pasted block, a previous run, or silence as approval.
- Raise the Cyber5 total.
