from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        from puzzle.result import SearchResult

        stack = [initial]
        stack_set = {initial.tiles}
        visited = set()

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier = 1

        while stack:
            max_frontier = max(max_frontier, len(stack))
            node = stack.pop()
            stack_set.discard(node.tiles)
            nodes_expanded += 1

            if node.is_goal:
                depth = len(node.path()) - 1
                return SearchResult(node, nodes_expanded, nodes_generated, max_frontier, depth)

            if node.tiles in visited:
                continue
            visited.add(node.tiles)

            children = node.neighbors()
            for child in reversed(children):
                if child.tiles in visited or child.tiles in stack_set:
                    continue
                if child.cost > self.depth_limit:
                    continue
                stack.append(child)
                stack_set.add(child.tiles)
                nodes_generated += 1

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
