from collections import deque, defaultdict
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple

from app.core.entities.course import Course
from app.core.ports.algorithm_service import AlgorithmService


class AlgorithmServiceImpl(AlgorithmService):
    def _course_map(self, courses: List[Course]) -> Dict[str, Course]:
        return {c.code: c for c in courses}

    def _edges(self, courses: List[Course]) -> Dict[str, List[str]]:
        m = self._course_map(courses)
        g: Dict[str, List[str]] = defaultdict(list)
        for c in courses:
            for p in c.prerequisites:
                if p in m:
                    g[p].append(c.code)
        return g

    def detect_cycles(self, courses: List[Course]) -> Tuple[bool, List[List[str]]]:
        m = self._course_map(courses)
        g = self._edges(courses)
        state: Dict[str, int] = {code: 0 for code in m}
        stack: List[str] = []
        cycles: List[List[str]] = []

        def dfs(u: str):
            state[u] = 1
            stack.append(u)
            for v in g.get(u, []):
                if state.get(v, 0) == 0:
                    dfs(v)
                elif state.get(v) == 1:
                    try:
                        k = stack.index(v)
                        cycles.append(stack[k:] + [v])
                    except ValueError:
                        cycles.append([v, u, v])
            stack.pop()
            state[u] = 2

        for code in m:
            if state[code] == 0:
                dfs(code)
        return (len(cycles) > 0, cycles)

    def topological_sort(self, courses: List[Course]) -> List[str]:
        m = self._course_map(courses)
        indeg: Dict[str, int] = {c.code: 0 for c in courses}
        children: Dict[str, List[str]] = defaultdict(list)
        for c in courses:
            for p in c.prerequisites:
                if p in m:
                    indeg[c.code] += 1
                    children[p].append(c.code)
        q = deque([code for code, d in indeg.items() if d == 0])
        order: List[str] = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in children.get(u, []):
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        if len(order) != len(m):
            return order
        return order

    def plan_min_cycles(
        self,
        courses: List[Course],
        max_credits: int,
        approved: Optional[Set[str]] = None,
        target_codes: Optional[Set[str]] = None,
        failures: Optional[Dict[int, Set[str]]] = None,
        max_exact_courses: int = 18,
    ) -> Dict:
        approved = approved or set()
        failures = failures or {}

        if target_codes is None or len(target_codes) == 0:
            order = self.topological_sort(courses)
            codes_from_order: List[str] = [c for c in order if c not in approved]
            if not codes_from_order:
                return {"total_cycles": 0, "cycles": []}
            limited = set(codes_from_order[:max_exact_courses])
            target_codes = limited

        m = self._course_map(courses)
        subset_codes = [c for c in target_codes if c in m]
        if not subset_codes:
            return {"total_cycles": 0, "cycles": []}

        idx = {code: i for i, code in enumerate(subset_codes)}
        credits = [m[c].credits for c in subset_codes]
        pre_mask: List[int] = [0] * len(subset_codes)
        for c in subset_codes:
            i = idx[c]
            needed = 0
            for p in m[c].prerequisites:
                if p in idx:
                    needed |= 1 << idx[p]
                elif p not in approved and p in m:
                    needed |= 1 << 62
            pre_mask[i] = needed

        start_mask = 0
        for c in subset_codes:
            if c in approved:
                start_mask |= 1 << idx[c]

        n = len(subset_codes)

        @lru_cache(maxsize=None)
        def dp(mask: int, t: int) -> int:
            if mask == (1 << n) - 1:
                return 0
            avail_idx: List[int] = []
            for i in range(n):
                if not (mask >> i) & 1:
                    if pre_mask[i] & mask == pre_mask[i]:
                        avail_idx.append(i)
            if not avail_idx:
                return 10**9

            best = 10**9
            L = len(avail_idx)

            if L <= 15:
                for sub in range(1, 1 << L):
                    total = 0
                    submask = 0
                    for k in range(L):
                        if (sub >> k) & 1:
                            i = avail_idx[k]
                            total += credits[i]
                            submask |= 1 << i
                    if total <= max_credits:
                        next_mask = mask
                        if t in failures:
                            failed_set = failures[t]
                            for k in range(L):
                                if (sub >> k) & 1:
                                    ccode = subset_codes[avail_idx[k]]
                                    if ccode not in failed_set:
                                        next_mask |= 1 << avail_idx[k]
                        else:
                            next_mask = mask | submask
                        cand = 1 + dp(next_mask, t + 1)
                        if cand < best:
                            best = cand
                return best
            else:
                ord_idx = sorted(avail_idx, key=lambda i: (-credits[i], i))
                total = 0
                chosen: List[int] = []
                for i in ord_idx:
                    if total + credits[i] <= max_credits:
                        total += credits[i]
                        chosen.append(i)
                next_mask = mask
                if t in failures:
                    failed_set = failures[t]
                    for i in chosen:
                        ccode = subset_codes[i]
                        if ccode not in failed_set:
                            next_mask |= 1 << i
                else:
                    for i in chosen:
                        next_mask |= 1 << i
                return 1 + dp(next_mask, t + 1)

        def reconstruct() -> List[Dict]:
            sched: List[Dict] = []
            mask, t = start_mask, 0
            while mask != (1 << n) - 1:
                avail_idx: List[int] = []
                for i in range(n):
                    if not (mask >> i) & 1:
                        if pre_mask[i] & mask == pre_mask[i]:
                            avail_idx.append(i)
                if not avail_idx:
                    break
                best = 10**9
                best_sub = 0
                L = len(avail_idx)
                if L <= 15:
                    for sub in range(1, 1 << L):
                        total = 0
                        submask = 0
                        for k in range(L):
                            if (sub >> k) & 1:
                                i = avail_idx[k]
                                total += credits[i]
                                submask |= 1 << i
                        if total <= max_credits:
                            next_mask = mask
                            if t in failures:
                                failed_set = failures[t]
                                for k in range(L):
                                    if (sub >> k) & 1:
                                        i = avail_idx[k]
                                        ccode = subset_codes[i]
                                        if ccode not in failed_set:
                                            next_mask |= 1 << i
                            else:
                                next_mask = mask | submask
                            cand = 1 + dp(next_mask, t + 1)
                            if cand < best:
                                best = cand
                                best_sub = sub
                else:
                    ord_idx = sorted(avail_idx, key=lambda i: (-credits[i], i))
                    total = 0
                    chosen_bits = 0
                    for i in ord_idx:
                        if total + credits[i] <= max_credits:
                            total += credits[i]
                            k = avail_idx.index(i)
                            chosen_bits |= 1 << k
                    best_sub = chosen_bits

                cycle_courses: List[Dict] = []
                total_cred = 0
                for k in range(L):
                    if (best_sub >> k) & 1:
                        i = avail_idx[k]
                        code = subset_codes[i]
                        course = m[code]
                        failed = t in failures and code in failures[t]
                        cycle_courses.append(
                            {
                                "code": code,
                                "name": course.name,
                                "credits": course.credits,
                                "approved": not failed,
                            }
                        )
                        total_cred += course.credits
                sched.append({"cycle": t + 1, "courses": cycle_courses, "total_credits": total_cred})

                if t in failures:
                    failed_set = failures[t]
                    for k in range(L):
                        if (best_sub >> k) & 1:
                            i = avail_idx[k]
                            ccode = subset_codes[i]
                            if ccode not in failed_set:
                                mask |= 1 << i
                else:
                    for k in range(L):
                        if (best_sub >> k) & 1:
                            i = avail_idx[k]
                            mask |= 1 << i
                t += 1
            return sched

        total = dp(start_mask, 0)
        schedule = reconstruct()
        return {"total_cycles": total if total < 10**9 else -1, "cycles": schedule}
