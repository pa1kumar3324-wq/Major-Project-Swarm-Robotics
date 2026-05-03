# Decentralized Swarm Drone System for Autonomous Search and Rescue

## Abstract

This project presents the design and simulation of a decentralized swarm drone system for autonomous search and rescue operations. Instead of relying on a single highly intelligent drone or a centralized command structure, we employ a swarm of simple, autonomous drones that coordinate through local interactions.

The objective is to develop a scalable, fault-tolerant, and platform-agnostic swarm framework that can be validated in simulation and later deployed on real aerial robotic platforms.

---

## Problem Statement

Search and rescue missions in disaster scenarios such as earthquakes, floods, and collapsed structures face several operational challenges:

- Limited communication infrastructure  
- High risk to human responders  
- Inefficient centralized coordination  
- Single-point failures in traditional systems  

Current drone-based rescue systems typically rely on manual control or centralized command structures. These approaches reduce scalability and increase vulnerability to communication breakdowns.

This project proposes a decentralized swarm-based approach to address these limitations.

---

## Project Objectives

### Primary Objectives

1. Design a decentralized multi-agent swarm architecture.
2. Implement distributed coordination without a central controller.
3. Develop autonomous area coverage and exploration strategies.
4. Integrate victim detection mechanisms.
5. Demonstrate fault tolerance under drone failure conditions.

### Secondary Objectives

1. Ensure scalability from small to large drone groups.
2. Maintain platform independence for future hardware deployment.
3. Measure performance using quantitative evaluation metrics.
4. Prepare the system for migration to ROS2 and real drone hardware.

---

## Core Design Principles

### 1. Decentralization
No global controller or master node exists. Each drone operates independently using local information.

### 2. Local Perception
Drones respond only to:
- Nearby drones within a communication radius
- Local sensor data
- Detected targets within sensing range

### 3. Emergent Intelligence
Complex collective behavior emerges from simple local interaction rules.

### 4. Fault Tolerance
The swarm continues functioning even if individual drones fail.

### 5. Scalability
The system architecture remains unchanged when scaling the number of drones.

---

## System Architecture

### Drone State Model

Each drone maintains the following internal state:

- Unique ID  
- Position (x, y, z)  
- Velocity (vx, vy, vz)  
- Battery level  
- Operational mode (searching, assisting, idle)  

### Perception Inputs

Each drone processes:

- Neighbor positions and velocities within radius R  
- Obstacle distance data  
- Victim detection signals  
- GPS coordinates  

### Communication Model

Each drone broadcasts:

- Current position  
- Velocity  
- Battery status  
- Detection events  

Communication is local and range-based. No drone has access to global state.

---

## Behavioral Layers

### 1. Motion Layer
Implements collision avoidance and swarm cohesion using Boids-inspired rules:

- Separation  
- Alignment  
- Cohesion  

### 2. Search Layer
Implements distributed area coverage strategies such as:

- Voronoi-based partitioning  
- Frontier-based exploration  
- Adaptive region reassignment upon drone failure  

### 3. Rescue Layer

Upon victim detection:

1. Drone records coordinates  
2. Broadcasts alert to nearby drones  
3. Nearest drones transition to assist mode  
4. Remaining drones continue exploration  

---

## Simulation Environment

### Webots (3D SAR scene)

The repository includes a **Webots** world that models a collapsed-building search area with debris, voids, and multiple **red sphere “victim” markers** for camera-based detection.

- **World:** `worlds/collapsed_rescue.wbt` — ground terrain, rubble, tunnel, and named victim solids.
- **Agents:** three differential-drive **SwarmDrone** robots (`drone0`, `drone1`, `drone2`) defined in the same file via a `PROTO`. Each robot runs the Python controller `swarm_controller` and is equipped with GPS, inertial unit, forward and ground distance sensors, camera, and emitter/receiver on a shared channel for decentralized map and victim updates.
- **Coordinates:** Webots uses a **Y-up** world frame. The controller maps GPS readings to a **horizontal exploration plane** `(x, z)` (stored as `position` with components `(plane_x, plane_y, altitude)` in Python) so mapping, navigation, and shared positions stay consistent on the ground.
- **Victim detection:** alerts are raised from **camera color cues** (strong red in view). Proximity to obstacles is **not** treated as a victim.

**Running the simulation:** Open Webots, set the **project directory** to this repository root (the folder that contains `worlds/` and `controllers/`), then open `worlds/collapsed_rescue.wbt` and run. Webots resolves `controller "swarm_controller"` to `controllers/swarm_controller/`.

### Original 2D prototype (reference)

An earlier design target used Python with NumPy and Pygame for a **2D** bounded environment. That layout is not present in this repository snapshot; the **authoritative runnable simulation here is Webots**.

### Simulation Assumptions

- Bounded environment (large ground slab in Webots; 2D in the Pygame design)  
- Static obstacles and victim targets  
- Local radio-style messaging (emitter/receiver range in Webots)  
- Identical controller software on each agent  

This controlled environment supports algorithm validation before real-world deployment.

---

## Performance Metrics

The system is evaluated using:

- Area coverage percentage  
- Time to victim detection  
- Redundancy rate (duplicate coverage)  
- Energy efficiency  
- Communication overhead  
- Recovery time after drone failure  

These metrics enable quantitative assessment of swarm intelligence.

---

## Technology Stack

- Python 3 (Webots controller API)  
- [Webots](https://cyberbotics.com/) — 3D physics and sensors  
- NumPy / Pygame — referenced for an optional 2D prototype path  
- Ubuntu Linux (typical for Webots; Windows/macOS also supported by Webots)  
- Planned migration to ROS2  

## Directory Structure

```
Major-Project-Swarm-Robotics/
├── README.md
├── worlds/
│   └── collapsed_rescue.wbt    # SAR scene + SwarmDrone PROTO and instances
└── controllers/
    └── swarm_controller/         # Python controller (one process per robot)
        ├── swarm_controller.py   # Main loop: perception → mapping → comm → explore → navigate
        ├── perception.py         # GPS / IMU / camera / distance sensors
        ├── mapping.py            # Local grid map and shared updates
        ├── communication.py      # Emitter / receiver JSON messages
        ├── exploration.py        # Frontier and goal selection
        ├── navigation.py         # Differential-drive command generation
        ├── detection.py          # Victim cue from camera
        ├── motors.py             # motor1 / motor2 velocity control
        └── utils.py              # Serialization, clamp, distance helpers
```

## Implementation Roadmap

### Phase 1: Simulation
- Multi-agent motion in **Webots** (differential drive, sensors, local radio)  
- Swarm coordination rules and shared mapping in the Python controller  
- Distributed exploration logic (frontiers, random goals within arena bounds)  

### Phase 2: Advanced Autonomy
- Victim detection integration  
- Failure simulation  
- Communication optimization  

### Phase 3: Hardware Migration
- ROS2 integration  
- Single drone autonomy testing  
- Multi-drone field validation  

---

## Research Domains Involved

- Swarm Robotics  
- Multi-Agent Systems  
- Distributed Algorithms  
- Autonomous Systems  
- Computer Vision (for detection layer)  
- Embedded Systems  

Machine learning is used only for perception tasks such as victim detection. Core swarm intelligence remains deterministic and explainable.

---

## Future Work

- Real-time mapping integration  
- Reinforcement learning for adaptive search optimization  
- Dynamic obstacle environments  
- Hardware implementation on aerial drone platforms  
- Field testing under controlled disaster simulation scenarios  

---

## Author

Pavan Kumar MG.  
Team Lead, Swarm Drones
