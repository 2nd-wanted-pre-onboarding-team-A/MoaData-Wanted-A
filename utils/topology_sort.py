import collections
from typing import Dict, List

def _check_double_edge(g):
    for u in g:
        v_counter = collections.Counter(g[u])
        if len(v_counter) == 0:
            continue
        v, n = v_counter.most_common(1)[0]
        if n > 1:
            raise ValueError(f"There should not be more than one process going from {u} to {v}.")

def _check_one_destination(g):
    end_cnt = 0
    for u in g:
        if len(g[u]) == 0:
            end_cnt += 1
    if end_cnt > 1:
        raise ValueError("There should not be more than one final destination.")

def _get_parents_size(g):
    parents_size = {k: 0 for k in g.keys()}
    for u in g:
        for v in g[u]:
            parents_size[v] += 1
    return parents_size

def _topology_sort(g, p) -> List[str]:
    """
    위상 정렬
    동시에 사이클도 판단한다.
    """
    q = collections.deque()
    n = len(list(g.keys()))

    for k in g:
        if p[k] == 0:
            q.appendleft(k)

    sorted_data = []
    while q:
        u = q.pop()
        sorted_data.append(u)

        for v in g[u]:
            p[v] -= 1
            if p[v] == 0:
                q.appendleft(v)
    if len(sorted_data) < n:
        raise ValueError("A cycle has been detected.")
    return sorted_data

def topology_sort(g: Dict[str, List[str]]):
    _check_double_edge(g)
    _check_one_destination(g)
    parents_size = _get_parents_size(g)
    return _topology_sort(g, parents_size)

