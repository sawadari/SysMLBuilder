# C02 Auto Window Anti-Pinch

## Context
This case models an automatic window feature with anti-pinch protection and a door-open inhibit condition.

## Requirements
- C02-RQ-001: The auto window system shall start automatic closing when the close switch is held for at least 300 ms.
- C02-RQ-002: The system shall inhibit automatic closing while the corresponding door is open.
- C02-RQ-003: When pinch is detected during automatic closing, the system shall stop within 30 ms and lower the glass by at least 100 mm.

## Structure Hints
- AutoWindowSystem
- WindowController
- WindowMotor
- PinchSensor

## Interface Hints
- closeRequest (input, WindowSwitchPort, WindowSwitchValue)
- doorOpen (input, DoorStatusPort, DoorStatusValue)
- pinchDetected (input, PinchSignalPort, PinchSignalValue)
- windowCommand (output, WindowMotorCommandPort, WindowMotorCommandValue)

## Metadata
- category: fault_reaction
- difficulty: intermediate
- completeness: high
