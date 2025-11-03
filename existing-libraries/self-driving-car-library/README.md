# Self-Driving Car Library

A comprehensive Python library for autonomous vehicle research, providing modular components for perception, planning, control, simulation, and sensor processing.

---

## 📁 Library Structure

### **Control Module**

#### `main.py`

This module implements PID control for vehicle lateral and longitudinal control.

- **Class `PIDController`**

  - Implements proportional-integral-derivative control algorithm.
  - Supports separate controllers for steering and throttle/brake.
  - Includes anti-windup and derivative filtering.
  - Configurable gains ($K_p$, $K_i$, $K_d$) for different scenarios.

- **Key Methods**

  - `compute(error, dt)`: Computes control output from error.
  - `process_frame(frame)`: Detect a horizontal line in the bottom region of the frame and compute lateral error.

### **Datasets Module**

#### `data`
#### `self_driving_car/sign`
#### `stop-sign-detection/..`

This module contains all photos needed for training

---