class Detection:
    def __init__(self, threshold=1.0):
        self.threshold = threshold
        self.last_seen = None

    def check(self, state):
        if state is None:
            return None

        if state.get("victim_signal"):
            x, y, _ = state["position"]
            self.last_seen = {"x": x, "y": y}
            return self.last_seen

        if state.get("front_distance") is not None and state["front_distance"] < self.threshold:
            x, y, _ = state["position"]
            self.last_seen = {"x": x, "y": y}
            return self.last_seen

        return None
