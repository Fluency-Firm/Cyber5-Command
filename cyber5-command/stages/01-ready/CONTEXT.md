# 01 Ready — readiness grade

Grades the account A to F across five categories. Every lost point becomes a fix with an owner, an effort and a do-by date. Read-only.

## Inputs

The setup record from 00. Optional: a prior C5PLAN (to show the change per category since that run).

## Loads

`shared/catalog-engine.md` (Catalog), `shared/learning.md` (Learning), `contracts/handoff-v1.md`, `output/exports.md`, `shared/meta-tool-notes.md` on failure. For A2, the warm-pool step of `stages/02-plan/CONTEXT.md` if 02 runs in the same session; otherwise A2 is Couldn't check.

## Process

Every check reports Pass / Warn / Fail / Couldn't check with the numbers behind it. A failed tool is retried once, then the check is Couldn't check and left out of the score.

### Signal (pixel / dataset)

Find the dataset with `ads_get_datasets` (`ad_account_id`). With several, grade the one firing Purchase for the key campaigns and list the rest.

| ID | Check | How | Pass | Warn | Fail |
| --- | --- | --- | --- | --- | --- |
| S1 | Purchase recency | `ads_get_dataset_stats`, `event_name: Purchase`, `aggregation: event`, `start_time` = now − 24h (unix seconds) | Purchases in 20+ of 24 hours | 1–19 hours | None in 24h — **critical** |
| S2 | Purchase match quality | `ads_get_dataset_quality`, `query_type: [web]`, Purchase `composite_score` | 8.0+ | 6.0–7.9 | Below 6.0 |
| S3 | Mid-funnel match quality | Same call; lower of AddToCart and InitiateCheckout | 7.0+ | 5.5–6.9 | Below 5.5 |
| S4 | Funnel ratios | `ads_get_dataset_stats`, `aggregation: event`, last 7 days; sum each event across all rows | AddToCart/ViewContent 3–25% and Purchase/AddToCart 5–40% | One ratio outside its band | ViewContent, AddToCart or Purchase missing |
| S5 | Server events | `ads_get_dataset_stats`, `event_name: Purchase`, `event_source: SERVER_ONLY`, last 24h | Server purchases present | Browser only | — |

### Catalog

Run only if a key ad set is DPA / catalog-backed, or discovery found a catalog. Otherwise Catalog is N/A and its weight is re-spread. Checks C0–C4 are defined in `shared/catalog-engine.md` → Health checks.

### Delivery

| ID | Check | How | Pass | Warn | Fail |
| --- | --- | --- | --- | --- | --- |
| D1 | Account can spend | From setup | `ACTIVE` with a payment method | — | Anything else — **critical** |
| D2 | Errors in key campaigns | `ads_get_errors` with key campaign IDs | No blocking errors | Errors on under 10% of key ads | An ad set blocked, or 10%+ of key ads |
| D3 | Disapproved ads | `ads_get_ad_entities`, `level: ad`, `ad.effective_status IN [DISAPPROVED]`, key campaigns | None | 1–2 | 3+, or the top-spend ad |

In D2, deprecated-crop-key and DMA → Comscore notices are informational: list them, don't score them.

### Learning phase

| ID | Check | How | Pass | Warn | Fail |
| --- | --- | --- | --- | --- | --- |
| L1 | Top ad set learning | `learning_stage_info.status` on the top-spend key ad set, else the fallback in `shared/learning.md` | `SUCCESS` | `LEARNING` | `FAIL` (learning limited) |
| L2 | Learning share | Same, across key ad sets, weighted by 7-day spend | Under `learning_share_pass` of key spend learning or limited | `learning_share_pass` to `learning_share_fail` | Over `learning_share_fail` |
| L3 | Recent significant edits | `last_sig_edit_ts`; `ads_account_get_activity_logs` (`event_category: ad_set`, `object_id` = each key ad set, last 7 days). Significant = targeting, optimization event, bid strategy, creative, or a budget change of `learning_reset_pct` or more | None in 7 days | Any, window more than 7 days away | Any inside the 7 days before the window |

