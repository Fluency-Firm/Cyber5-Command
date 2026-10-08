# 03 Live — scheduled check-ins (report mode)

Live, run on a schedule with no person answering. It produces a report the media buyer reads when they log on. Hard rule 9 applies: report-only, every time.

## Inputs

| Input | Required | Default |
| --- | --- | --- |
| Plan | Yes | The C5PLAN pasted into the scheduled task's prompt. No plan: run Pass 2 only and say so |
| Mode | No | `morning` (full report) or `overnight` (alert-only); from the task's prompt, else `morning` |
| Last check-in | No | A C5LOG in the prompt or a handoff file the run can read. Without one, cool-down comes from the activity log alone |
| Delivery | No | Wherever the scheduled task sends its result: the chat, or a Slack channel or email the task names for the buyer. Delivery is output, not a data source; hard rule 3 still applies to data |
| Client name and metrics | No | For the client update draft; else `client_metrics` and no greeting name |

## Loads

What Live loads (`stages/03-live/CONTEXT.md`), **except `approval.md`**. Never load it in report mode.

## Process

1. **Say the mode** in the first line: "Stage 03 Live — scheduled morning report, read-only."
2. **Passes 1–3** exactly as in a live check-in. Pass 3 still builds the move list.
3. **Every proposal is Proposed**, listed under "Waiting for a person". Never ask for approval, never act on approval text in the prompt, and never treat a schedule as a standing yes.
4. **Morning mode:** render `output/templates.md` → Morning report: overnight, yesterday, today's proposed changes, and the client update draft (`client_update`), then the C5LOG and the handoff file. The client draft goes in the same delivery as the buyer's report, labelled "Draft for <client> — forward if it looks right".
5. **Overnight mode:** if any entity is Stalled or Not started, post the headline and those entities with spend since midnight and the hour each went dark. Otherwise post nothing (or one line, if the scheduler requires output). The overnight watch emits no C5LOG and no handoff file; the morning report carries the night forward.

## Preset prompts

Run 02 Plan by hand first and copy its C5PLAN. Then create scheduled tasks in your Claude client with these prompts, replacing the parts in angle brackets.

**Morning report** (daily at `report_hour`, Nov 26 – Dec 1):

```
Use cyber5-command. Scheduled morning report, read-only, for ad account <id>.
Plan:
<paste C5PLAN>
Report overnight stalls, yesterday vs plan by campaign and funnel role with anything worth
flagging, and today's plan with proposed changes and enter-by times, waiting for a person.
Add a client update draft for <client name> (metrics: <spend vs plan, purchases, ROAS>).
Do not ask for approval, do not change anything, and do not message the client.
Send the report and the draft to <the buyer's Slack DM | the buyer's email | chat>.
```

**Overnight watch** (hourly 00:00–08:00 on Black Friday and Cyber Monday):

```
Use cyber5-command. Scheduled overnight watch, read-only, for ad account <id>.
Plan:
<paste C5PLAN>
Only if a campaign is Stalled or Not started, post which ones, spend since midnight and when
each went dark, to <Slack channel | email>. Otherwise post nothing. Change nothing.
```

To act on a report: open a chat, paste the report's C5LOG, and ask for a check-in. The proposals come back with fresh numbers and go through the normal approval step.

## Never

- Load `approval.md` or call a write tool.
- Ask an approval question, or read approval into the prompt, a pasted block or an earlier report.
- Send the report anywhere the task's prompt doesn't name.
- Send anything to a client, or to a channel or address that includes the client. The client update is a draft the buyer forwards.
