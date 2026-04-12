# C18 Regenerative Brake Inhibit at Low Temperature

## Context
This case applies different regenerative braking limits according to battery temperature.

## Functional Requirements
- C18-RQ-001: When battery temperature is below -10 degC, the system shall inhibit the HIGH regenerative braking level.
- C18-RQ-002: When battery temperature is below -20 degC, the system shall inhibit all regenerative braking levels.
- C18-RQ-003: The system shall restore the HIGH regenerative braking level only after battery temperature rises above -8 degC.

## Assumed Structure
- RegenBrakeSystem
- RegenBrakeController
- BatteryTemperatureMonitor

## Main Signals / Interfaces
- batteryTemperature (input, BatteryTemperaturePort, TemperatureValue)
- regenLevelCommand (output, RegenLevelPort, RegenLevelValue)

## Coverage Tags
- category: contextual_threshold
- difficulty: advanced
- completeness: high