Learning is weighted lightly on purpose: sale campaigns launched for the window often never leave learning in five days, and agencies that pause evergreen ads for sale creative will start the window mostly in learning. Read L1–L2 as a pre-window health check, not a verdict on the sale.

### Audiences

`ads_get_ad_account_custom_audiences` with no subtype filter, paged with `next_cursor`. Website and engagement audiences come back as subtype `PLATFORM`; identify them by subtype plus name. Use `approximate_count_lower_bound`.

**Grade what the account uses.** Read the key ad sets' `targeting` field (`ads_get_ad_entities`, `level: adset`, `object_ids` = key ad sets, at most 5 per call). Inside it, `custom_audiences` are audiences the ad set targets and `excluded_custom_audiences` are audiences it excludes. A1 counts targeting only; A3 counts both, since a stale exclusion list matters too. Many agencies run broad or Advantage+ audiences and keep warm pools off on purpose, so a missing or inactive audience that no key ad set uses is a note, not a failure.

| ID | Check | How | Pass | Warn | Fail |
| --- | --- | --- | --- | --- | --- |
| A1 | Warm pools exist | Active 30-day site visitors and 30-day add-to-cart | Both present and active | One missing; or both missing and no key ad set targets warm audiences (or targeting couldn't be read), noted "not used in key campaigns" | Both missing while a key ad set targets warm audiences |
| A2 | Warm pool capacity | From 02 Plan → Warm pool capacity | Expected frequency ≤ `warm_freq_pass` | Up to `warm_freq_fail` | Over `warm_freq_fail` |
| A3 | Stale audiences | `delivery_status: INACTIVE`, "Not maintained", "Custom audience not available" errors in key campaigns (D2) | None in key ad sets' targeting (inactive audiences no key ad set uses are listed as a note, unscored) | A key ad set targets an inactive audience, no error yet | A key campaign has an audience error |

### Scoring

- Category score = average of its scored checks. Couldn't check is left out.
- Overall = weighted average with the weights in config. If Catalog is N/A or Couldn't check, divide by the remaining weights.
- Any **critical** Fail caps the grade at `critical_cap`.
- A whole category Couldn't check makes the grade **Provisional**; say what would make it final.

### Fix list

Every Warn, Fail and Couldn't check becomes one fix. 02 Plan's budget-guard items are added when 02 runs.

| Checks | Owner | Effort |
| --- | --- | --- |
| S1–S5, C3 | Developer | Days |
| C1, C2, C4 | Developer / ecommerce | Hours |
| C0, D1 | Client / business admin | Minutes |
| D2, D3, A1 | Media buyer | Minutes |
| L1, L2, A3 | Media buyer | Hours |
| L3 | Media buyer | Edit freeze |

Do-by dates come from config. Never set one in the past; if it has passed, use "Now". Sort by do-by.

### Meta's own suggestions

`ads_get_opportunity_score`: the score and its top 3 recommendations by points, shown separately and never graded.

### Merged accounts

If C2–C4 show product ID mismatches, the catalog serves several countries, or the user says the account recently merged regions, stores or catalogs, add this caveat: "This account may have merged regions or catalogs recently. Catalog matching and audience checks can read worse than reality until the merge settles; confirm the failing items before fixing them." Grade as normal.

## Outputs

Grade banner, category scorecard, fix list, Meta's suggestions, and (if a prior C5PLAN was pasted) the change per category. Rendered with `output/templates.md` → Ready, plus the exports in `output/exports.md`. If 02 is not running next, offer it in one line.

## Never

- Call a write tool, or offer to make a fix. Fixes are for the user.
- Count Couldn't check as Pass or Fail.
- Grade Meta's opportunity-score items.
