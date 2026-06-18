from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        from puzzle.result import SearchResult

        frontier = deque()
        frontier.append(initial)
        frontier_set = {initial.tiles}
        visited = set()

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier = 1

        while frontier:
            max_frontier = max(max_frontier, len(frontier))
            node = frontier.popleft()
            frontier_set.discard(node.tiles)
            nodes_expanded += 1

            if node.is_goal:
                depth = len(node.path()) - 1
                return SearchResult(node, nodes_expanded, nodes_generated, max_frontier, depth)

            visited.add(node.tiles)

            for neigh in node.neighbors():
                if neigh.tiles in visited or neigh.tiles in frontier_set:
                    continue
                frontier.append(neigh)
                frontier_set.add(neigh.tiles)
                nodes_generated += 1

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)