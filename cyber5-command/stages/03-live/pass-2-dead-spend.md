# Pass 2 — Spend on sold-out products

Finds ads spending on products people can't buy.

1. **Map** every active ad to products with `shared/catalog-engine.md` → Map ads to products.
2. **Roll up** stock with `shared/catalog-engine.md` → Roll up stock.
3. **Per ad:**
   - **Dead:** every mapped product is Out.
   - **Leaking:** the share of products Out is above `leak_share_threshold`, or, where only a variant share is available, that share is above `leak_variant_share`.
   - **Size gaps:** Partial products only, below those lines. Watch list, never a proposal.
   - **Clean** otherwise.
4. **Spend at risk** = window spend × sold-out share for Dead and Leaking ads, plus the same rate projected over the rest of the window. Catalog ads on unfiltered sets count as an upper bound only, because Meta may already skip sold-out items; say so.
5. **Leaking: converting or not.** Compare each Leaking ad's cost per purchase (or ROAS) with its own ad set at the same attribution, and pass the result to Pass 3. Compare only ads optimised for purchases; mark others "not comparable".
6. **Unmapped share.** If Unmapped ads hold more than `unmapped_flag` of purchase-goal spend, say so in the headline. Add a task: "Name the product (or use product URLs) in ads, so stock can be checked."
7. **Sold-out styles.** List every fully sold-out style or colorway found in any set on the watch list, with "check no live creative features these".
8. **Back in stock.** An ad paused on an earlier check-in (from C5LOG) whose products are In again gets a re-activation proposal in Pass 3.
