import time

class Motors:
    def __init__(self, robot):
        try:
            self.left_motor = robot.getDevice("motor1")
            self.right_motor = robot.getDevice("motor2")
        except (AttributeError, TypeError) as e:
            raise RuntimeError(
                "Expected differential-drive motors named motor1 and motor2 on the Robot node."
            ) from e

        for motor in (self.left_motor, self.right_motor):
            motor.setPosition(float("inf"))
            motor.setVelocity(0.0)

        # Battery management
        self.battery_level = 100.0  # percentage
        self.battery_capacity = 3600.0  # seconds of full operation
        self.last_update_time = time.time()
        self.efficiency_factor = 1.0
        self.low_battery_threshold = 20.0

    def apply(self, control):
        current_time = time.time()
        dt = current_time - self.last_update_time

        # Calculate power consumption based on motor activity
        left_speed = control.get("left", 0.0)
        right_speed = control.get("right", 0.0)

        # Power consumption proportional to speed and time
        power_used = (abs(left_speed) + abs(right_speed)) * dt * 0.01

        # Reduce battery level
        self.battery_level = max(0.0, self.battery_level - power_used)

        # Apply efficiency factor (reduced performance when battery is low)
        if self.battery_level < self.low_battery_threshold:
            self.efficiency_factor = 0.5 + (self.battery_level / self.low_battery_threshold) * 0.5
        else:
            self.efficiency_factor = 1.0

        # Apply motors with efficiency factor
        actual_left_speed = left_speed * self.efficiency_factor
        actual_right_speed = right_speed * self.efficiency_factor

        self.left_motor.setVelocity(actual_left_speed)
        self.right_motor.setVelocity(actual_right_speed)

        self.last_update_time = current_time

    def hover(self):
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

    def get_battery_status(self):
        """Return battery level and efficiency factor"""
        return {
            "level": self.battery_level,
            "efficiency": self.efficiency_factor,
            "low_battery": self.battery_level < self.low_battery_threshold
        }

    def is_battery_critical(self):
        """Check if battery is critically low"""
        return self.battery_level < 10.0
