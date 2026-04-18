# C11 Lane Departure Warning

## Context
This case triggers an audible warning when lane departure occurs under valid operating conditions.

## Requirements
- C11-RQ-001: When lane departure is detected at vehicle speed of at least 60 km/h and the turn signal is OFF, the system shall generate an audible warning within 150 ms.
- C11-RQ-002: The system shall suppress the warning while the turn signal is active.
- C11-RQ-003: The system shall stop the audible warning within 300 ms after the lane departure condition is cleared.

## Structure Hints
- LaneDepartureWarningSystem
- LaneMonitor
- Buzzer

## Interface Hints
- vehicleSpeed (input, VehicleSpeedPort, VehicleSpeedValue)
- turnSignalActive (input, TurnSignalPort, TurnSignalValue)
- laneDepartureDetected (input, LaneDeparturePort, LaneDepartureValue)
- buzzerCommand (output, BuzzerCommandPort, BuzzerCommandValue)

## Metadata
- category: multi_condition_alert
- difficulty: intermediate
- completeness: high
