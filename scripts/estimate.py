#!/usr/bin/env python3
"""Estimate GCP Enterprise Databricks DBU cost for Lakeflow Jobs (classic) and Photon.

Reads ../references/gcp-enterprise-pricing.json and computes the Databricks DBU cost for
a given instance, cluster size and runtime, for both Jobs Compute (classic) and Jobs
Compute Photon.

Each variant is matched independently against its own supported-instance list. If the
requested instance isn't in a list (e.g. `n4-highmem-32`, or any n4/n4d for Photon), it
is resolved to the nearest comparable *supported* instance: same vCPU, same shape
(standard/highmem/highcpu), nearest family/generation, with a fallback alternative.
Photon prices are never derived from the classic rate — Photon always maps to a real
Photon-listed instance.

NOTE: this is the Databricks DBU charge only; it excludes the underlying Google Cloud
VM / infrastructure cost, billed separately by Google.

Usage:
  python3 estimate.py list [FILTER] [--photon|--classic]
  python3 estimate.py match --instance n4-highmem-32           # show the mapping only
  python3 estimate.py estimate --instance n4-highmem-32 --nodes 32 --hours 5 --runs 10
    [--vcpus N] [--memory G]   # override specs for an unrecognized instance name
"""
import argparse
import json
import os
import re
import sys

DATA = os.path.join(os.path.dirname(__file__), "..", "references", "gcp-enterprise-pricing.json")


def norm(name):
    s = str(name).lower()
    s = re.sub(r"\s*\(-lssd\)\s*", "", s)
    s = re.sub(r"\s*\(photon\)\s*", "", s)
    return s.replace("_", "-").strip()


def load():
    with open(DATA) as f:
        d = json.load(f)
    classic = d["products"]["Jobs Compute"]["instances"]
    photon = d["products"]["Jobs Compute Photon"]["instances"]
    for r in classic + photon:
        r["norm"] = norm(r["instance"])
    return {"classic": classic, "photon": photon}


# ---- instance matching ----
def parse_spec(name):
    n = norm(name)
    nums = re.findall(r"\d+", n)
    vcpu = int(nums[-1]) if nums else None            # trailing number is the vCPU count
    shape = ("highmem" if "highmem" in n else "highcpu" if "highcpu" in n
             else "standard" if "standard" in n else "")
    fam = re.match(r"([a-z]+\d+[a-z]*)", n)
    return vcpu, shape, (fam.group(1) if fam else "")


def fam_base(f):
    return re.sub(r"d$", "", f)


def fam_score(src, cand):
    if not src or not cand:
        return 9
    if src == cand:
        return 0
    if fam_base(src) == fam_base(cand):
        return 1
    ls = re.match(r"[a-z]+", src); lc = re.match(r"[a-z]+", cand)
    gs = re.search(r"\d+", src); gc = re.search(r"\d+", cand)
    if ls and lc and ls.group(0) == lc.group(0):
        return 2 + abs(int(gs.group(0)) - int(gc.group(0)))
    return 9


def rank(candidates, vcpu, shape, fam, mem=None):
    def key(r):
        shape_miss = 0 if (shape and shape in r["norm"]) else 1
        mem_d = abs(r["memory_gb"] - mem) if mem is not None else 0
        return (abs(r["vcpu"] - (vcpu if vcpu is not None else r["vcpu"])),
                shape_miss, mem_d, fam_score(fam, parse_spec(r["instance"])[2]), r["norm"])
    return sorted(candidates, key=key)


def resolve(candidates, name, vcpu=None, mem=None):
    """Match `name` against a supported-instance list -> {requested, primary, fallback, exact}."""
    nn = norm(name)
    sv, ss, sf = parse_spec(name)
    vcpu = vcpu if vcpu is not None else sv
    exact = [r for r in candidates if r["norm"] == nn]
    if exact:
        prim = exact[0]
        fb = next((r for r in rank(candidates, prim["vcpu"],
                                   ss or parse_spec(prim["instance"])[1], sf, prim["memory_gb"])
                   if r["norm"] != prim["norm"]), None)
        return {"requested": name, "primary": prim, "fallback": fb, "exact": True}
    ordered = rank(candidates, vcpu, ss, sf, mem)
    return {"requested": name, "primary": ordered[0] if ordered else None,
            "fallback": ordered[1] if len(ordered) > 1 else None, "exact": False}


def label(m):
    rec = m["primary"]
    return "n/a" if not rec else rec["instance"] + ("" if m["exact"] else " ≈")


