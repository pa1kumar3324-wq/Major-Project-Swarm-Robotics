import math

from controller import Robot


class Perception:
    def __init__(self, robot, timestep):
        self.robot = robot
        self.timestep = timestep

        self.gps = self._safe_device("gps")
        self.imu = self._safe_device("inertial unit")
        self.camera = self._safe_device("camera")
        self.front_distance = self._safe_device("front_distance")
        self.ground_distance = self._safe_device("ground_distance")

        if self.gps:
            self.gps.enable(timestep)
        if self.imu:
            self.imu.enable(timestep)
        if self.camera:
            self.camera.enable(timestep)
        if self.front_distance:
            self.front_distance.enable(timestep)
        if self.ground_distance:
            self.ground_distance.enable(timestep)

    def _safe_device(self, name):
        try:
            return self.robot.getDevice(name)
        except Exception:
            return None

    def update(self):
        if self.robot is None:
            return None

        position = self._get_position()
        orientation = self._get_orientation()
        front = self._get_value(self.front_distance)
        ground = self._get_value(self.ground_distance)
        victim_signal = self._detect_victim_signal()

        if position is None:
            return None

        return {
            "position": position,
            "orientation": orientation,
            "front_distance": front,
            "ground_distance": ground,
            "victim_signal": victim_signal,
        }

    def _get_position(self):
        """Return (plane_x, plane_y, altitude) using Webots Y-up world frame.

        Exploration and mapping use the horizontal X–Z plane; GPS returns (x, y, z)
        with y vertical, so we expose (x, z, y) for consistent 2D navigation.
        """
        if not self.gps:
            return None
        x, y, z = (float(v) for v in self.gps.getValues())
        if any(math.isnan(v) or math.isinf(v) for v in (x, y, z)):
            return None
        return (x, z, y)

    def _get_orientation(self):
        if self.imu:
            return tuple(self.imu.getRollPitchYaw())
        return (0.0, 0.0, 0.0)

    def _get_value(self, sensor):
        return sensor.getValue() if sensor else float("inf")

    def _detect_victim_signal(self):
        if self.camera is None:
            return False

        try:
            image = self.camera.getImage()
            width = self.camera.getWidth()
            height = self.camera.getHeight()
            center_x = width // 2
            center_y = height // 2
            pixel_index = center_x + center_y * width
            red = self.camera.imageGetRed(image, width, center_x, center_y)
            green = self.camera.imageGetGreen(image, width, center_x, center_y)
            blue = self.camera.imageGetBlue(image, width, center_x, center_y)

            if red > 200 and green < 150 and blue < 150:
                return True
        except Exception:
            pass

        return False
