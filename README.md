# gcp-lakeflow-pricing

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skill for **Databricks on
Google Cloud, Enterprise tier** pricing — specifically **Lakeflow Jobs (classic, "Jobs
Compute")** and **Jobs Compute Photon**.

It provides the DBU pricing data plus the methodology (cost formula + instance-matching
rules) so Claude can look up rates and estimate the Databricks cost of a jobs workload.

## What's here

| Path | Purpose |
|------|---------|
| `SKILL.md` | The skill definition Claude Code loads (pricing, rules, formulas). |
| `references/gcp-enterprise-pricing.json` | 248 instances (174 classic + 74 Photon): vCPU, memory, DBU/hr, $/DBU, $/hr. |
| `references/pricing-table.md` | The same pricing data as human-readable tables. |

Pricing scraped from the [Databricks pricing calculator](https://www.databricks.com/product/pricing/product-pricing/instance-types)
(GCP, Enterprise tier) on **2026-10-23**. Rates change — see "Refreshing the data" in `SKILL.md`.

## Install as a Claude Code skill

Copy this directory into your skills folder:

```bash
cp -r . ~/.claude/skills/gcp-lakeflow-pricing
```

Then ask Claude things like *"What's the GCP Enterprise rate for Lakeflow Jobs with
Photon?"* or *"Estimate the cost of a job on n4-highmem-32, 32 nodes, 5 hr/run, 10 runs."*

## How costs are calculated

Databricks bills by **DBUs**, not by VM:

```
cluster DBU/hr = Σ ( nodes × instance DBU/hr )
Rate/hr        = cluster DBU/hr × $/DBU      (Enterprise = $0.20)
DBU/day        = Rate/hr × ( run minutes ÷ 60 ) × runs per day
```

- **DBU charge only** — this excludes the underlying Google Cloud Compute Engine VM,
  disk, and network cost, which Google bills separately.
- **Instance matching** — classic and Photon are matched independently against their own
  supported-instance lists. An exact match is kept; otherwise the nearest same-vCPU /
  same-shape / nearest-family instance is substituted (`≈`), with a fallback alternative.
  A Photon rate is never derived from classic — Photon always maps to a real
  Photon-listed instance.

## Scope

Enterprise tier only; classic *Jobs Compute* and *Jobs Compute Photon* only (not
Serverless, DLT, SQL, or All-Purpose); Google Cloud only.
