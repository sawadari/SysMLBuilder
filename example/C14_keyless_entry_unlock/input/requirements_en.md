# C14 Keyless Entry Unlock

## Context
This case models valid key detection, unlock timing, and a lockout after repeated invalid attempts.

## Functional Requirements
- C14-RQ-001: When a valid key is within 1 m and the driver door handle is touched, the system shall unlock the driver door within 300 ms.
- C14-RQ-002: The system shall reject unlock requests from invalid keys.
- C14-RQ-003: When 5 invalid key attempts occur within 60 s, the system shall inhibit further keyless unlock processing for 5 min.

## Assumed Structure
- KeylessEntrySystem
- AccessController
- RfReceiver
- DoorLockActuator

## Main Signals / Interfaces
- validKeyPresent (input, KeyPresencePort, KeyPresenceValue)
- handleTouched (input, HandleTouchPort, HandleTouchValue)
- doorUnlockCommand (output, DoorLockCommandPort, DoorLockCommandValue)

## Coverage Tags
- category: timed_secure_access
- difficulty: advanced
- completeness: high
