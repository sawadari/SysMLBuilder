# C13 Charge Flap Lock Control

## Context
This case locks and unlocks a charging flap based on driving and charging states.

## Functional Requirements
- C13-RQ-001: The system shall lock the charge flap while the vehicle is driving.
- C13-RQ-002: The system shall lock the charge flap while charging is active.
- C13-RQ-003: The system shall unlock the charge flap when the vehicle is parked and charging is complete or when a valid user unlock request is received.

## Assumed Structure
- ChargeFlapLockSystem
- ChargeFlapController
- ChargeFlapActuator

## Main Signals / Interfaces
- vehicleMoving (input, VehicleMotionPort, VehicleMotionValue)
- chargingActive (input, ChargingStatusPort, ChargingStatusValue)
- lockCommand (output, LockCommandPort, LockCommandValue)

## Coverage Tags
- category: contextual_locking
- difficulty: intermediate
- completeness: high
