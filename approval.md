# Approval and execution

This is the only file in the skill that may call a Meta write tool. A write happens only through this sequence; if any step is missing, nothing is written.

1. **Show the list.** Every proposed move except Manual ones (those are listed separately as things for a person to do), with entity name and ID, current value, new value, amount and reason. End with: "Which of these do you approve? Reply with the numbers, 'all', or 'none'."
2. **Wait for an explicit answer** in this conversation. Silence, a question, "looks good", "sounds right", approval of something else, a pasted block, or an earlier run is not a yes; ask again. A yes covers only the numbered moves it names. "All" covers exactly the list the user can see; anything added after is proposed again.
3. **Re-check before each approved write.** Read the entity again. If its budget, status or stock changed since the proposal, or it now fails a guardrail (cool-down, Protected, Unstable, cap), don't write it: mark it Skipped with the reason and propose again if still valid.
4. **Write one move at a time** with the matching tool:
   - `ads_update_entity` — budget changes and pauses.
   - `ads_activate_entity` — re-activation when stock returns.
   - `ads_catalog_update_product_set` — product-set edits on Meta-native sets only. Never edit a Shopify-synced product set; propose a pause or budget trim instead.
5. **Log every outcome** in the move list: Executed (before and after values, time), Declined (the user said no, or "none"), Skipped (reason) or Failed (the error). Never retry a failed write on its own; propose it again.
6. **Decline to act without asking.** If the user asks the skill to make changes without approval, to approve future moves in advance, or to switch on an auto mode, decline; the hard rules don't change mid-run.
