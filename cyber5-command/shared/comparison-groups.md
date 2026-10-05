# Comparison groups

Shared by 03 Live (efficiency status, donors and receivers) and 04 Review (the same passes on a past window).

1. Take attribution from the API (`learning_stage_info.attribution_windows` on the ad set), never from the entity name: in testing, names said "7DC1DE" where the API said 7-day click, and "7DC" where it said 7-day click + 1-day view. Group budget-holding entities by that attribution and funnel stage (prospecting vs retargeting). Never compare across groups.
2. Exclude custom attribution; it isn't comparable.
3. Skip a group with fewer than `min_group_size` members and name it on the watch list.
4. Efficiency uses the goal metric (ROAS or CPA) on the window so far, at the entity's own attribution setting, leaving out hours with spend under `min_hourly_spend`.
5. Bands against the group median: Inefficient worse than `efficiency_band_low` × median, Efficient better than `efficiency_band_high` × median, Marginal between. For CPA, "better" means lower.
6. Every efficiency figure shown to the user carries its attribution setting.
