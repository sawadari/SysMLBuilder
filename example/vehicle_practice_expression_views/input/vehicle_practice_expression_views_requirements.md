# Vehicle Practice Expression Views

## Context
This document is a human-authored requirement specification for a small SysML v2 practice model that is easy to inspect in Cameo.
The model should stay simple and deterministic. The goal is not a production architecture but a compact sample that demonstrates requirement, structure, action, and state views from one text-first source.

## Goal
The sample should give a beginner a single `.sysml` file that can be imported into Cameo and used to inspect:

- a small requirement hierarchy
- a small structural model with one explicit connection
- a small action flow
- a small state machine
- several symbolic views that match those concerns

## Context
- Requirements
  The sample should include one requirement definition for mass checking and one requirement hierarchy that applies it to a vehicle and an engine.
- Structure
  The sample should include a small vehicle structure with an engine, a transmission, one drive power port type, and one engine-to-transmission interface.
- Behavior (actions)
  The sample should include one action flow that generates torque and transfers it.
- Behavior (states)
  The sample should include one controller with a simple off/on state machine driven by start and off signals.

## Authoring Notes
- The package and view names are fixed by the companion `case.yaml`.
- The Markdown should explain intent in plain language.
- The Markdown does not need to restate every SysML token as long as the desired model content is clear.

## Requirements
- [REQ-VPV-001] The sample shall provide a requirement package that checks actual mass against limit mass for both a vehicle and an engine.
- [REQ-VPV-002] The sample shall provide a structural package with a vehicle, an engine, a transmission, one drive-power port type, and one explicit engine-to-transmission interface.
- [REQ-VPV-003] The structural package shall also include a concrete vehicle part usage so that tree, nested, and interconnection views have something to expose.
- [REQ-VPV-004] The sample shall provide an action package in which torque is generated and then transferred through one explicit flow.
- [REQ-VPV-005] The sample shall provide a state package in which a controller moves between `off` and `on` in response to start and off signals.
- [REQ-VPV-006] The sample shall provide a requirements tree view for the requirements package.
- [REQ-VPV-007] The sample shall provide structural views for parts tree, parts nested, parts and ports nested, and system interconnection.
- [REQ-VPV-008] The sample shall provide action views for actions nested, actions tree, and action flow.
- [REQ-VPV-009] The sample shall provide state views for states nested and state transition.
- [REQ-VPV-010] The sample shall remain Cameo-oriented, so the views should be useful after `Display > Display Exposed Elements`, and connector-focused views should also work with `Display > Display Connectors` when needed.
