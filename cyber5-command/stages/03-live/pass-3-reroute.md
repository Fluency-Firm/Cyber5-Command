# Pass 3 — Reroute proposals

Builds the numbered move list. Writes nothing.

## Ad-level proposals

The budget stays in the ad's ad set, so an ad-level proposal frees no money for elsewhere.

| Ad state (Pass 2) | Converts at or above its ad set (same attribution) | Converts below it |
| --- | --- | --- |
| Dead | Pause | Pause |
| Leaking | Swap to an in-stock colorway or creative (**manual**) | Pause, with the swap offered as the alternative |
| Paused for stock, now back in stock | Re-activate | Re-activate |

A **manual** proposal is one the skill can't carry out (it has no creative-edit tool). It is listed with what to change, never sent to approval, and marked Manual in the log.

**Catalog ads on an unfiltered set** never get a per-ad Pause or Swap. Their stock figure is an upper bound, and in testing one "Leaking" retention ad was the account's best converter. Instead, make **one proposal per set**: add `availability = in stock` to the set's filter. Name every ad seen using the set, and say the change affects any other ad on it. The proposal is Manual if the set is synced from the store (it has a `retailer_id`, or its rule uses `dynamic_retailer_product_set_id`) or its filter can't be read (over 1,000 characters): "add an in-stock condition to this collection where it's managed". Otherwise it is Proposed and goes through `approval.md`.

## Budget-level proposals

Move daily budget from one budget-holding entity (campaign under CBO or Advantage+, ad set under ABO) to another. Only these move money.

### Donors and receivers

- **Donors:** Dead or mostly-Dead entities (whole ad set or campaign), and entities that are Ahead and Inefficient.
- **Receivers:** Behind or On pace, Efficient, not Unstable, not Stalled, not in learning, not Protected, mapped mostly to in-stock products, prospecting stage.
- **Blocked either way:** cool-down (`shared/learning.md`), delivery-blocking errors from `ads_get_errors` (ignore deprecation notices), more than `max_changes_per_entity_per_day` changes today, anything Protected.

### Allocation

1. Pool = cuts from donors, each capped at `max_move_pct_donor` of the donor's daily budget.
2. Rank receivers by efficiency headroom over the group median × room behind pace.
3. Allocate top-down, each receiver capped at `max_move_pct_receiver` of its daily budget. Money left over stays unallocated and is reported, never forced.
4. The sum of raises never exceeds the sum of cuts.
5. Flag any move of `learning_reset_pct` or more as "may reset learning".

## Declined moves

A move the user declined at an earlier check-in (C5LOG status Declined) is not proposed again the same day unless its evidence has changed by `repropose_change_pct` or more (spend at risk, efficiency gap, or pace). When it is proposed again, say what changed.

## Each proposal

One line: number, action, entity name and ID, current value → new value, amount per day, reason, expected effect, and status Proposed or Manual.
