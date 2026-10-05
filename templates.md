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
2. **Game plan** — day shares, daypart shares, budget guard, creative plan, per-campaign plan (dollars if budgeted, else shares).
3. **Updated fix list** — with budget-guard items.
4. **C5PLAN v2 block** — then: "Paste this into your first Cyber5 check-in."

## Live

1. **Headline strip** — any Stalled or Not started entity first, then plan total, spent so far, projected finish (range on peak days before 18:00), spend at risk ($ and %), money proposed to move, proposals awaiting approval, any pass skipped and why.
2. **Burn-down** — plan vs actual by hour, rolled up and for the top campaigns, dead spend shaded, today's finish as a range.
3. **Move list** — number, action, from, to, amount per day, reason, status. Ends with the approval question. Manual items are listed after it, under "For a person to do".
4. **Watch list** — Unstable entities, Unmapped ads with spend, Medium-confidence matches, sold-out colorways on live ads, entities in cool-down with the time it ends, receivers rechecked from last check-in.
5. **Caveats** — attribution settings in play, failed tools, any tuned value that differs from default.
6. **C5LOG v1 block** — then: "Paste this into your next check-in."

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
