import random
from utils import distance

class Exploration:
    def __init__(self):
        self.last_target = None

    def choose_target(self, mapping):
        victim = mapping.get_closest_victim()
        if victim is not None:
            return victim

        frontier = mapping.get_frontier_cells()
        if frontier:
            return self._choose_best_frontier(frontier, mapping.current_position)

        return self._choose_random_goal(mapping.current_position)

    def _choose_best_frontier(self, frontier, current_position):
        best = min(frontier, key=lambda cell: distance(current_position, (cell[0], cell[1], 0.0)))
        self.last_target = best
        return best

    def _choose_random_goal(self, current_position):
        x, y, _ = current_position
        dx = random.uniform(-5.0, 5.0)
        dy = random.uniform(-5.0, 5.0)
        return (x + dx, y + dy)
