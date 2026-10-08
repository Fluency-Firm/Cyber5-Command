# Exports

Three outputs, in order of importance. Chat always comes first and must stand on its own.

| Output | For | When | Needs |
| --- | --- | --- | --- |
| Chat view | The media buyer | Every run | Nothing |
| Handoff file (.md) | A later run, a teammate, or an agent | Every run (`export_handoff`) | File creation; otherwise printed in chat as a fenced block |
| Client update draft | The client's point of contact, forwarded by the buyer | Scheduled morning reports (`client_update`), or when asked in any Live check-in | Nothing; plain text in Slack or email form |
| Leadership deck (PDF) | Account and agency leads | Ready, Plan and Review only (`export_deck`). Never in Live: check-ins stay in chat and the handoff file | File creation and code execution; otherwise skipped with one line saying so |

## Rules

1. **Never let an export block the chat answer.** Render chat first, then exports. If an export fails, say which one and why in one line, and carry on.
2. **Same numbers everywhere.** The handoff and deck use the figures already shown in chat. Never re-pull data or round differently for an export.
3. **No new claims.** The deck summarizes; it adds no findings, advice or forecasts that chat didn't show.
4. **Neutral by default.** No agency or client branding unless set in `deck_brand`. The client account name appears only on the cover.
5. **Approval stays in chat.** No export contains an approval question, and none can be used to approve a move.
6. **Client updates are drafts.** The skill never sends one to a client or any address the user didn't name for the buyer. It goes to the buyer, who forwards it. See `output/templates.md` → Client update.

## Combined runs

When one run covers more than one stage (for example Ready then Plan), write **one** handoff file named for the last stage. It carries every stage's tasks, findings and blocks. Make **one deck per stage** that makes decks, so each can be shared on its own.

## Handoff file

Follow `contracts/handoff-v1.md` exactly, including the authorization notice. Write it with the stage's tasks, proposals, blocks, findings and caveats.

## Leadership deck

A short PDF, 16:9, one idea per slide, at most 6 slides. Charts are drawn from the same rows as chat. Slide titles state the finding, not the topic.

| Stage | Slides |
| --- | --- |
| Ready | 1 Cover: account, grade, days to Cyber5 · 2 Scorecard: five categories as bars with the grade line · 3 Top fixes: the 5 earliest do-bys with owners · 4 Meta's own suggestions (marked not graded) |
| Plan | 1 Cover: basis and window · 2 Last year by day: spend share vs purchase share · 3 Day × hour heatmap of purchases with delivery gaps outlined · 4 This year's day and daypart plan · 5 Budget guard and creative plan |
| Review | 1 Cover: what the skill would have caught · 2 Scorecard: catches with lead time and purchases still ahead · 3 Burn-down over the window (`lines`: cumulative actual vs plan, delivery gaps shaded) · 4 Fixes for this year's plan |

Build it with `output/deck.py`. Write a JSON spec of the slides (format in the script's docstring), then run `python output/deck.py spec.json out.pdf --preview previews/`. Use only the slide types the script supports, so every deck looks the same in every agency. If Python or its plotting libraries can't run, skip the deck and say so in one line.

**Check before sending.** Open the PNG previews and look at every slide. Fix and rebuild if any text is clipped or overflows, any label overlaps, or any number differs from chat. The script also prints warnings for titles and table cells it had to shorten; treat each warning as something to fix. Every slide ends with the source line "Meta Ads MCP · <account ID> · <attribution> · <run_at>", which the script adds. Use the account ID there, not the name: the name appears only on the cover.

Name each deck `cyber5-<account_id>-<stage>-<YYYYMMDD-HHMM>.pdf`, matching the handoff file.
