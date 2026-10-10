# -*- coding: utf-8 -*-
"""세 구조를 같은 자로 재본다 — 무엇이 안 남는지가 드러난다."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from traceable import Trace, score, table

# ① RAG — 문서는 남지만 판단 경로가 없다
rag = Trace(
    items=[{"id": i, "accepted": True, "source": f"https://doc/{i}",
            "text": "바다 관련 문서"} for i in range(5)],
    state={"바다": 2.0}, label="RAG", step=1, size=5)

# ② 그래프 에이전트 — 경로는 남지만 그 선택이 다음을 바꾸지 않는다
graph = Trace(
    units=[{"id": n, "used": True, "path_logged": True, "evidence": 2,
            "branches": [{"options": {"a": 0.5, "b": 0.5}}]}
           for n in ("plan", "search", "answer")],
    items=[{"id": i, "accepted": True, "source": f"https://doc/{i}",
            "text": "바다 관련 문서"} for i in range(5)],
    state={"바다": 2.0}, label="그래프", step=1, size=5)

# ③ 학습하는 판단 구조 — 갈림길이 실제로 기울어 있다
learned = Trace(
    units=[{"id": n, "used": True, "path_logged": True, "evidence": 4,
            "branches": [{"options": {"a": 0.78, "b": 0.22}}]}
           for n in ("plan", "search", "answer")],
    items=[{"id": i, "accepted": True, "source": f"https://doc/{i}",
            "text": "바다 관련 문서"} for i in range(5)],
    state={"바다": 2.0}, label="학습형", step=1, size=5)

print(table([score(x) for x in (rag, graph, learned)]))
print("\n'-' 는 0점이 아니라 '잴 단위가 없다'는 뜻입니다.")
