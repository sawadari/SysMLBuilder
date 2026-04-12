package C15ChildLockShiftInterlock {
    doc /*
    C15 チャイルドロックシフト連動
    このケースは、安全な車両条件下でのみチャイルドロック状態変更を許可する機能を表します。
    */

    item def ShiftPositionValue;
    item def VehicleSpeedValue;
    item def DoorStatusValue;
    item def LockCommandValue;

    port def ShiftPositionPort {
        in item shiftPosition : ShiftPositionValue;
    }

    port def VehicleSpeedPort {
        in item vehicleSpeed : VehicleSpeedValue;
    }

    port def DoorStatusPort {
        in item rearDoorOpen : DoorStatusValue;
    }

    port def LockCommandPort {
        out item childLockCommand : LockCommandValue;
    }

    interface def ChildLockCommandInterface {
        end source : LockCommandPort;
        end target : ~LockCommandPort;
        flow source.childLockCommand to target.childLockCommand;
    }

    requirement def Req001 {
        doc /*
        C15-RQ-001: システムは、シフト位置がPかつ車速0 km/hの場合にのみチャイルドロック有効化を許可すること。
        */
    }

    requirement def Req002 {
        doc /*
        C15-RQ-002: システムは、いずれかの後席ドアが開いている間、チャイルドロック有効化を拒否すること。
        */
    }

    requirement def Req003 {
        doc /*
        C15-RQ-003: システムは、有効なチャイルドロック無効化要求を受信した場合、500 ms以内に無効化を完了すること。
        */
    }

    part def ChildLockController {
        port shiftIn : ShiftPositionPort;
        port speedIn : VehicleSpeedPort;
        port doorStatusIn : DoorStatusPort;
        port commandOut : LockCommandPort;
    }

    part def RearDoorLockActuator {
        port commandIn : ~LockCommandPort;
    }

    part def ChildLockSystem {
        part controller : ChildLockController;
        part actuator : RearDoorLockActuator;
    }

    part systemUnderTest : ChildLockSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;
}
