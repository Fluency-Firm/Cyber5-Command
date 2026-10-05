# Replay engine

Shared by 02 Plan (last year → this year's plan) and 04 Review (simulated check-ins on any past window). One set of pulls serves both; if both run in one session, pull once.

## Pick the window

Try in order and label every output with the basis used:

1. **`cyber5`** — `last_year_window`, if the account spent on at least `min_cyber5_days` of those days. (04 Review may instead use any past 5 days the user names; label it `custom`.)
2. **`proxy`** — the account's biggest promo in the last 12 months:
   - Daily account data (`ads_get_ad_entities`, `level: ad_account`, `time_increment: "1"`, fields `amount_spent, omni_purchase`) in chunks of 180 days or fewer. The tool stops at 200 rows with no cursor.
   - Leave out last year's window ± 7 days.
   - Purchase lift per day = purchases ÷ median purchases of the 28 days before. A promo window is a run of consecutive days at `promo_lift` or more.
   - Pick the window with the most total purchases, not the most spend (a growing account's spend baseline moves too much).
   - Name it with its dates, plus a campaign name if one matches (`level: campaign`, that range, sorted by spend).
3. **`default`** — no usable history. Skip the pulls; 02 uses the default curve.

## Pull

- **Hourly, per day:** `ads_get_ad_entities`, `level: ad_account`, `breakdowns: ["hourly_stats_aggregated_by_advertiser_time_zone"]`, `time_range` = one day, fields `amount_spent, omni_purchase, cpm, impressions`. One call per day; a multi-day range sums hours across days.
- **Per campaign, daily:** the same window at `level: campaign`, `time_increment: "1"`, fields `amount_spent, omni_purchase, purchase_roas, attribution_setting`. Used by 04's pacing and by 02's per-campaign split check.
- **Per campaign, hourly** (04 only): the hourly breakdown at the budget level, one call per day.
- **Pre-season baseline:** daily account data for the 14 days ending 10 days before the window starts (2025: Nov 3–16).
- **Ads:** `level: ad`, the window, `amount_spent_descending`, limit 12, fields `id, name, amount_spent, omni_purchase, ctr, frequency, cpm`. Then the top 8 by `object_ids` with `time_increment: "1"`, from 2 days before the window to its end.
- **Activity log:** `ads_account_get_activity_logs` over the window with `event_category: budget` (04 uses it to rebuild budgets at the time); plus, around any delivery gap, from 12 hours before to its end, once with no category.

If the hourly breakdown fails or is empty, replay at daily grain, drop daypart and hourly outputs, and say so.

## Findings

1. **Day table:** spend, spend vs pre-season daily average, CPM, CPM vs pre-season, share of window spend, share of window purchases.
2. **Delivery gaps:** any hour under `delivery_gap` while purchases continue. Report hours, purchases with no ad support, and the log events around it. Don't claim a cause the log doesn't show.
3. **Demand vs spend by daypart** (00–06, 06–12, 12–18, 18–24, pooled): share of spend vs share of purchases. A gap of `daypart_gap` or more is a finding; name the days it was worst.
4. **Cost peaks:** the highest-CPM hours on the biggest day.
5. **Creative decay:** top ads' click-through rate at peak day vs last day, and cost per purchase. Split sale-launched (launched within 7 days of the window) vs evergreen. Present the comparison as a lead to test, not a verdict: these are Meta-attributed purchases.
6. **Early sale start:** any day in the 7 before the window with spend at `pre_window_ramp` or more × the pre-season daily average. Report the dates and their spend; 02 Plan treats them as part of the sale (in testing, a sale began two days before Thanksgiving at 3.2× normal).
7. **Promo campaigns:** the share of window spend in campaigns with **no spend in the last 30 days**. Never use `effective_status`: in testing, last year's finished BFCM campaigns still reported ACTIVE. Report separately the part in campaigns whose names mark a promo (Promo, BFCM, Black Friday, Cyber, Sale). At `promo_share_flag` or more, 02 Plan must ask about this year's promo campaigns before splitting by campaign.
8. **Value sanity:** pre-season purchase ROAS above `value_sanity_roas` → flag the purchase value setup and hold any ROAS statement.

Render the replay as a **day × hour heatmap** of purchases with delivery-gap hours outlined (`output/templates.md` → Heatmap).
