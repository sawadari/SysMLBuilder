# C07 Battery Low Voltage Warning

## Context
This case monitors battery voltage, shows a warning, and reports a message after a debounce period.

## Requirements
- C07-RQ-001: When battery voltage is below 11.5 V for 5 s, the system shall turn on the low-voltage warning lamp.
- C07-RQ-002: The system shall send a low-voltage status message on the vehicle network within 100 ms after the warning lamp is turned on.
- C07-RQ-003: The system shall clear the warning after battery voltage is above 12.1 V for 10 s.

## Structure Hints
- BatteryWarningSystem
- BatteryMonitor
- WarningLamp
- NetworkPublisher

## Interface Hints
- batteryVoltage (input, VoltageInputPort, VoltageValue)
- lampCommand (output, LampCommandPort, LampCommandValue)
- statusMessage (output, NetworkStatusPort, NetworkStatusValue)

## Metadata
- category: threshold_monitoring
- difficulty: intermediate
- completeness: high
