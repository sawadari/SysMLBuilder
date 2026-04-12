# C06 Climate Defog Priority

## Context
This case coordinates blower level, compressor state, and outlet mode when front defog is requested.

## Functional Requirements
- C06-RQ-001: When front defog is requested, the HVAC system shall set blower level to 5 or higher within 500 ms.
- C06-RQ-002: The system shall command the air outlet mode to windshield mode while front defog is active.
- C06-RQ-003: The system shall turn the air conditioner ON while front defog is active unless compressor protection is active.

## Assumed Structure
- ClimateDefogSystem
- HvacController
- BlowerActuator
- AirMixActuator
- CompressorRelay

## Main Signals / Interfaces
- defogRequest (input, DefogRequestPort, DefogRequestValue)
- blowerCommand (output, BlowerCommandPort, BlowerCommandValue)
- outletModeCommand (output, OutletModePort, OutletModeValue)
- acCommand (output, AcCommandPort, AcCommandValue)

## Coverage Tags
- category: multi_action_response
- difficulty: intermediate
- completeness: high
