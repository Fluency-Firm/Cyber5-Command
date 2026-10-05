# 02 Plan — replay and game plan

Turns last year's Cyber5 (or the best stand-in) into this year's day, daypart and hourly pacing, a budget guard, a creative plan and a per-campaign split, and prints the C5PLAN v2 block that 03 Live runs on. Read-only.

## Inputs

The setup record from 00, and the 01 Ready result (run 01 first unless a C5PLAN under `plan_valid_days` old is pasted). Optional: planned Cyber5 budget, campaign budgets, protected entities, per-campaign start hours.

## Loads

`shared/replay-engine.md`, `contracts/c5plan-v2.md`, `contracts/handoff-v1.md`, `output/exports.md`, `shared/meta-tool-notes.md` on failure.

## Process

1. **Replay.** Pick the window, pull and work out the findings with `shared/replay-engine.md`.
2. **Day and daypart shares.** For each day and daypart, plan share = `plan_blend` × last year's spend share + (1 − `plan_blend`) × last year's purchase share, rounded to whole percents summing to 100. Map last year's days to this year's by weekday (Thanksgiving → Thanksgiving). Basis `default`: `default_days` and `default_dayparts`.
3. **Hourly curve.** The same blend per hour (24 values, summing to 100), used by Live's burn-down. Basis `default`: spread each daypart evenly over its hours.
4. **Budget guard** — each that applies becomes a fix with a do-by date, added to 01's fix list:
   - A daypart gap against evening or morning → hold that gap as a reserve for those hours on the days it was worst.
   - Any delivery gap last year → confirm a backup payment method and the account spend limit, and that every ad planned for that day is approved and scheduled from 12am. Do-by: 7 days before the window.
   - Spend ran out before midnight on the biggest days → name the days and the hour.
5. **Creative plan.**
   - Sale-launched ads lost `creative_decay` or more of click-through rate by the last day → plan a second set of sale creatives launched the evening before the last day.
   - Evergreen ads beat sale ads on cost per purchase → keep the top evergreen ads funded all five days, and name them.
6. **Per-campaign split.** If the replay found a promo share at `promo_share_flag` or more, first ask whether promo campaigns are planned this year and what share they get. Without an answer, hold last year's promo-named share as `promo_reserve` and split the rest. Then split each day's remaining share by last-30-day spend share, unless the user gives campaign budgets. Split across **every active campaign with spend in the last 30 days** (the top 10 by spend; the rest pooled as "other"), not only Ready's key campaigns: in testing, the key-campaign cut left out the account's best campaign from last Cyber5. Flag any campaign that beat the window's ROAS last year but gets under 10% this year.
6a. **Early sale start.** If the replay found an early sale start, say so above the day plan and ask whether this year's sale starts early too. If it does, add those days to the plan with last year's share of total spend and re-scale. With a planned budget, show dollars per campaign per day; without one, shares.
7. **Start hours.** Default 0 for every campaign; the user may set a later hour for a planned late launch. Live treats $0 before that hour as Not started.
8. **Warm pool capacity** (feeds 01's A2):
   - Warm ad sets = last year's window ad sets whose name marks retargeting (RTN, RT, retarget, warm, existing customers) or whose targeting includes website or customer audiences. None identified → A2 Couldn't check.
   - Planned warm spend = warm share of last year's window spend × this year's budget (or last year's window spend if unset).
   - Expected frequency = (planned warm spend ÷ last year's warm CPM × 1,000) ÷ lower bound of the 30-day site-visitor pool. Re-score A2 and Audiences.
9. **Emit C5PLAN v2** exactly as `contracts/c5plan-v2.md` specifies.

## Outputs

Replay (basis, day table, heatmap, findings), game plan (day shares, daypart shares, budget guard, creative plan, per-campaign plan), the updated fix list, and the C5PLAN v2 block with the line "Paste this into your first Cyber5 check-in." Rendered with `output/templates.md` → Plan, plus the exports in `output/exports.md`.

## Never

- Call a write tool, or offer to set budgets. The plan is a proposal the user builds in Ads Manager.
- Use hourly ROAS.
- Name a cause for a delivery gap that the activity log doesn't show.
