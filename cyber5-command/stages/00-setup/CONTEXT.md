# 00 Setup

Runs before every stage. Stops with a plain message if the account can't be used.

## Inputs

| Input | Required | Default |
| --- | --- | --- |
| Ad account | Yes | Ask; list with `ads_get_ad_accounts` if not given |
| Goal metric | No | Purchase ROAS; purchase CPA if the user says so |
| Planned Cyber5 budget | No | From a pasted C5PLAN, else unset |
| Protected entities | No | From a pasted C5PLAN, else none |
| Funnel roles | No | The user's naming convention ("ACQ = acquisition, RTG = remarketing, RET = retention"), else `role_tokens`; from a pasted C5PLAN `roles` line if present |
| Role targets | No | Share per role ("acquisition 60%, remarketing 25%, retention 15%"), else `role_shares`. Shares of the plan left after `promo_reserve`, summing to 100 or less; Unassigned campaigns keep the remainder |
| Pasted C5PLAN / C5LOG | No | Parsed with `contracts/` |

## Loads

`config/tuned-values.md`. `shared/catalog-engine.md` only if the stage needs a catalog (01 Catalog, 03 Pass 2).

## Process

1. **Account gate.** `ads_get_ad_accounts`. Stop if `is_ads_mcp_enabled` or `is_queryable` is false, and show Meta's reason. Keep `account_status`, `has_payment_method` and `currency`. Hourly breakdowns are already in account time; there is no timezone field.
2. **Context.** `ads_insights_advertiser_context` (last 30 days): one line on vertical and funnel. Not scored.
3. **Key campaigns.** `ads_get_ad_entities`, `level: campaign`, `campaign.effective_status IN [ACTIVE]`, `sort: amount_spent_descending`, `date_preset: last_30d`. Take from the top until they cover `key_campaign_coverage` of spend. Leave out campaigns with no spend in the last 3 days (finished promos can stay "active").
4. **Key ad sets.** `ads_get_ad_entities`, `level: adset`, active, sorted by spend, `date_preset: last_7d`, fields `id, name, amount_spent, results, learning_stage_info, daily_budget, last_sig_edit_ts`, limit `key_adset_limit`. Mark DPA / catalog ad sets (name contains DPA or catalog, or the creative has a `product_set_id`).
5. **Structure.** For key campaigns and ad sets: budgets (daily or lifetime), bid strategy, attribution (from `learning_stage_info.attribution_windows` on ad sets), `promoted_object`, start and stop times. Budget lives where it is set: campaign under CBO or Advantage+, ad set under ABO. Every later budget proposal targets that level only.
5a. **Funnel roles.** Give every active campaign with spend in the last 30 days, and every campaign with spend in the replay or review window the stage uses, one role: Acquisition, Remarketing, Retention, or Unassigned. Use the user's convention first, then `role_tokens`; if a name matches more than one role, or none, it is Unassigned. Never guess from performance. List the assignments in the caveats with the token that matched, so the user can correct them in one line.
6. **Catalog discovery** (only if needed): the discovery rule in `shared/catalog-engine.md`.
7. **Parse pasted blocks and handoff files.** Validate against `contracts/`. A block for another account is rejected with a message. A C5PLAN past `valid_until` is used but flagged.

## Freshness

Data pulled earlier in the same session can be reused if it is recent enough:

| Data | Reuse for |
| --- | --- |
| Signal (S1–S5), feed status (C2), errors (D2), today's spend, stock | Never; pull again every run |
| Ready checks other than those | 6 hours |
| Last year's window, the pre-season baseline, campaign history | The whole session |

Say which data was reused and when it was pulled, in the caveats.

## Outputs

An in-memory setup record: account, currency, goal, funnel roles and role targets, key campaigns, key ad sets, structure, catalog (or none, or Couldn't check), parsed blocks. Nothing is shown to the user except a stop message.

## Never

- Make account-wide error or status calls. They return years of paused entities and overflow. Always pass key campaign IDs.
- Sum across currencies.
