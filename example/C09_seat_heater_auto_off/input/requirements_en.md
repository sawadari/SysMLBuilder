# C09 Seat Heater Auto-Off

## Context
This case models a seat heater that steps down and turns off after timed operation.

## Functional Requirements
- C09-RQ-001: The seat heater shall allow the HIGH level immediately after user activation.
- C09-RQ-002: After 30 min of continuous HIGH operation, the system shall change the level from HIGH to MEDIUM.
- C09-RQ-003: After 60 min of total heating operation, the system shall turn the seat heater OFF.

## Assumed Structure
- SeatHeaterSystem
- SeatHeaterController
- SeatHeaterElement

## Main Signals / Interfaces
- heaterRequest (input, HeatingRequestPort, HeatingRequestValue)
- heatingLevelCommand (output, HeatingLevelPort, HeatingLevelValue)

## Coverage Tags
- category: timed_state_change
- difficulty: basic
- completeness: high
