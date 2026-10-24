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

## Files

- `references/gcp-enterprise-pricing.json` — machine-readable: full per-instance list
  (vCPU, memory, `dbu_per_hour`, `usd_per_dbu`, `usd_per_hour`) for both products.
- `references/pricing-table.md` — the same data as human-readable tables.
- `scripts/estimate.py` — look up instances and compute cost estimates.
- `scripts/build_databricks_cost_tab.py` — add a Databricks cost tab to a POC
  workload-selection report (see below).

## How to use

**Quote a rate or a specific instance.** Read `references/pricing-table.md` (or the
JSON) and report the numbers. The $/DBU is $0.20 for both products; per-instance
$/hr is in the table.

**Look up / search instances:**
```
python3 scripts/estimate.py list                 # everything
python3 scripts/estimate.py list n2-standard     # name substring
python3 scripts/estimate.py list --photon        # Photon only
python3 scripts/estimate.py list --classic       # non-Photon only
```

**Estimate a workload's Databricks cost (classic + Photon in one call):**
```
python3 scripts/estimate.py estimate --instance n4-highmem-32 --nodes 32 --hours 5 --runs 10
```
`--nodes` x `--hours` x `--runs` gives total node-hours; cost = node-hours x instance
$/hr, shown for both Jobs Compute (classic) and Jobs Compute Photon. Always restate that
this is the DBU charge only and the GCE VM cost is extra.

**Instance matching.** Classic and Photon are matched **independently**, each against its
own supported-instance list. If the requested instance isn't in a list (e.g.
`n4-highmem-32`, or any `n4`/`n4d` for Photon), it is resolved to the nearest comparable
*supported* instance — same vCPU, same shape (standard/highmem/highcpu), nearest
family/generation — with a fallback alternative (`≈` marks a substitute). Supported
instances are kept as-is. A Photon rate is **never derived** from the classic rate —
Photon always maps to a real Photon-listed instance. vCPU/shape are inferred from the
name; override with `--vcpus`/`--memory` for unusual names. To just see the mapping:
```
python3 scripts/estimate.py match --instance n4-highmem-32
```

## Adding a Databricks cost tab to a POC report

For a "Databricks POC workload selection" report (`report-*.html`) whose Cost tab is
rendered by JS from an embedded `compute-data` JSON:

```
python3 scripts/build_databricks_cost_tab.py INPUT.html [-o OUTPUT.html]
```

This writes a **new** file (never overwrites the input) with a **Databricks cost** tab
that is an **exact replica of the report's Cost tab** — every table, collapsible section
and control — with Databricks columns appended. At runtime it deep-clones the Cost-tab
DOM, makes all ids/control-classes unique so the clone is fully independent (it never
corrupts the original Cost tab), and wires a scoped copy of the report's cost model to
the new tab's **own working controls** (days, headroom, rate inputs, workload
checkboxes, selection buttons, CSV export).

For two variants — **Jobs Compute (classic)** and **Jobs Compute Photon**, GCP
Enterprise — it appends: comparable Databricks instance + DBU/hour + Rate/hour (+ daily
DBU and all-in daily cost) on the Workloads and Instance-types tables, and a DBU-cost
field folded into an all-in Total on "Compare the selections" / "Compute cost" /
"Total cost".

Instance-mapping rule: classic and Photon are matched **independently**, each against its
own supported-instance list. Keep the original instance when it's in that list; otherwise
substitute a same-vCPU instance (same shape, closest memory, nearest family/generation)
as primary with a second as fallback — `≈` marks a substitute. A Photon rate is **never
derived** from the classic rate — if a type has no Photon pricing (e.g. all `n4`/`n4d`),
Photon substitutes a real Photon-listed same-spec instance (e.g. `n2`/`n2d`).

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
