# C20 Washer Low Fluid Warning

## Context
This case shows a warning after low fluid is detected with debounce and clears it after refill.

## Requirements
- C20-RQ-001: When washer fluid level is low for 2 s, the system shall display a low-fluid warning within 500 ms.
- C20-RQ-002: The system shall not display the warning for transient low-level detections shorter than 2 s.
- C20-RQ-003: The system shall clear the warning after fluid level is normal for 5 s.

## Structure Hints
- WasherFluidWarningSystem
- FluidLevelMonitor
- ClusterDisplay

## Interface Hints
- fluidLow (input, FluidLevelPort, FluidLevelValue)
- displayCommand (output, DisplayCommandPort, DisplayCommandValue)

## Metadata
- category: threshold_monitoring
- difficulty: basic
- completeness: high
