---
name: gcp-lakeflow-pricing
description: GCP Enterprise-tier Databricks pricing for Lakeflow Jobs (classic, "Jobs Compute") and Jobs Compute Photon. Use to look up the $/DBU rate or per-instance DBU/hr and $/hr, or to estimate the Databricks cost of a jobs workload on Google Cloud. Triggers on questions about GCP job compute cost, Lakeflow Jobs pricing, Photon jobs pricing, DBU rates, or cost estimates for Databricks jobs on GCP Enterprise.
---

# GCP Enterprise — Lakeflow Jobs (classic) & Photon pricing

Pricing for **Databricks on Google Cloud, Enterprise tier**, for the two classic
jobs compute types:

- **Jobs Compute** = **Lakeflow Jobs (classic)** — **$0.20 / DBU**
- **Jobs Compute Photon** — **$0.20 / DBU**

Both headline rates are the same per DBU; Photon instances consume **more DBUs per
hour** per node (Photon's higher DBU/hr is where the speed/cost tradeoff shows up),
so always compare on **$/hour** or total DBUs, not the $/DBU rate.

Data was scraped on **2026-10-23** from the Databricks pricing calculator:
`https://www.databricks.com/product/pricing/product-pricing/instance-types`
(underlying data file `.../en-pricing-assets/data/pricing/GCP.json`).

## Files

- `references/gcp-enterprise-pricing.json` — machine-readable: full per-instance list
  (vCPU, memory, `dbu_per_hour`, `usd_per_dbu`, `usd_per_hour`) for both products.
- `references/pricing-table.md` — the same data as human-readable tables.

## Important scope / caveats

- **DBU charge only.** These figures are the Databricks software (DBU) cost. They do
  **not** include the underlying Google Cloud Compute Engine VM, disk, or network
  cost, which Google bills separately. For all-in cost, add the GCE VM price.
- **Enterprise tier only.** Premium is cheaper ($0.15/DBU for the same products). If
  the user asks about Premium/Standard or AWS/Azure, this skill doesn't cover it —
  say so; the same source page has that data.
- **Classic compute only.** This covers *Jobs Compute* and *Jobs Compute Photon*, not
  Jobs **Serverless** Compute, DLT, SQL, or All-Purpose. Don't substitute a serverless
  rate when asked about classic jobs.
- Rates change. Note the scrape date when you quote them, and re-scrape if stale
  (see "Refreshing the data" below).

## How to answer

**Quote a rate or a specific instance.** Read `references/pricing-table.md` (or the
JSON) and report the numbers. The $/DBU is $0.20 for both products; per-instance
DBU/hr and $/hr are in the table.

**Estimate a workload's Databricks cost.** Databricks bills by **DBUs**, not by VM.
Use the billing basis `DBU/hr × $/DBU` (the published `$/hr` column is only rounded to
2 dp — e.g. `n4-standard-32` is 6.72 × 0.20 = **$1.344/hr**, not the listed $1.34):

```
cluster DBU/hr = Σ ( nodes × instance DBU/hr )
Rate/hr        = cluster DBU/hr × $0.20 per DBU
DBU/day        = Rate/hr × ( run minutes ÷ 60 ) × runs per day
cost           = Rate/hr × total node-hours        (node-hours = nodes × hours × runs)
```

Report both **Jobs Compute (classic)** and **Jobs Compute Photon**, and always restate
that this is the DBU charge only — the GCE VM cost is extra.

## Instance matching

Classic and Photon are matched **independently**, each against its own supported-instance
list in the JSON. The rule:

1. If the requested machine type is in the list, **keep it**.
2. Otherwise substitute the nearest comparable *supported* instance: **same vCPU**, same
   shape (standard / highmem / highcpu), then nearest family/generation. Offer a second
   instance as a **fallback** alternative. Mark a substitute with `≈`.

Nearest family/generation means: same family first, then the `d` sibling (`n4` ↔ `n4d`),
then the same letter-series nearest generation (`n4` → `n2` → `n1`), then other series.

A **Photon rate is never derived** from the classic rate. Several families (all `n4`/`n4d`,
plus `n1`, `c2`, `c4`/`c4d`, GPU families) have **no Photon SKU** — for those, Photon must
substitute a real Photon-listed same-spec instance (typically `n2`/`n2d`). Example:
`n4-highmem-32` (32 vCPU, 256 GB) → classic `n4d-highmem-32 ≈`, Photon `n2-highmem-32 (Photon) ≈`.

## Notes on instance naming

- `(Photon)` suffix = Photon-accelerated engine (in the **Jobs Compute Photon** product).
- `(-lssd)` = local-SSD variant of the instance.
- Families include n1/n2/n2d/n4/n4d (general & high-mem), c2/c3/c3d/c4/c4a/c4d
  (compute-optimized), e2 (cost-optimized), and a2/a3/g2/g4 (GPU).

## Refreshing the data

The calculator loads a JSON feed. To re-scrape, fetch
`https://www.databricks.com/en-pricing-assets/data/pricing/GCP.json` (a flat array of
records with fields `cloud, instance, compute, plan, vcpu, memory, baserate, dburate,
hourrate`), filter to `plan == "Enterprise"` and `compute in ("Jobs Compute",
"Jobs Compute Photon")`, and regenerate the two reference files. The page is
JS-rendered, so fetch the JSON feed directly (via browser/devtools or an authenticated
request) rather than scraping the HTML.
