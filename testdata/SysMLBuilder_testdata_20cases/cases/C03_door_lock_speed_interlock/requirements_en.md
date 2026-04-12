# C03 Door Lock Speed Interlock

## Context
This case models automatic door locking and unlocking based on speed, shift position, and door status.

## Functional Requirements
- C03-RQ-001: The door lock system shall lock all doors when vehicle speed is at least 20 km/h for 3 s.
- C03-RQ-002: The system shall not perform automatic locking while any door is ajar.
- C03-RQ-003: When ignition is OFF and shift position changes to P, the system shall unlock the driver door within 500 ms.

## Assumed Structure
- DoorLockSystem
- DoorLockController
- DoorLockActuator

## Main Signals / Interfaces
- vehicleSpeed (input, VehicleSpeedPort, VehicleSpeedValue)
- doorAjar (input, DoorStatusPort, DoorStatusValue)
- shiftPosition (input, ShiftPositionPort, ShiftPositionValue)
- lockCommand (output, DoorLockCommandPort, DoorLockCommandValue)

## Coverage Tags
- category: timed_gated_capability
- difficulty: basic
- completeness: high
