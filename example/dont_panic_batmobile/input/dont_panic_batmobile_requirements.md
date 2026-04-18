# Don't Panic Batmobile Public Sample

## Context
This Markdown document is a reverse-engineered requirement specification for the public SysML v2 Batmobile sample shown in "Don't Panic - The Absolute Beginners Guide to SysML v2".
The goal of this case is not to simplify the source model, but to provide a deterministic Markdown input that regenerates the same public `.sysml` sample text.

## Source Trace
- Book sample package: `Dont_Panic_Batmobile`
- Public model theme: structural modeling, behavioral modeling, use cases modelling, requirements modelling

## Requirements
- REQ-BAT-001: Define the core vehicle domain including Vehicle, Wheel, BatmobileEngine, PowerInterface, PowerIP, Power, and EngineCommand.
- REQ-BAT-002: Define the Batmobile system with seats, body, wheels, battery, engine, and the `bat2eng` power interface connection.
- REQ-BAT-003: Define specialization and variability elements including BatmobileNG, EngineChoices, WheelChoices, BatmobileConfigurations, and XBatmobile.
- REQ-BAT-004: Define the Batman and Hero related items and the `bm1` system occurrence with driving and charging timeslices.
- REQ-BAT-005: Define operational behavior including `Drive Batmobile`, `Activate rocket booster`, and `ActivateRocketBooster`.
- REQ-BAT-006: Define the VehicleMaxSpeed requirement, the batmobileSpecification requirements package, and the satisfy relation on `batmobileDesignV23`.
- REQ-BAT-007: Define concern, viewpoint, tabular view, and the `batmobileParts` exposed view filtered to non-standard library elements.
- REQ-BAT-008: Define the generic symbolic views `definition and usage`, `subclassification`, `subsetting`, `redefinition`, `structural Modeling`, `default value`, `timeslice modelling`, `behavioral modelling`, `use cases modelling`, `requirements modelling`, and top-level `index`.
