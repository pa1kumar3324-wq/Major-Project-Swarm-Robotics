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
    # 5. BATTERY MANAGEMENT
    # =========================
    battery_status = motors.get_battery_status()

    # Emergency: critical battery - return to base immediately
    if motors.is_battery_critical():
        base_position = (0.0, 0.0, 0.0)  # Rendezvous point at origin
        control = navigation.move_to(base_position, state)
        control = navigation.limit(control)
        motors.apply(control)
        continue

    # =========================
    # 6. TARGET SELECTION
    # =========================
    if battery_status["low_battery"]:
        # Low battery: head to rendezvous point
        rendezvous_point = (0.0, 0.0, 0.0)
        target = rendezvous_point
    else:
        # Normal operation: explore or go to victims
        target = exploration.choose_target(mapping)

    if target is None:
        motors.hover()
        continue

    # =========================
    # 7. NAVIGATION
    # =========================
    control = navigation.move_to(target, state)
    control = navigation.limit(control)

    # =========================
    # 8. VICTIM DETECTION
    # =========================
    victim = detection.check(state)
    if victim:
        comm.send_victim(victim["x"], victim["y"])

    # =========================
    # 9. PERIODIC COMMUNICATION
    # =========================
    if step_count % COMM_INTERVAL == 0:
        updates = mapping.get_recent_updates()
        for cell in updates:
            comm.send_map_update(cell["x"], cell["y"], cell["value"])

        # Share battery status with other drones
        comm.send_battery_status(battery_status["level"])

    if step_count % POSITION_INTERVAL == 0:
        x, y, _ = state["position"]
        comm.send_position(x, y)

    # =========================
    # 10. APPLY CONTROL
    # =========================
    motors.apply(control)

    # =========================
    # 10. DEBUG
    # =========================
    if step_count % 50 == 0:
        print(f"[{DRONE_ID}] Pos: {state['position']} Target: {target}")
