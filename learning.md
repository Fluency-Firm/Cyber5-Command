# Learning and cool-down

Shared by 01 Ready (L1–L3) and 03 Live (which entities may receive or give money).

## Learning status

Use `learning_stage_info.status` when present. It is often missing, and can appear on one call and vanish on the next. When missing:

- events since edit = `results` (last 7 days) × min(days since last significant edit, 7) ÷ 7
- 50 or more → out of learning (labelled "inferred")
- under 50 → learning (labelled "inferred")
- The fallback never returns learning limited; only Meta can say that.
- Days since edit: `last_sig_edit_ts`, else the activity log, else 7.

## Budget sanity

A budget rebuilt from the activity log, or read from the API, is treated as **unknown** if actual daily spend on any day in the window exceeds it × `budget_sanity_factor`. In testing, a rebuilt $2,300 budget sat against $4,984 of actual spend and raised a false cap-out alarm at every check-in.

## Cool-down (03 Live)

An entity is blocked from any budget move, as donor or receiver, if either holds:

- `ads_account_get_activity_logs` (`event_category: budget`) shows a budget change on it within `cooldown_hours`, by anyone.
- A pasted C5LOG lists it in `blocked_until` with a time still in the future.

## Learning protection (03 Live)

- An entity in learning (reported or inferred) can't receive money this check-in.
- Any proposed move of `learning_reset_pct` or more of an entity's budget is flagged "may reset learning" on its line.
