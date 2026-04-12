# C19 Drive Mode State Transition

## Context
This case models Eco, Normal, and Sport drive modes with transition guards and a fault fallback.

## Functional Requirements
- C19-RQ-001: The system shall support ECO, NORMAL, and SPORT drive modes.
- C19-RQ-002: The system shall accept a drive-mode change request only when accelerator pedal opening is less than 20 percent.
- C19-RQ-003: When a drive-mode fault is detected, the system shall return to NORMAL mode within 100 ms.

## Assumed Structure
- DriveModeSystem
- DriveModeController

## Main Signals / Interfaces
- acceleratorOpening (input, AcceleratorPort, AcceleratorValue)
- driveModeRequest (input, DriveModeRequestPort, DriveModeRequestValue)
- driveModeStatus (output, DriveModeStatusPort, DriveModeStatusValue)

## Coverage Tags
- category: state_machine
- difficulty: advanced
- completeness: high
