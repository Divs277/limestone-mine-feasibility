"""Techno-economic model for a small open-pit limestone mine.

Run:  python src/model.py
Reads data/assumptions.csv, prints key results, saves charts to outputs/.
All money is in INR crore (1 crore = 10 million).
"""
import math
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
CRORE = 1e7


def load_assumptions(path=ROOT / "data" / "assumptions.csv"):
    df = pd.read_csv(path)
    return dict(zip(df["parameter"], df["value"].astype(float)))


def fleet(a):
    """How many trucks are needed to move ore + waste."""
    total_t_per_day = a["annual_ore"] * 1e6 * (1 + a["stripping_ratio"]) / a["working_days"]
    hours = a["shifts_per_day"] * a["shift_hours"]
    trips = hours * 60 * a["truck_availability"] * a["truck_utilisation"] / a["truck_cycle_min"]
    per_truck = trips * a["truck_payload"]
    return total_t_per_day, per_truck, math.ceil(total_t_per_day / per_truck)


def cashflows(a):
    life = int(a["reserve"] / a["annual_ore"])
    ore_t = a["annual_ore"] * 1e6
    revenue = ore_t * a["price"] / CRORE
    mining = (ore_t * a["mining_cost_ore"] + ore_t * a["stripping_ratio"] * a["mining_cost_waste"]) / CRORE
    processing = ore_t * a["processing_cost"] / CRORE
    royalty = revenue * a["royalty_rate"]
    opex = mining + processing + royalty + a["overhead"]
    ebitda = revenue - opex
    dep = a["capex"] / life
    tax = max(0.0, (ebitda - dep) * a["tax_rate"])
    cf = ebitda - tax

    rows = [{"year": 0, "cashflow": -a["capex"]}]
    rows += [{"year": y, "cashflow": cf} for y in range(1, life + 1)]
    return pd.DataFrame(rows), {"revenue": revenue, "opex": opex, "ebitda": ebitda, "tax": tax, "life": life}


def npv(cfs, r):
    return sum(cf / (1 + r) ** y for y, cf in zip(cfs["year"], cfs["cashflow"]))


def irr(cfs, lo=-0.5, hi=1.0):
    f = lambda r: npv(cfs, r)
    if f(lo) * f(hi) > 0:
        return float("nan")
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(lo) * f(mid) > 0 else (lo, mid)
    return mid


def payback(cfs):
    cum = 0.0
    for y, cf in zip(cfs["year"], cfs["cashflow"]):
        prev, cum = cum, cum + cf
        if cum >= 0 and y > 0:
            return y - 1 + (-prev / cf)
    return float("nan")


def run(a):
    cfs, s = cashflows(a)
    return {"NPV (INR cr)": npv(cfs, a["discount_rate"]), "IRR": irr(cfs), "Payback (yrs)": payback(cfs), **s}, cfs


def sensitivity(a, swing=0.2):
    """+/- swing on each driver, ranked by effect on NPV (tornado chart data)."""
    base = run(a)[0]["NPV (INR cr)"]
    out = []
    for p in ["price", "mining_cost_ore", "mining_cost_waste", "processing_cost",
              "stripping_ratio", "capex", "discount_rate", "annual_ore"]:
        res = []
        for m in (1 - swing, 1 + swing):
            b = dict(a); b[p] = a[p] * m
            res.append(run(b)[0]["NPV (INR cr)"] - base)
        out.append((p, res[0], res[1]))
    return base, sorted(out, key=lambda t: abs(t[2] - t[1]))


def main():
    a = load_assumptions()
    res, cfs = run(a)
    tpd, per_truck, n = fleet(a)
    print(f"Mine life: {res['life']} years")
    print(f"Revenue/yr: {res['revenue']:.1f} cr | Opex/yr: {res['opex']:.1f} cr | EBITDA/yr: {res['ebitda']:.1f} cr")
    print(f"NPV @ {a['discount_rate']:.0%}: {res['NPV (INR cr)']:.1f} cr | IRR: {res['IRR']:.1%} | Payback: {res['Payback (yrs)']:.1f} yrs")
    print(f"Material to move: {tpd:,.0f} t/day | one truck: {per_truck:,.0f} t/day | trucks needed: {n}")

    base, sens = sensitivity(a)
    for p, lo, hi in sens[::-1]:
        print(f"  {p:18s} -20%: {lo:+7.1f}   +20%: {hi:+7.1f}")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for i, (p, lo, hi) in enumerate(sens):
        ax.barh(i, lo, color="#c0504d"); ax.barh(i, hi, color="#4f81bd")
    ax.set_yticks(range(len(sens))); ax.set_yticklabels([s[0] for s in sens])
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("Change in NPV (INR crore) for -20% / +20% in each input")
    ax.set_title(f"Sensitivity of NPV (base = {base:.0f} cr)")
    plt.tight_layout(); plt.savefig(ROOT / "outputs" / "tornado.png", dpi=150)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(cfs["year"], cfs["cashflow"].cumsum(), marker="o")
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xlabel("Year"); ax.set_ylabel("Cumulative cash flow (INR crore)")
    ax.set_title("Cumulative cash flow")
    plt.tight_layout(); plt.savefig(ROOT / "outputs" / "cumulative_cashflow.png", dpi=150)


if __name__ == "__main__":
    main()
