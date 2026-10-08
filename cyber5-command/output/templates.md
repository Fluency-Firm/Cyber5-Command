# Output templates

Every stage opens with one line naming the stage and why it was picked. Plain words, numbers with units, account currency, account timezone. Everything in chat.

## Ready

1. **Grade banner** — letter, score, Provisional if applicable, days until the window, the single most urgent fix.
2. **Category scorecard** — one row per category: score, status, the evidence in numbers.
3. **Fix list** — do-by, fix, evidence, owner, effort; sorted by do-by.
4. **Change since last run** — only if a C5PLAN was pasted.
5. **Meta's own suggestions** — opportunity score and top 3, marked "not part of the grade".

## Plan

1. **Replay** — basis, day table, heatmap, findings.
2. **Game plan** — day shares, daypart shares, budget guard, creative plan, per-campaign plan grouped by funnel role with role subtotals (dollars if budgeted, else shares), and the budget change schedule (campaign, change, lands at, enter by).
3. **Updated fix list** — with budget-guard items.
4. **C5PLAN v2 block** — then: "Paste this into your first Cyber5 check-in."

## Live

1. **Headline strip** — any Stalled or Not started entity first, then plan total, spent so far, projected finish (range on peak days before 18:00), spend at risk ($ and %), money proposed to move, proposals awaiting approval, any pass skipped and why.
2. **Burn-down** — plan vs actual by hour, rolled up and for the top campaigns, dead spend shaded, today's finish as a range.
3. **Move list** — number, action, from, to (with roles), amount per day, reason, enter by, status. Ends with the approval question. Manual items are listed after it, under "For a person to do".
4. **Watch list** — Unstable entities, Unmapped ads with spend, Medium-confidence matches, sold-out colorways on live ads, entities in cool-down with the time it ends, receivers rechecked from last check-in.
5. **Caveats** — attribution settings in play, failed tools, any tuned value that differs from default.
6. **C5LOG v1 block** — then: "Paste this into your next check-in."

## Morning report (scheduled)

Written for the buyer's first look of the day. One screen, in this order:

1. **Overnight** — anything Stalled or Not started since midnight, with the hour it went dark and whether it came back. "Nothing stalled overnight" when clean.
2. **Yesterday** — each campaign's finish vs plan (rolled up by role), purchases and goal metric with its attribution, and anything worth flagging: cap-outs, sold-out spend, campaigns well ahead or behind, an Unstable entity. Then window spend to date vs the Cyber5 total.
3. **Today** — today's plan by role, pace so far, and **today's proposed changes**: ranked, each with the reason tied to yesterday ("finished 18% behind plan at the best CPA in its group"), amount, and enter-by time. Proposals only; end with "Open a chat and paste the C5LOG to approve any of these."
4. **For a person to do** — Manual items (creative swaps, store-synced product sets) and open fix-list items due today.
5. **Client update (draft)** — see below, when `client_update` is on.
6. **C5LOG v1 block** — every move Proposed.

The overnight watch posts only its headline line and the entities flagged.

## Client update (draft)

A short message for the client's point of contact, in Slack or email form, built from the morning report. It is a **draft for the buyer to forward**, delivered with the buyer's report and never sent to the client by the skill.

- 3–5 lines plus an optional subject line: yesterday's headline (spend vs plan, purchases, and the metrics in `client_metrics`), what's planned for today, and anything the client needs to do (confirm restock timing, approve a creative, fix billing). Then "Next update tomorrow morning."
- Same numbers as the buyer report, rounded the same way. It adds no findings, forecasts or advice the report doesn't show.
- Leaves out proposed budget moves, efficiency bands and rankings, comparison groups, internal tasks, the skill's caveats and tool failures. Keeps the attribution setting next to any ROAS or CPA.
- Written in `client_tone`. No agency or client branding beyond the client's name in the greeting, if the buyer's prompt gives it.
- If yesterday had a delivery problem the client must know about (a billing failure, an outage), say it plainly with when it was caught and whether delivery recovered; never name a cause the activity log doesn't show.

## Review

1. **Scorecard** — pace breaks caught, finish error by hour, dollars that would have moved, dead spend found.
2. **Timeline** — one row per clock step: what each pass flagged and what would have moved.
3. **Burn-down** — as Live, over the whole window.
4. **Post-mortem** — only if C5LOGs were pasted.
5. **Caveats** — the stock caveat on every Pass 2 figure, how budgets were rebuilt, attribution.

## Heatmap

Day × hour grid of purchases (rows = days, columns = hours 0–23), shaded by share of the day's purchases, with delivery-gap hours outlined. Render as a code-block grid or table in chat; an agency may render it as an image in its own wrapper.

## Burn-down

Cumulative plan vs cumulative actual spend by hour. In chat, a table by hour for today plus a compact text sparkline; the numbers in the table are the source of truth.
