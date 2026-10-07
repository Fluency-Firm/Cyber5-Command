# Tuned values

Every number an agency may change lives here. The submitted skill ships with these neutral defaults and no client names, IDs or tuned values. An agency overrides a value by stating it at the start of a run ("pace_tolerance 15%") or by editing this file in its own copy. Any value used in a run that differs from the default is listed in the output's caveats.

## Season

| Name | Default | Used by |
| --- | --- | --- |
| `window` | Thanksgiving (4th Thursday of November) through the following Monday, account timezone | Router, 02, 03, 04 |
| `last_year_window` | The same days last year (2025: Nov 27 – Dec 1) | 02, 04 |
| `plan_valid_days` | 7 | C5PLAN `valid_until` |

## 01 Ready — scoring

| Name | Default |
| --- | --- |
| `weight_signal` | 30 |
| `weight_catalog` | 20 |
| `weight_delivery` | 25 |
| `weight_learning` | 10 |
| `weight_audiences` | 15 |
| `grade_bands` | A 90+, B 80–89, C 70–79, D 60–69, F below 60 |
| `critical_cap` | C |
| `points` | Pass 100, Warn 50, Fail 0 |
| `key_campaign_coverage` | 80% of last-30-day spend, max 8 campaigns |
| `key_adset_limit` | 10 |
| `learning_share_pass` / `learning_share_fail` | 35% / 60% of key spend learning or limited (L2) |

Learning carries less weight than the other categories because new sale campaigns and ad sets often stay in learning through a five-day window, and that isn't a failure. Check thresholds (S1–S5, C1–C4, D2–D3, L1–L3, A1–A3) are set in the tables in `stages/01-ready/CONTEXT.md` and may be overridden here by ID, e.g. `S2.pass: 8.5`.

## 01 Ready — do-by dates

| Effort | Do-by |
| --- | --- |
| Days | 21 days before window start |
| Hours | 14 days before |
| Minutes | 7 days before |
| Edit freeze | Starts 7 days before |
| Blocks the grade (C0, failed tool) | Within 2 days of the run |

## 02 Plan

| Name | Default |
| --- | --- |
| `plan_blend` | 0.5 (plan share = halfway between last year's spend share and purchase share) |
| `promo_lift` | 3× the 28-day median purchases |
| `min_cyber5_days` | 3 days of spend in last year's window to use basis `cyber5` |
| `delivery_gap` | An hour under 10% of that day's hourly average spend while purchases continue |
| `daypart_gap` | 5 points |
| `creative_decay` | 30% loss of click-through rate by the last day |
| `default_days` | Thu 15, Fri 30, Sat 12, Sun 13, Mon 30 |
| `default_dayparts` | 00–06 8, 06–12 28, 12–18 36, 18–24 28 |
| `warm_freq_pass` / `warm_freq_fail` | 6 / 10 over five days |
| `value_sanity_roas` | 15× pre-season purchase ROAS |
| `pre_window_ramp` | 2× pre-season daily spend on a day before the window = early sale start |
| `promo_share_flag` | 20% of last year's window spend in campaigns with no spend in the last 30 days = ask about promo campaigns |

## 04 Review

| Name | Default |
| --- | --- |
| `review_steps` | 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00; hourly on peak days |
| `review_plan_basis` | Each entity's average daily spend over the 7 days before the window; window actuals only if it didn't exist then |

## Exports

| Name | Default |
| --- | --- |
| `export_handoff` | on (every stage, every check-in) |
| `export_deck` | on for Ready, Plan and Review; never in Live |
| `deck_brand` | neutral (agency logo, colors and font may be set here) |

## 03 Live

Provisional defaults, confirmed Oct 2 2026 pending review by an agency's paid team.

| Name | Neutral default | Meaning |
| --- | --- | --- |
| `pace_tolerance` | 10% | Ahead / Behind band around plan |
| `efficiency_band_low` | 0.8 | Inefficient below this × group median |
| `efficiency_band_high` | 1.2 | Efficient above this × group median |
| `min_hourly_spend` | 1% of the entity's daily budget | Hours below this are left out of efficiency |
| `max_move_pct_donor` | 20% | Largest cut from one donor's daily budget |
| `max_move_pct_receiver` | 20% | Largest raise to one receiver's daily budget |
| `learning_reset_pct` | 20% | A move this large or larger is flagged as a learning risk |
| `cooldown_hours` | 12 | No move on an entity whose budget changed this recently, by anyone |
| `max_changes_per_entity_per_day` | 2 | |
| `min_group_size` | 3 | Smallest comparison group Live will rank |
| `leak_share_threshold` | 25% | Share of an ad's products fully Out that makes it Leaking |
| `leak_variant_share` | 40% | Where only a variant share is available, the share sold out that makes it Leaking |
| `group_rollup_max` | 300 | Largest set (in variants) paged through for a product-level roll-up |
| `unmapped_flag` | 30% | Share of purchase-goal spend in Unmapped ads that goes in the headline |
| `range_until_hour` | 18 | Before this hour on a peak day, today's finish is shown as a range |
| `finish_range_pct` | 50% | Half-width of that range (Review testing: median finish error was 51% at 09:00, 11% at 18:00) |
| `stall_hours` | 2 | Consecutive near-$0 hours after earlier spend that make an entity Stalled |
| `cap_out_factor` | 1.0 | Today's finish above this × daily budget = early cap-out alert |
| `budget_sanity_factor` | 1.75 | A rebuilt or reported budget below actual daily spend ÷ this is treated as unknown |
| `repropose_change_pct` | 50% | How much a declined move's evidence must change before it is proposed again the same day |
