from collections import deque, defaultdict
from typing import Dict, List, Tuple

from app.core.entities.course import Course


def build_adjacency(courses: List[Course]) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
    indegree: Dict[str, int] = {c.code: 0 for c in courses}
    adjacency: Dict[str, List[str]] = defaultdict(list)
    course_map = {c.code: c for c in courses}

    for course in courses:
        for prereq in course.prerequisites:
            if prereq in course_map:
                adjacency[prereq].append(course.code)
                indegree[course.code] += 1

    return adjacency, indegree


def topological_order(courses: List[Course]) -> List[str]:
    adjacency, indegree = build_adjacency(courses)
    queue = deque([code for code, deg in indegree.items() if deg == 0])
    order: List[str] = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adjacency.get(node, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return order


def find_cycles(courses: List[Course]) -> Tuple[bool, List[List[str]]]:
    adjacency, _ = build_adjacency(courses)
    visited: Dict[str, int] = {c.code: 0 for c in courses}
    stack: List[str] = []
    cycles: List[List[str]] = []

    def dfs(node: str):
        visited[node] = 1
        stack.append(node)
        for neighbor in adjacency.get(node, []):
            if visited[neighbor] == 0:
                dfs(neighbor)
            elif visited[neighbor] == 1:
                try:
                    idx = stack.index(neighbor)
                    cycles.append(stack[idx:] + [neighbor])
                except ValueError:
                    cycles.append([neighbor, node, neighbor])
        stack.pop()
        visited[node] = 2

    for course in courses:
        if visited[course.code] == 0:
            dfs(course.code)

    return len(cycles) > 0, cycles
