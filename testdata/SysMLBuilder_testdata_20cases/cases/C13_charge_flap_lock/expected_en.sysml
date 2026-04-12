package C13ChargeFlapLockControl {
    doc /*
    C13 Charge Flap Lock Control
    This case locks and unlocks a charging flap based on driving and charging states.
    */

    item def VehicleMotionValue;
    item def ChargingStatusValue;
    item def LockCommandValue;

    port def VehicleMotionPort {
        in item vehicleMoving : VehicleMotionValue;
    }

    port def ChargingStatusPort {
        in item chargingActive : ChargingStatusValue;
    }

    port def LockCommandPort {
        out item lockCommand : LockCommandValue;
    }

    interface def LockCommandInterface {
        end source : LockCommandPort;
        end target : ~LockCommandPort;
        flow source.lockCommand to target.lockCommand;
    }

    requirement def Req001 {
        doc /*
        C13-RQ-001: The system shall lock the charge flap while the vehicle is driving.
        */
    }

    requirement def Req002 {
        doc /*
        C13-RQ-002: The system shall lock the charge flap while charging is active.
        */
    }

    requirement def Req003 {
        doc /*
        C13-RQ-003: The system shall unlock the charge flap when the vehicle is parked and charging is complete or when a valid user unlock request is received.
        */
    }

    part def ChargeFlapController {
        port motionIn : VehicleMotionPort;
        port chargingIn : ChargingStatusPort;
        port commandOut : LockCommandPort;
    }

    part def ChargeFlapActuator {
        port commandIn : ~LockCommandPort;
    }

    part def ChargeFlapLockSystem {
        part controller : ChargeFlapController;
        part actuator : ChargeFlapActuator;
    }

    part systemUnderTest : ChargeFlapLockSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C13ChargeFlapLockControl::systemUnderTest;
            expose C13ChargeFlapLockControl::systemUnderTest::controller;
            expose C13ChargeFlapLockControl::systemUnderTest::actuator;
        }
    }
}
