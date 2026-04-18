# Case 01: Vehicle quantitative and interface requirements

## Context
This requirement specification is a bottom-up reconstruction derived from the structure and requirement style seen in `VehicleModel.sysml`.

## Requirements
- REQ-VEH-001: The vehicle shall have a total mass less than or equal to 2000 kg.
- REQ-VEH-002: The vehicle shall maintain an average city fuel economy of at least 25 mpg in the nominal city driving scenario with an assumed cargo mass of at least 500 kg.
- REQ-VEH-003: The vehicle shall maintain an average highway fuel economy of at least 30 mpg in the nominal highway driving scenario with an assumed cargo mass of at least 500 kg.
- REQ-VEH-004: The engine shall transfer generated torque to the transmission through the clutch interface.

## Structure Hints
The system includes a vehicle, an engine, and a transmission.
