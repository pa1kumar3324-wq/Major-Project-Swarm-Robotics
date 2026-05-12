import random
import math
from utils import distance

class Exploration:
    def __init__(self):
        self.last_target = None
        self.exploration_history = []
        self.max_history_size = 20
        self.information_gain_weight = 0.7
        self.distance_weight = 0.3

    def choose_target(self, mapping):
        # Priority 1: Go to closest known victim
        victim = mapping.get_closest_victim()
        if victim is not None:
            self._add_to_history(victim)
            return victim

        # Priority 2: Explore frontier cells with information gain consideration
        frontier = mapping.get_frontier_cells()
        if frontier:
            best_target = self._choose_best_frontier(frontier, mapping)
            if best_target:
                self._add_to_history(best_target)
                return best_target

        # Priority 3: Random exploration with bounds checking
        return self._choose_random_goal(mapping.current_position)

    def _choose_best_frontier(self, frontier, current_position):
        if not frontier:
            return None

        scored_frontiers = []
        for cell in frontier:
            score = self._score_frontier_cell(cell, current_position, frontier)
            scored_frontiers.append((cell, score))

        # Sort by score (higher is better)
        scored_frontiers.sort(key=lambda x: x[1], reverse=True)

        best_cell = scored_frontiers[0][0]
        self.last_target = best_cell
        return best_cell

    def _score_frontier_cell(self, cell, current_position, all_frontiers):
        """Score frontier cells based on multiple factors"""
        cell_x, cell_y = cell

        # Distance cost (closer is better, but not overwhelming)
        dist = distance(current_position, (cell_x, cell_y, 0.0))
        distance_score = 1.0 / (1.0 + dist * 0.1)  # Normalized distance score

        # Information gain (cells near other frontiers might reveal more area)
        nearby_frontiers = sum(1 for fx, fy in all_frontiers
                              if abs(fx - cell_x) <= 1 and abs(fy - cell_y) <= 1)
        info_gain_score = min(nearby_frontiers / 5.0, 1.0)  # Cap at 1.0

        # Avoid recently visited areas
        recency_penalty = self._calculate_recency_penalty(cell)

        # Combine scores
        total_score = (self.distance_weight * distance_score +
                      self.information_gain_weight * info_gain_score -
                      recency_penalty)

        return max(0, total_score)  # Ensure non-negative

    def _calculate_recency_penalty(self, cell):
        """Penalize cells near recently visited locations"""
        penalty = 0.0
        cell_x, cell_y = cell

        for i, (hx, hy, _) in enumerate(self.exploration_history[-5:]):  # Last 5 visits
            dist_to_history = math.sqrt((hx - cell_x)**2 + (hy - cell_y)**2)
            if dist_to_history < 2.0:  # Within 2 units
                # More recent visits have higher penalty
                penalty += (5 - i) * 0.1

        return penalty

    def _add_to_history(self, target):
        """Add target to exploration history"""
        if len(self.exploration_history) >= self.max_history_size:
            self.exploration_history.pop(0)
        self.exploration_history.append(target)

    def _choose_random_goal(self, current_position):
        """Generate a random goal with improved bounds and safety"""
        x, y, _ = current_position

        # Adaptive exploration range based on current position
        exploration_radius = 8.0

        # Add some directional bias to encourage coverage
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(2.0, exploration_radius)

        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)

        nx, ny = x + dx, y + dy

        # World bounds (from the world file, ground is 80x80)
        limit = 35.0  # Leave some margin from the 40 unit limit

        # Ensure we stay within bounds
        nx = max(-limit, min(limit, nx))
        ny = max(-limit, min(limit, ny))

        return (nx, ny, 0.0)
