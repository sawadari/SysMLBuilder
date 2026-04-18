# C01 Power Tailgate Opening Conditions

## Context
This case describes a power tailgate that checks vehicle conditions before opening and reacts to obstacles during closing.

## Functional Requirements
- C01-RQ-001: The power tailgate system shall accept an open request only when vehicle speed is less than 3 km/h and shift position is P.
- C01-RQ-002: After a valid close request, the system shall start closing within 200 ms.
- C01-RQ-003: When an obstacle is detected during closing, the system shall stop within 50 ms and reverse for at least 200 ms.

## Assumed Structure
- PowerTailgateSystem
- TailgateController
- TailgateActuator
- ObstacleSensor

## Main Signals / Interfaces
- vehicleSpeed (input, VehicleSpeedPort, VehicleSpeedValue)
- shiftPosition (input, ShiftPositionPort, ShiftPositionValue)
- tailgateCommand (output, TailgateCommandPort, TailgateCommandValue)
- obstacleDetected (input, ObstacleSignalPort, ObstacleSignalValue)

## Coverage Tags
- category: timed_response
- difficulty: intermediate
- completeness: high
