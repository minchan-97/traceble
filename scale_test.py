# -*- coding: utf-8 -*-
"""
규모가 커지면 추적이 끊기는가 — **구조에 따라 다르다.**

주의: 자료를 비율 그대로 불리면 비율로 재는 자는 당연히 안 변한다(순환논증).
traceable 은 시스템의 성질을 재는 자이지, 자 자체가 규모에 강한 게 아니다.
그래서 여기서는 **서로 다른 두 구조**를 같은 규모에 걸쳐 재고,
자가 그 차이를 잡아내는지 본다.

  ① 매칭형  새 주제가 기존 판단 단위와 맞아야 경로가 남는다.
            주제가 늘수록 안 맞는 게 늘어 경로가 끊긴다.
  ② 배정형  맞는 단위가 없으면 가장 가까운 단위에 붙인다.
            정확도는 떨어지지만 경로는 끊기지 않는다.
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from traceable import Trace, score, table

rng = random.Random(11)
BASE_UNITS = 40
SAMPLE = 400          # 자료는 표본만 만든다 (비율만 쓰므로 결과는 같다)


def build(n_items, mode):
    # 주제는 자료를 거의 따라 늘고(현실: 새 자료는 새 주제를 데려온다),
    # 판단 단위는 로그로만 는다. 그 간격이 규모의 부담이다.
    n_topics = int(25 * (n_items / 500) ** 0.8)
    n_units = BASE_UNITS + int(12 * math.log10(max(1.0, n_items / 500)))
    covered = min(1.0, n_units * 1.2 / max(1, n_topics))

    units = []
    for i in range(n_units):
        logged = True if mode == "배정형" else (rng.random() < covered)
        ev = int(rng.paretovariate(1.5) * 3)
        branches = ([{"options": {"a": 0.5 + rng.random() * 0.4,
                                  "b": 0.5 - rng.random() * 0.4}}]
                    if logged else [])
        units.append({"id": f"u{i}", "used": True, "path_logged": logged,
                      "evidence": ev if logged else 0, "branches": branches})

    items = [{"id": i, "accepted": True, "source": f"https://s/{i}",
              "text": f"주제{i % n_topics} 자료 {i}"} for i in range(SAMPLE)]
    state = {f"주제{k}": rng.random() * 3
             for k in rng.sample(range(n_topics), min(28, n_topics))}
    return Trace(units=units, items=items, state=state,
                 label=f"{mode} {n_items:,}", step=n_items, size=n_items)


rows = []
for n in (500, 2_000, 10_000, 50_000):
    for mode in ("매칭형", "배정형"):
        rows.append(score(build(n, mode)))
print(table(rows))
print("\n같은 규모에서 두 구조의 경로 추적률이 갈린다 — 자가 차이를 잡아낸다.")
