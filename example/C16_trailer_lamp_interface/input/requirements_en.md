# C16 Trailer Lamp Interface

## Context
This case focuses on typed signal interfaces between the trailer controller and the trailer lamp connector.

## Requirements
- C16-RQ-001: The trailer lamp controller shall output left-turn, right-turn, and stop-lamp commands on the trailer connector interface.
- C16-RQ-002: The system shall detect trailer disconnect within 500 ms after connector continuity is lost.
- C16-RQ-003: The system shall suppress trailer-lamp commands when no trailer is detected.

## Structure Hints
- TrailerLampSystem
- TrailerLampController
- TrailerConnector

## Interface Hints
- leftTurnLampCommand (output, LeftTurnLampPort, LampCommandValue)
- rightTurnLampCommand (output, RightTurnLampPort, LampCommandValue)
- stopLampCommand (output, StopLampPort, LampCommandValue)
- trailerDetected (input, TrailerPresencePort, TrailerPresenceValue)

## Metadata
- category: interface_contract
- difficulty: intermediate
- completeness: high
