# C05 Rear Wiper Reverse Link

## Context
This case links a rear wiper one-wipe action to reverse gear when the front wiper is already active.

## Requirements
- C05-RQ-001: When reverse gear is engaged while the front wiper is active, the system shall command one rear-wiper wipe within 1 s.
- C05-RQ-002: The system shall not issue more than one reverse-linked rear-wiper wipe within 10 s.
- C05-RQ-003: The system shall disable the reverse-linked wipe while the rear wiper service mode is active.

## Structure Hints
- RearWiperLinkSystem
- RearWiperController
- RearWiperMotor

## Interface Hints
- frontWiperActive (input, WiperStatusPort, WiperStatusValue)
- shiftPosition (input, ShiftPositionPort, ShiftPositionValue)
- rearWiperCommand (output, WiperCommandPort, WiperCommandValue)

## Metadata
- category: contextual_trigger
- difficulty: basic
- completeness: high
