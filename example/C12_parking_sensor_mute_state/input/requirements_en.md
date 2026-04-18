# C12 Parking Sensor Mute State

## Context
This case models a mute/unmute toggle and a power-cycle reset for parking sensor audio alerts.

## Requirements
- C12-RQ-001: Each valid mute-button press shall toggle the parking sensor audio alert state between MUTED and UNMUTED.
- C12-RQ-002: The system shall reset the audio alert state to UNMUTED at every power cycle.
- C12-RQ-003: The system shall preserve visual alerts while audio alerts are muted.

## Structure Hints
- ParkingSensorAlertSystem
- ParkingSensorController
- AudioBuzzer
- VisualDisplay

## Interface Hints
- muteButtonPressed (input, MuteButtonPort, MuteButtonValue)
- audioAlertCommand (output, AudioAlertPort, AudioAlertValue)
- visualAlertCommand (output, VisualAlertPort, VisualAlertValue)

## Metadata
- category: stateful_toggle
- difficulty: basic
- completeness: high
