class Detection:
    def __init__(self):
        self.last_seen = None

    def check(self, state):
        if state is None:
            return None

        if state.get("victim_signal"):
            x, y, _ = state["position"]
            self.last_seen = {"x": x, "y": y}
            return self.last_seen

        return None
