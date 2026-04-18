# C15 Child Lock Shift Interlock

## Context
This case allows child-lock state changes only under safe vehicle conditions.

## Requirements
- C15-RQ-001: The system shall allow child-lock activation only when shift position is P and vehicle speed is 0 km/h.
- C15-RQ-002: The system shall reject child-lock activation while any rear door is open.
- C15-RQ-003: When a valid child-lock deactivation request is received, the system shall complete the deactivation within 500 ms.

## Structure Hints
- ChildLockSystem
- ChildLockController
- RearDoorLockActuator

## Interface Hints
- shiftPosition (input, ShiftPositionPort, ShiftPositionValue)
- vehicleSpeed (input, VehicleSpeedPort, VehicleSpeedValue)
- rearDoorOpen (input, DoorStatusPort, DoorStatusValue)
- childLockCommand (output, LockCommandPort, LockCommandValue)

## Metadata
- category: gated_capability
- difficulty: basic
- completeness: high
