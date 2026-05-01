import json
from utils import serialize_message, deserialize_message

class Communication:
    def __init__(self, robot, timestep):
        self.robot = robot
        self.emitter = robot.getDevice("emitter")
        self.receiver = robot.getDevice("receiver")
        self.receiver.enable(timestep)

    def send(self, message):
        payload = serialize_message(message)
        self.emitter.send(payload)

    def receive(self):
        messages = []
        while self.receiver.getQueueLength() > 0:
            raw = self.receiver.getData().decode("utf-8")
            message = deserialize_message(raw)
            if message is not None:
                messages.append(message)
            self.receiver.nextPacket()
        return messages

    def send_map_update(self, x, y, value):
        self.send({"type": "map", "id": self.robot.getName(), "x": x, "y": y, "value": value})

    def send_position(self, x, y):
        self.send({"type": "position", "id": self.robot.getName(), "x": x, "y": y})

    def send_victim(self, x, y):
        self.send({"type": "victim", "id": self.robot.getName(), "x": x, "y": y})
