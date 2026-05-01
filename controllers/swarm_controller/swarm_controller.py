from controller import Robot
from perception import Perception
from communication import Communication
from mapping import Mapping
from navigation import Navigation
from exploration import Exploration
from detection import Detection
from motors import Motors

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Unique drone ID (simple version)
DRONE_ID = robot.getName()

# Modules
perception = Perception(robot, timestep)
mapping = Mapping()
comm = Communication(robot, timestep)
navigation = Navigation(robot)
exploration = Exploration()
detection = Detection()
motors = Motors(robot)

# Timing control
step_count = 0
COMM_INTERVAL = 10        # send data every 10 steps
POSITION_INTERVAL = 15    # send position less frequently

while robot.step(timestep) != -1:
    step_count += 1

    # =========================
    # 1. PERCEPTION
    # =========================
    state = perception.update()
    if state is None:
        motors.hover()
        continue

    # =========================
    # 2. LOCAL MAP UPDATE
    # =========================
    mapping.update(state)

    # =========================
    # 3. RECEIVE MESSAGES
    # =========================
    messages = comm.receive()

    # =========================
    # 4. INTEGRATE SHARED DATA
    # =========================
    for msg in messages:
        if msg.get("type") == "victim":
            mapping.mark_victim(msg.get("x"), msg.get("y"))
        elif msg.get("type") == "map":
            mapping.update_cell(msg.get("x"), msg.get("y"), msg.get("value"))
        elif msg.get("type") == "position":
            mapping.update_drone_position(msg.get("id"), msg.get("x"), msg.get("y"))

    # =========================
    # 5. TARGET SELECTION
    # =========================
    target = exploration.choose_target(mapping)
    if target is None:
        motors.hover()
        continue

    # =========================
    # 6. NAVIGATION
    # =========================
    control = navigation.move_to(target, state)
    control = navigation.limit(control)

    # =========================
    # 7. VICTIM DETECTION
    # =========================
    victim = detection.check(state)
    if victim:
        comm.send_victim(victim["x"], victim["y"])

    # =========================
    # 8. PERIODIC COMMUNICATION
    # =========================
    if step_count % COMM_INTERVAL == 0:
        updates = mapping.get_recent_updates()
        for cell in updates:
            comm.send_map_update(cell["x"], cell["y"], cell["value"])

    if step_count % POSITION_INTERVAL == 0:
        x, y, _ = state["position"]
        comm.send_position(x, y)

    # =========================
    # 9. APPLY CONTROL
    # =========================
    motors.apply(control)

    # =========================
    # 10. DEBUG
    # =========================
    if step_count % 50 == 0:
        print(f"[{DRONE_ID}] Pos: {state['position']} Target: {target}")
