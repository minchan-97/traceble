# -*- coding: utf-8 -*-
"""몰랑이 성장 기록(pkl) 여러 개 → 시간에 따른 설명 가능성."""
import os, pickle, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from traceable import series, table, report
from traceable.adapters import from_molang

folder = sys.argv[1] if len(sys.argv) > 1 else "."
files = sorted([f for f in os.listdir(folder) if f.endswith(".pkl")],
               key=lambda f: int(re.findall(r"(\d+)", f)[-1]))
traces = []
for f in files:
    with open(os.path.join(folder, f), "rb") as fp:
        d = pickle.load(fp)
    if not (d.get("meta") or {}).get("cycle"):
        continue
    traces.append(from_molang(d, label=f.replace(".pkl", "")))

sc = series(traces)
print(table(sc))
r = report(sc)
print(f"\n시점 {r['n_points']} · 회차 {r['step_range']} · "
      f"규모 {r['size_range']} ({r.get('size_growth')}배)")
for a, v in r["axes"].items():
    if v:
        print(f"  {a:9} {v['first']} → {v['last']}  유지: {v['held']}")
