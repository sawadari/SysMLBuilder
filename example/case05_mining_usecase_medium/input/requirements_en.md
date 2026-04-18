# Case 05: Mining frigate operational use cases

## Scope
This requirement specification is a bottom-up reconstruction derived from `UseCasesFrigate.sysml`.

## Operational objectives
### UC-MF-001 Mine Asteroids
Main Flow:
1. Identify an asteroid target.
2. Activate the mining laser.
3. Extract ore and store it in the cargo hold.
4. Suspend mining when the cargo hold becomes full.

Exception Flows:
- If the mining laser fails, halt mining and alert the pilot.
- If the target asteroid is depleted, reacquire a target.

### UC-MF-002 Offload Ore and Resupply
Main Flow:
1. Establish a docking connection with a station.
2. Transfer ore to the station.
3. Resupply essential systems.

Exception Flows:
- If docking fails, notify the pilot and abort the offload sequence.
- If cargo transfer fails, suspend operations and keep the ore on board.

## Note
This input intentionally leaves quantitative success thresholds unspecified.