# ---- commands ----
def cmd_list(args):
    p = load()
    rows = []
    if not args.photon:
        rows += [(r, "Jobs Compute") for r in p["classic"]]
    if not args.classic:
        rows += [(r, "Jobs Compute Photon") for r in p["photon"]]
    if args.filter:
        rows = [x for x in rows if args.filter.lower() in x[0]["instance"].lower()]
    rows.sort(key=lambda x: (x[1], x[0]["instance"]))
    print(f"{'instance':<42}{'product':<22}{'vCPU':>5}{'mem(GB)':>8}{'DBU/hr':>8}{'$/hr':>9}")
    print("-" * 94)
    for r, prod in rows:
        print(f"{r['instance']:<42}{prod:<22}{r['vcpu']:>5}{r['memory_gb']:>8}"
              f"{r['dbu_per_hour']:>8}{r['usd_per_hour']:>9.4f}")
    print(f"\n{len(rows)} row(s).")


def hourly(rec):
    # Billing basis: DBUs x $/DBU (the published $/hr column is only rounded to 2dp).
    return rec["dbu_per_hour"] * rec["usd_per_dbu"]


def one_line(m, rec):
    return (f"{label(m):<24} ({rec['vcpu']} vCPU, {rec['memory_gb']} GB, "
            f"{rec['dbu_per_hour']} DBU/hr, ${hourly(rec):.4f}/hr)")


def print_mapping(p, name, vcpu=None, mem=None):
    c = resolve(p["classic"], name, vcpu, mem)
    ph = resolve(p["photon"], name, vcpu, mem)
    print(f"Requested         : {name}")
    for title, m in [("Classic", c), ("Photon", ph)]:
        state = "kept as-is" if m["exact"] else "substituted (same vCPU/shape, nearest Photon-supported family)" \
            if title == "Photon" else "substituted (same vCPU/shape, nearest family)"
        print(f"{title + ' instance':<18}: {one_line(m, m['primary'])}  [{state}]"
              if m["primary"] else f"{title + ' instance':<18}: n/a")
        if m["fallback"]:
            fb = m["fallback"]
            print(f"{'  fallback alt':<18}: {fb['instance']} ({fb['vcpu']} vCPU, {fb['memory_gb']} GB, {fb['dbu_per_hour']} DBU/hr)")
    return c, ph


def cmd_match(args):
    print_mapping(load(), args.instance, args.vcpus, args.memory)


def cmd_estimate(args):
    p = load()
    c, ph = print_mapping(p, args.instance, args.vcpus, args.memory)
    if not c["primary"] or not ph["primary"]:
        sys.exit(f"Could not resolve '{args.instance}'. Pass --vcpus (and --memory) to match by spec.")
    node_hours = args.nodes * args.hours * args.runs
    print(f"\nCluster           : {args.nodes:g} node(s) x {args.hours:g} hr x {args.runs:g} run(s) "
          f"= {node_hours:g} node-hours")
    for title, m in [("Jobs Compute (classic)", c), ("Jobs Compute Photon", ph)]:
        rec = m["primary"]
        dbus = rec["dbu_per_hour"] * node_hours
        cost = dbus * rec["usd_per_dbu"]
        tag = "" if m["exact"] else f"  (via {rec['instance']} ≈)"
        print(f"\n{title}{tag}")
        print(f"  rate            : {rec['dbu_per_hour']} DBU/node/hr x ${rec['usd_per_dbu']}/DBU "
              f"= ${hourly(rec):.4f}/node/hr")
        print(f"  total DBUs      : {dbus:,.2f}")
        print(f"  Databricks cost : ${cost:,.2f}")
    print("\nNote: Databricks DBU charge only; Google Cloud VM/infra cost is billed separately.")
    if not c["exact"] or not ph["exact"]:
        print("Note: ≈ marks a substituted instance (requested type not offered for that variant).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list", help="list/search instances")
    pl.add_argument("filter", nargs="?", default="")
    pl.add_argument("--photon", action="store_true", help="only Photon instances")
    pl.add_argument("--classic", action="store_true", help="only classic Jobs Compute instances")
    pl.set_defaults(func=cmd_list)

    pm = sub.add_parser("match", help="show how an instance maps to Databricks")
    pm.add_argument("--instance", required=True)
    pm.add_argument("--vcpus", type=int, default=None)
    pm.add_argument("--memory", type=float, default=None)
    pm.set_defaults(func=cmd_match)

    pe = sub.add_parser("estimate", help="estimate cost of a run (classic + Photon)")
    pe.add_argument("--instance", required=True, help="instance name (resolved if not in a list)")
    pe.add_argument("--vcpus", type=int, default=None, help="override vCPU count for matching")
    pe.add_argument("--memory", type=float, default=None, help="override memory (GB) for matching")
    pe.add_argument("--nodes", type=float, default=1, help="number of nodes (default 1)")
    pe.add_argument("--hours", type=float, default=1, help="hours per run (default 1)")
    pe.add_argument("--runs", type=float, default=1, help="number of runs, e.g. per month (default 1)")
    pe.set_defaults(func=cmd_estimate)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
