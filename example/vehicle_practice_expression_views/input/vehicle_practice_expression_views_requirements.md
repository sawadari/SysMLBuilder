# Vehicle Practice Expression Views

## Context
This Markdown document is a deterministic requirement specification for a Cameo-oriented SysML v2 text-first practice model.
It is designed to output requirement, structure, action, and state-transition examples together with symbolic views that can be opened in Cameo.

## Source Trace
- Goal: use expression-based symbolic views where they reduce noise for text-first modeling
- Complementary goal: keep one interconnection view, one action-flow view, and one state-transition view for connector-oriented rendering

## Requirements
- REQ-VPV-001: Define a requirement package with a mass requirement and a requirements tree view that recursively exposes the requirement package.
- REQ-VPV-002: Define a structure package with parts, ports, an interface connection, parts tree views, and a parts-and-ports nested view that recursively exposes the structure package.
- REQ-VPV-003: Define an action behavior package with action definitions, an action usage with flow, and nested or tree action views that recursively expose the action package.
- REQ-VPV-004: Define a state behavior package with start and off signals, a controller state machine, and a states nested view that recursively exposes the state package.
- REQ-VPV-005: Define complementary render-based views for interconnection, action flow, and state transitions so the same model can be opened with connector-oriented renderers in Cameo.
