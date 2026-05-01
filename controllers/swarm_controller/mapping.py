import math
from utils import distance

class Mapping:
    def __init__(self, grid_resolution=1.0, grid_size=50):
        self.grid_resolution = grid_resolution
        self.grid_size = grid_size
        self.cells = {}
        self.victims = []
        self.drone_positions = {}
        self.recent_updates = []
        self.current_position = (0.0, 0.0, 0.0)

    def update(self, state):
        position = state.get("position")
        if position is None:
            return

        self.current_position = position
        cell = self._to_grid(position)
        self._set_cell(cell[0], cell[1], 0)

        if state.get("front_distance") is not None:
            distance_ahead = state["front_distance"]
            if distance_ahead < 2.0:
                obstacle_x = position[0] + math.cos(state["orientation"][2]) * distance_ahead
                obstacle_y = position[1] + math.sin(state["orientation"][2]) * distance_ahead
                self._set_cell(*self._to_grid((obstacle_x, obstacle_y, 0.0)), 1)

    def _to_grid(self, position):
        x, y, _ = position
        gx = int(round(x / self.grid_resolution))
        gy = int(round(y / self.grid_resolution))
        return gx, gy

    def _set_cell(self, x, y, value):
        key = (x, y)
        if self.cells.get(key) != value:
            self.cells[key] = value
            self.recent_updates.append({"x": x, "y": y, "value": value})

    def mark_victim(self, x, y):
        cell = self._to_grid((x, y, 0.0))
        if cell not in self.victims:
            self.victims.append(cell)
            self._set_cell(cell[0], cell[1], 2)

    def update_cell(self, x, y, value):
        grid = self._to_grid((x, y, 0.0))
        self._set_cell(grid[0], grid[1], value)

    def update_drone_position(self, drone_id, x, y):
        self.drone_positions[drone_id] = (x, y)

    def get_recent_updates(self):
        updates = self.recent_updates[:]
        self.recent_updates.clear()
        return updates

    def get_frontier_cells(self):
        frontier = []
        for (x, y), value in self.cells.items():
            if value == 0:
                for neighbor in self._neighbors(x, y):
                    if self.cells.get(neighbor) is None:
                        frontier.append((x * self.grid_resolution, y * self.grid_resolution, 0.0))
                        break
        return frontier

    def get_closest_victim(self):
        if not self.victims:
            return None
        current = self.current_position
        best = min(self.victims, key=lambda v: distance(current, (v[0], v[1], 0.0)))
        return (best[0] * self.grid_resolution, best[1] * self.grid_resolution, 0.0)

    def _neighbors(self, x, y):
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
