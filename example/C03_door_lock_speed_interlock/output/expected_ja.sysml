package C03DoorLockSpeedInterlock {
    doc /*
    C03 ドアロック車速連動
    このケースは、車速、シフト位置、ドア状態に基づく自動ロック・自動アンロックを表します。
    */

    item def VehicleSpeedValue;
    item def DoorStatusValue;
    item def ShiftPositionValue;
    item def DoorLockCommandValue;

    port def VehicleSpeedPort {
        in item vehicleSpeed : VehicleSpeedValue;
    }

    port def DoorStatusPort {
        in item doorAjar : DoorStatusValue;
    }

    port def ShiftPositionPort {
        in item shiftPosition : ShiftPositionValue;
    }

    port def DoorLockCommandPort {
        out item lockCommand : DoorLockCommandValue;
    }

    interface def DoorLockCommandInterface {
        end source : DoorLockCommandPort;
        end target : ~DoorLockCommandPort;
        flow source.lockCommand to target.lockCommand;
    }

    requirement def Req001 {
        doc /*
        C03-RQ-001: ドアロックシステムは、車速が20 km/h以上の状態が3 s継続した場合、全ドアを施錠すること。
        */
    }

    requirement def Req002 {
        doc /*
        C03-RQ-002: システムは、いずれかのドアが半ドアの間、自動施錠を実行しないこと。
        */
    }

    requirement def Req003 {
        doc /*
        C03-RQ-003: システムは、イグニッションがOFFでシフト位置がPに変化した場合、500 ms以内に運転席ドアを解錠すること。
        */
    }

    part def DoorLockController {
        port speedIn : VehicleSpeedPort;
        port doorStatusIn : DoorStatusPort;
        port shiftIn : ShiftPositionPort;
        port commandOut : DoorLockCommandPort;
    }

    part def DoorLockActuator {
        port commandIn : ~DoorLockCommandPort;
    }

    part def DoorLockSystem {
        part controller : DoorLockController;
        part actuator : DoorLockActuator;
    }

    part systemUnderTest : DoorLockSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C03DoorLockSpeedInterlock::systemUnderTest;
            expose C03DoorLockSpeedInterlock::systemUnderTest::controller;
            expose C03DoorLockSpeedInterlock::systemUnderTest::actuator;
        }
    }
}
