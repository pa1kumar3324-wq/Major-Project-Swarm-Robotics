import time

class Detection:
    def __init__(self):
        self.last_seen = None
        self.last_detection_time = 0
        self.detection_cooldown = 2.0  # seconds between detections
        self.victim_types = {
            "visual": {"detected": False, "confidence": 0.0},
            "thermal": {"detected": False, "confidence": 0.0},
            "motion": {"detected": False, "confidence": 0.0}
        }

    def check(self, state):
        if state is None:
            return None

        current_time = time.time()
        if current_time - self.last_detection_time < self.detection_cooldown:
            return None

        # Reset detection states
        for victim_type in self.victim_types.values():
            victim_type["detected"] = False
            victim_type["confidence"] = 0.0

        # Visual detection (camera-based)
        if state.get("victim_signal"):
            self.victim_types["visual"]["detected"] = True
            self.victim_types["visual"]["confidence"] = 0.8

        # Thermal detection (simulated - could be enhanced with actual thermal sensor)
        if self._check_thermal_signature(state):
            self.victim_types["thermal"]["detected"] = True
            self.victim_types["thermal"]["confidence"] = 0.6

        # Motion detection (based on distance sensor changes)
        if self._check_motion(state):
            self.victim_types["motion"]["detected"] = True
            self.victim_types["motion"]["confidence"] = 0.4

        # Determine if victim is detected based on combined confidence
        total_confidence = sum(v["confidence"] for v in self.victim_types.values() if v["detected"])
        detection_threshold = 0.5

        if total_confidence >= detection_threshold:
            x, y, _ = state["position"]
            victim_info = {
                "x": x,
                "y": y,
                "confidence": total_confidence,
                "types": [k for k, v in self.victim_types.items() if v["detected"]],
                "timestamp": current_time
            }
            self.last_seen = victim_info
            self.last_detection_time = current_time
            return victim_info

        return None

    def _check_thermal_signature(self, state):
        """Simulate thermal detection - in real implementation would use thermal camera"""
        # For simulation, we'll use a simple heuristic based on position and time
        # In a real system, this would analyze thermal camera data
        front_dist = state.get("front_distance", float('inf'))
        ground_dist = state.get("ground_distance", float('inf'))

        # Simulate thermal detection when close to obstacles (potential victims)
        if front_dist < 1.0 and ground_dist < 0.5:
            return True
        return False

    def _check_motion(self, state):
        """Detect motion through distance sensor changes"""
        # This would require storing previous sensor readings
        # For now, we'll use a simple heuristic
        front_dist = state.get("front_distance", float('inf'))
        if front_dist < 0.8:  # Very close detection
            return True
        return False
