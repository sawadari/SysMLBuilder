# C08 CAN Heartbeat Timeout Reaction

## Context
This case reacts to a missing heartbeat from a brake controller by disabling a dependent function and storing a fault.

## Requirements
- C08-RQ-001: When the brake controller heartbeat is missing for 100 ms, the system shall set a communication-timeout fault.
- C08-RQ-002: The system shall disable cruise control within 50 ms after the communication-timeout fault is set.
- C08-RQ-003: The system shall store a diagnostic trouble code and send a fault status message within 100 ms.

## Structure Hints
- CommunicationMonitoringSystem
- HeartbeatMonitor
- CruiseControlGate
- DiagnosticManager

## Interface Hints
- heartbeat (input, HeartbeatPort, HeartbeatValue)
- cruiseEnable (output, FunctionControlPort, FunctionControlValue)
- diagnosticStatus (output, DiagnosticStatusPort, DiagnosticStatusValue)

## Metadata
- category: fault_reaction
- difficulty: advanced
- completeness: high
