# C04 Headlamp Auto-Off Delay

## Context
This case covers delayed headlamp shutoff after ignition off and manual cancellation of the timer.

## Requirements
- C04-RQ-001: When ignition turns OFF and the driver door is closed, the system shall turn off the headlamps after 30 s.
- C04-RQ-002: The system shall cancel the auto-off timer when the user manually switches the headlamps ON again.
- C04-RQ-003: The system shall keep the headlamps ON while the driver door is open.

## Structure Hints
- HeadlampControlSystem
- HeadlampController
- HeadlampRelay

## Interface Hints
- ignitionOn (input, IgnitionStatusPort, IgnitionStatusValue)
- driverDoorOpen (input, DoorStatusPort, DoorStatusValue)
- lampCommand (output, LampCommandPort, LampCommandValue)

## Metadata
- category: timed_response
- difficulty: basic
- completeness: high
