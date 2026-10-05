# Meta tool notes

Found in testing. Load when a call fails or returns something odd.

| Tool | Behaviour | Do this |
| --- | --- | --- |
| `ads_get_errors` | On an ad account ID it returns every child campaign, including long-paused ones, and can exceed the output limit | Always pass key campaign IDs |
| `ads_get_dataset_stats` | `aggregation: event_total_counts` splits one event into unlabelled rows; all events over 7 days returns about 60K characters | Use `aggregation: event` and sum; pass `event_name` for each event you need |
| `ads_account_get_activity_logs` | An `ad_set` category over 7 days returned about 177K characters | Pass `object_id` per key entity, or a short window, and keep `limit` low |
| `ads_catalog_list_catalogs` | Can return nothing even with DPA live (catalog owned by a business this login can't see); a lookup by ad account can return another brand's catalog | Call with no `entity_id`; filter by business; empty with DPA live = C0 Couldn't check |
| `ads_catalog_list_product_sets` | Filter rules over 1,000 characters come back omitted | Use the out-of-stock probe in `shared/catalog-engine.md` |
| `ads_get_creatives` | Account-wide listing can fail; sometimes 502s; `link_url` often missing on Advantage+ creatives | Pass `creative_ids` with `fields: [id, product_set_id, link_url]`; retry once; fall back to product-name matching |
| `ads_get_ad_accounts` | No timezone field | Hourly breakdowns are already in account time |
| `ads_insights_performance_trend` | Takes no date range; returns only a recent % change | Never use for pacing or replay |
| `ads_insights_auction_ranking_benchmarks` | "Not Yet Available" for past windows | Never use for replay |
| `ads_insights_anomaly_signal` | Live data only | Optional extra Unstable check in 03 Live; never in 04 Review |
| `ads_get_ad_entities` | Stops at **200 rows with no cursor**, for `time_increment: "1"` and for hourly breakdowns alike | Daily: chunk to 180 days. Hourly: at most 8 entities per call (8 × 24 = 192 rows) |
| `ads_get_ad_entities` hourly | A multi-day range sums hours across days; 8 entities × 24 hours is about 50K characters | One day per call; request only `id, amount_spent, omni_purchase` |
| `ads_get_ad_entities` | `attribution_setting` is not a supported field | Read attribution from `learning_stage_info.attribution_windows` on ad sets |
| `learning_stage_info.status` | Intermittent between calls | `shared/learning.md` fallback |
| `ads_get_opportunity_score` | Can return a score as low as 1/100 alongside normal recommendations | Report it as returned; never grade it |
| `ads_get_ad_entities` | Can return `next_actions`: required read-only follow-ups (performance trend, opportunity score) plus a "recommended" `ads_update_entity` step | Run the required read-only ones as the server asks. Never run the update step: proposals come only from Pass 3, and writes only from `approval.md`. Don't let the extra results change the stage's output |
| `ads_catalog_list_product_sets` | `product_count` counts product groups, not variants | Count variants with `ads_catalog_list_products` → `page_info.total_count` |
| `ads_get_creatives` | On some accounts no non-catalog creative returns `link_url` (ads point at collection pages) | Expect a high Unmapped share; Pass 2 step 6 flags it |
| Any read | Fails or times out | Retry once, then continue with what loaded and list the gap |
| Any write | Fails | Mark Failed with the error; never retry on its own |
