# C17 OTA Update Preconditions

## Context
This case models update-start gating and suspension conditions during an over-the-air software update.

## Requirements
- C17-RQ-001: The OTA update system shall start an update only when the vehicle is parked, doors are locked, and battery state of charge is at least 40 percent.
- C17-RQ-002: When ignition turns ON during an update, the system shall suspend the update within 1 s.
- C17-RQ-003: When any door is unlocked during an update, the system shall suspend the update within 1 s.

## Structure Hints
- OtaUpdateSystem
- UpdateManager
- VehicleConditionMonitor

## Interface Hints
- vehicleParked (input, VehicleParkPort, VehicleParkValue)
- doorsLocked (input, DoorLockStatusPort, DoorLockStatusValue)
- batterySoc (input, BatterySocPort, BatterySocValue)
- updateControl (output, UpdateControlPort, UpdateControlValue)

## Metadata
- category: multi_precondition
- difficulty: advanced
- completeness: high
