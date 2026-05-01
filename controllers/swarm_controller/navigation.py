import math
from utils import clamp

class Navigation:
    def __init__(self, robot):
        self.robot = robot
        self.max_speed = 6.28

    def move_to(self, target, state):
        if state is None or target is None:
            return {"left": 0.0, "right": 0.0}

        position = state["position"]
        yaw = state["orientation"][2]

        dx = target[0] - position[0]
        dy = target[1] - position[1]
        distance = math.hypot(dx, dy)
        target_yaw = math.atan2(dy, dx)

        heading_error = self._normalize_angle(target_yaw - yaw)
        forward = clamp(distance * 0.5, -self.max_speed, self.max_speed)
        turn = clamp(heading_error * 2.0, -self.max_speed / 2.0, self.max_speed / 2.0)

        left = clamp(forward + turn, -self.max_speed, self.max_speed)
        right = clamp(forward - turn, -self.max_speed, self.max_speed)

        return {"left": left, "right": right}

    def limit(self, control):
        return {
            "left": clamp(control.get("left", 0.0), -self.max_speed, self.max_speed),
            "right": clamp(control.get("right", 0.0), -self.max_speed, self.max_speed),
        }

    def _normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle
