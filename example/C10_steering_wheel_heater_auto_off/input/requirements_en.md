# C10 Steering Wheel Heater Auto-Off

## Context
This case combines ambient temperature gating with automatic timeout for steering wheel heating.

## Functional Requirements
- C10-RQ-001: The system shall reject a steering wheel heater request when ambient temperature is above 20 degC.
- C10-RQ-002: The system shall turn the steering wheel heater OFF after 30 min of continuous heating.
- C10-RQ-003: The system shall restore the heater to OFF after every ignition cycle.

## Assumed Structure
- SteeringWheelHeaterSystem
- SteeringWheelHeaterController
- SteeringWheelHeaterElement

## Main Signals / Interfaces
- ambientTemperature (input, AmbientTemperaturePort, TemperatureValue)
- heaterRequest (input, HeatingRequestPort, HeatingRequestValue)
- heatingLevelCommand (output, HeatingLevelPort, HeatingLevelValue)

## Coverage Tags
- category: contextual_threshold
- difficulty: basic
- completeness: high
