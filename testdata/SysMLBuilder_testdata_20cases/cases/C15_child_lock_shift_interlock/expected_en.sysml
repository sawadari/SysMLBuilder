package C15ChildLockShiftInterlock {
    doc /*
    C15 Child Lock Shift Interlock
    This case allows child-lock state changes only under safe vehicle conditions.
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
        C15-RQ-001: The system shall allow child-lock activation only when shift position is P and vehicle speed is 0 km/h.
        */
    }

    requirement def Req002 {
        doc /*
        C15-RQ-002: The system shall reject child-lock activation while any rear door is open.
        */
    }

    requirement def Req003 {
        doc /*
        C15-RQ-003: When a valid child-lock deactivation request is received, the system shall complete the deactivation within 500 ms.
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
