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

    def apply(self, control):
        left_speed = control.get("left", 0.0)
        right_speed = control.get("right", 0.0)
        self.left_motor.setVelocity(left_speed)
        self.right_motor.setVelocity(right_speed)

    def hover(self):
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)
