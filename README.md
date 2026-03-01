# Decentralized Swarm Drone System for Autonomous Search and Rescue

## Abstract

This project presents the design and simulation of a decentralized swarm drone system for autonomous search and rescue operations. Instead of relying on a single highly intelligent drone or a centralized controller, the system employs multiple autonomous drones operating under distributed control principles. Each drone makes decisions based solely on local perception and peer-to-peer communication, resulting in emergent collective intelligence.

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

The initial implementation is developed in Python using:

- NumPy for vector computations  
- Pygame for real-time visualization  

### Simulation Assumptions

- 2D bounded environment  
- Static obstacles  
- Static victim targets  
- Limited communication range  
- Identical drone software instances  

This controlled environment allows algorithm validation before real-world deployment.

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

- Python 3  
- NumPy  
- Pygame  
- Ubuntu Linux  
- Planned migration to ROS2  

## Implementation Roadmap

### Phase 1: Simulation
- Multi-agent motion implementation  
- Swarm coordination rules  
- Distributed exploration logic  

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

Pavan  
Undergraduate Computer Science Student  
Focus Areas: Robotics, Distributed Systems, Autonomous Intelligence  
