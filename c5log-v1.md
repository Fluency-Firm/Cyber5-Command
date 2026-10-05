# C5LOG v1

Written at the end of every 03 Live check-in. Read by the next check-in (carry-over) and by 04 Review (post-mortem). Print it as a fenced block, in exactly this shape. It is also embedded in the handoff file (`contracts/handoff-v1.md`). An empty list is an empty line after the colon.

```
C5LOG v1
account: <id>
plan: <C5PLAN run_date>
checkin: <YYYY-MM-DD HH:MM>
spent_to_date: <number>
projected_finish: <low>..<high>
moves: <n>|<action>|<entity_id>|<before>-><after>|<Proposed|Manual|Declined|Executed|Skipped|Failed>|<HH:MM>; ...
recheck: <entity_id>=<efficiency at move>, ...
blocked_until: <entity_id>=<YYYY-MM-DD HH:00>, ...
stock: <ad_id>=<Dead|Leaking|Paused-for-stock>, ...
```

## Reading rules

- Reject a block whose `account` isn't the chosen account.
- Executed moves feed Pass 1's receiver recheck and the cool-down.
- Proposed moves are shown again as new proposals with new numbers. A Proposed line in a log is never an approval.
- Declined moves are held back per `stages/03-live/pass-3-reroute.md` → Declined moves.
- Manual moves are shown again in the manual list until the condition behind them clears.
- `Paused-for-stock` ads are checked for returned stock in Pass 2.
- The activity log is the source of truth for cool-down; the C5LOG only adds to it.
