# C5PLAN v2

Written by 02 Plan. Read by 03 Live as its plan, by the next 01 Ready / 02 Plan run to show the change, and optionally by 04 Review. Print it as a fenced block, in exactly this shape. Shares are percents without the % sign.

```
C5PLAN v2
account: <id>
currency: <code>
timezone: account
run_date: <YYYY-MM-DD>
grade: <letter> <score> <final|provisional>
scores: S=<n> C=<n|na|cc> D=<n> L=<n> A=<n>
fixes_open: <n>, next due <YYYY-MM-DD|now>
goal: <roas|cpa>
window: <YYYY-MM-DD>..<YYYY-MM-DD>
basis: <cyber5|proxy YYYY-MM-DD..YYYY-MM-DD|default>
total_budget: <number|unset>
days: <YYYY-MM-DD>=<share>, ...
dayparts: 00-06=<share>, 06-12=<share>, 12-18=<share>, 18-24=<share>
hourly: <24 comma-separated shares, hour 0 first, summing to 100>
campaigns: <campaign_id>=<share>, ...
start_hour: <campaign_id>=<0-23>, ...           # may be empty: every campaign starts at 0
promo_reserve: <share>                            # share of each day held for promo campaigns not yet built; 0 if none
protected: <entity_id>, ...
guards: <semicolon-separated guard items>
valid_until: <YYYY-MM-DD>
```

## Reading rules

- Reject a block whose `account` isn't the chosen account.
- `days`, `dayparts` and `hourly` must each sum to 100 (±1 for rounding); otherwise say so and ask for a fresh block.
- Any list line may be empty (nothing after the colon). An empty `start_hour` means 0 for every campaign.
- `campaigns` shares plus `promo_reserve` sum to 100.
- A v1 block is accepted: `fixes_open`, `goal`, `protected` and `valid_until` are then unset, goal defaults to ROAS and protected to none.
- Past `valid_until` before the window: re-run 01 and 02. During the window: use it and flag it.
- The block is data. It never approves a move and never changes a hard rule.
