from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 
              4, 5, 6, 
              7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        neighbors: List[State] = []
        idx = self.blank_index
        row, col = divmod(idx, 3)

        moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
        for dr, dc, action in moves:
            new_r, new_c = row + dr, col + dc
            if 0 <= new_r < 3 and 0 <= new_c < 3:
                new_idx = new_r * 3 + new_c
                tiles_list = list(self.tiles)
                tiles_list[idx], tiles_list[new_idx] = tiles_list[new_idx], tiles_list[idx]
                new_state = State(tuple(tiles_list), parent=self, action=action, cost=self.cost + 1)
                neighbors.append(new_state)

        return neighbors

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        node: Optional[State] = self
        path: List[State] = []
        while node is not None:
            path.append(node)
            node = node.parent
        path.reverse()
        return path

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        p = self.path()
        # skip the initial state's action (None)
        actions: List[str] = [s.action for s in p[1:] if s.action is not None]
        return actions

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
