package C13ChargeFlapLockControl {
    doc /*
    C13 充電フラップロック制御
    このケースは、走行状態と充電状態に応じて充電フラップを施錠・解錠する機能を表します。
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
        C13-RQ-001: システムは、車両走行中に充電フラップを施錠すること。
        */
    }

    requirement def Req002 {
        doc /*
        C13-RQ-002: システムは、充電中に充電フラップを施錠すること。
        */
    }

    requirement def Req003 {
        doc /*
        C13-RQ-003: システムは、車両が駐車状態で充電完了時、または有効なユーザー解錠要求を受信した場合、充電フラップを解錠すること。
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
