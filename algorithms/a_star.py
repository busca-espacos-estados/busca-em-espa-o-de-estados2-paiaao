import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        dist = 0
        for idx, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_idx = tile - 1
            r1, c1 = divmod(idx, 3)
            r2, c2 = divmod(goal_idx, 3)
            dist += abs(r1 - r2) + abs(c1 - c2)
        return dist

    def search(self, initial: State) -> SearchResult:
        from puzzle.result import SearchResult
        from itertools import count

        counter = count()
        open_heap = []
        g_scores = {initial.tiles: initial.cost}
        entry = (self.heuristic(initial) + initial.cost, next(counter), initial)
        heapq.heappush(open_heap, entry)

        closed = set()

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier = 1

        while open_heap:
            max_frontier = max(max_frontier, len(open_heap))
            _, _, node = heapq.heappop(open_heap)

            if node.tiles in closed:
                continue

            nodes_expanded += 1

            if node.is_goal:
                depth = len(node.path()) - 1
                return SearchResult(node, nodes_expanded, nodes_generated, max_frontier, depth)

            closed.add(node.tiles)

            for neigh in node.neighbors():
                if neigh.tiles in closed:
                    continue
                tentative_g = node.cost + 1
                prev_g = g_scores.get(neigh.tiles)
                if prev_g is None or tentative_g < prev_g:
                    neigh.cost = tentative_g
                    neigh.parent = node
                    g_scores[neigh.tiles] = tentative_g
                    f = tentative_g + self.heuristic(neigh)
                    heapq.heappush(open_heap, (f, next(counter), neigh))
                    nodes_generated += 1

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
