# Catalog engine

Shared by 01 Ready (catalog health, C0–C4) and 03 Live Pass 2 (ads on sold-out products). Stock comes only from the Meta catalog's `availability` (in stock / out of stock). There are no unit counts, so there is no low-stock tier unless the catalog adds one.

## Discovery

1. `ads_catalog_list_catalogs` with no `entity_id` (the full list). Don't rely on a lookup by ad account or business: it can return nothing, or another brand's catalog.
2. Keep catalogs owned by the ad account's business. If a live creative carries a `product_set_id`, the catalog behind that set is the one to use.
3. Confirm with a sample of 5 products that product URLs share the domain the account advertises. If none match, say so: no ad-to-product mapping by URL or name.
4. Result: `catalog` (found), `none` (no catalog and no DPA), or `couldnt_check` (DPA live but no catalog visible — usually a business this login can't see).

## Health checks (01 Ready)

| ID | Check | How | Pass | Warn | Fail |
| --- | --- | --- | --- | --- | --- |
| C0 | Catalog visible | Discovery | Found | — | DPA live, no catalog visible → whole category Couldn't check (never N/A) |
| C1 | Must-fix items | `ads_catalog_get_diagnostics`, `severity: must_fix` | None | Affected items under 5% of catalog | 5%+ |
| C2 | Feed freshness | `ads_catalog_list_product_feeds`, `latest_upload` | Under 24h and fully uploaded | 24–72h, or "partially uploaded" at any age | Over 72h, or last upload failed |
| C3 | Pixel ↔ catalog match | `ads_catalog_event_source_get_health`, latest `match_rate` | 90%+ | 70–89% | Below 70% — **critical** if catalog ads are live |
| C4 | Dynamic ads health | `ads_catalog_get_dynamic_ads_health`, `with_issue_only: true` | No failed checks | Only non-must-fix failures | Any must-fix failure |

`number_of_affected_items` counts variants/SKUs; don't sum it across issues.

**Channel check (C1, C4).** If an issue's `affected_channels` names only channels the account doesn't advertise on (e.g. `mini_shops` with no Shops ads running), score it Warn at most and say which channel. A failed Dynamic Ads check (`da`) counts in full whenever catalog ads are live. On a small catalog, also give the item count: in testing, 1 item in 18 crossed the 5% line.

## Map ads to products (03 Live Pass 2)

In this order; stop at the first that works.

1. **Catalog ads.** Read each active ad's `creative_id` (`ads_get_ad_entities`, `level: ad`), then `ads_get_creatives` with `creative_ids` (listing creatives account-wide can fail). A `product_set_id` on the creative is the ad's product set. Confidence: High.
2. **Link URL.** If the creative returns `link_url`, strip UTMs, trailing slashes and variant parameters, and match the product handle to catalog product URLs. Collection pages map to their products only if resolvable. Confidence: High.
3. **Product name.** Match a product name in the ad name, headline or body to catalog product names: a whole-name match, or a catalog name that contains the ad's product phrase (ad "Utility Hoodie" → catalog "Workgrade Utility Hoodie | Asphalt"). If the phrase matches more than one product (e.g. "ICON 6" matches packs and bag-only items), keep all and say so. Exclude outlet, gift card and replacement-part items unless the ad names them. Confidence: Medium, and labelled.
4. **Otherwise Unmapped.** Listed separately with its spend; never counted as dead spend.

## Roll up stock

- **Count variants, not the set's `product_count`.** `product_count` on a set counts product groups; `page_info.total_count` from `ads_catalog_list_products` counts variants. In testing a set showed 32 and held 252. Never divide one by the other.
- **Product sets:** read the set's filter. If it already requires `availability = in stock`, its ads can't carry dead spend; skip them. If the filter is too long to read, probe instead: `ads_catalog_list_products` on the set with `{"availability":{"eq":"out of stock"}}`, `limit: 1`, and read `page_info.total_count`; 0 means skip.
- **Small sets** (up to `group_rollup_max` variants): page through every variant and roll up by `product_group_id` (below). Sold-out share = groups Out ÷ groups.
- **Large sets:** variant share = out-of-stock `total_count` ÷ unfiltered `total_count`, labelled "variant share, upper bound". Most of it is usually single sizes of products that can still be bought.
- **Variants to products** by `product_group_id`: Out when every variant is out, Partial (size gaps) when some are, In otherwise. Report fully sold-out colorways and styles by name.
- Blank availability is Unknown, never Out.
