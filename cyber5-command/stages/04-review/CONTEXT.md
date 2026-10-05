# 04 Review — replay and post-mortem

Runs 03 Live's three passes on a past window as if it were live, stepping a simulated clock through it, and scores what the skill would have caught. It is the proof for reviewers, the demo when no sale is running, and the post-mortem after Cyber Monday. It never calls a write tool and never loads `stages/03-live/approval.md`.

## Inputs

| Input | Required | Default |
| --- | --- | --- |
| Window | No | Last year's Cyber5; after this year's window, this year's; or any past 5 days the user names |
| Plan | No | A pasted C5PLAN; else `review_plan_basis` (each entity's 7-day average before the window). Window actuals only for entities that didn't exist then, and say pacing for those is circular. Say which basis was used |
| C5LOGs | No | This year's logs, to compare what was proposed and done with what the replay finds |
| Clock | No | `review_steps` (03:00 to 21:00 every 3 hours, hourly on peak days); or a single "now" the user names (e.g. day 2, 14:00) |

## Loads

`shared/replay-engine.md`, `stages/03-live/pass-1-pace.md`, `stages/03-live/pass-2-dead-spend.md`, `stages/03-live/pass-3-reroute.md`, `shared/catalog-engine.md`, `shared/comparison-groups.md`, `shared/learning.md`, `contracts/c5log-v1.md`, `contracts/handoff-v1.md`, `output/exports.md`.

## Process

1. **Pull** with `shared/replay-engine.md` (per-campaign daily and hourly, activity log). Reuse 02's pulls if they ran in this session.
2. **Budgets at the time.** Current budgets aren't historical. Rebuild them from budget events in the activity log and check each with Budget sanity in `shared/learning.md`; where none exist or the check fails, say the budget is unknown, pace against the plan only, and size any move against the day's plan as a labelled stand-in.
3. **Step the clock.** At each step, run the three passes using only data up to that hour. Moves are labelled "would have moved", with the same guardrails, cool-down included, and carried to the next step as if executed.
4. **Stock caveat.** The catalog shows only today's stock, so Pass 2 uses current availability. Label every Pass 2 number with this.
5. **Scorecard:** pace breaks caught (entity, status — Not started, Stalled, Behind, cap-out — hour caught, hours before the day ended, purchases still ahead of that hour), false alarms, today's-finish error by hour, dollars the reroute would have moved, dead spend found.
6. **Post-mortem** (when this year's C5LOGs are pasted): moves proposed vs approved vs executed, what the replay would have added, and which receivers held their efficiency.

## Outputs

Scorecard, a timeline of calls by clock step, the burn-down, and caveats (`output/templates.md` → Review), plus the exports in `output/exports.md`. If run before this year's window, end with one line offering 02 Plan.

## Never

- Call a write tool, or load `approval.md`.
- Use `ads_insights_anomaly_signal`; it has no past data.
- Present a "would have moved" figure as money lost; it is a lead, at the stated attribution.
