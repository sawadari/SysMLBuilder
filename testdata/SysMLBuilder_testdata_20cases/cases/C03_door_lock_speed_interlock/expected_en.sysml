package C03DoorLockSpeedInterlock {
    doc /*
    C03 Door Lock Speed Interlock
    This case models automatic door locking and unlocking based on speed, shift position, and door status.
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
        C03-RQ-001: The door lock system shall lock all doors when vehicle speed is at least 20 km/h for 3 s.
        */
    }

    requirement def Req002 {
        doc /*
        C03-RQ-002: The system shall not perform automatic locking while any door is ajar.
        */
    }

    requirement def Req003 {
        doc /*
        C03-RQ-003: When ignition is OFF and shift position changes to P, the system shall unlock the driver door within 500 ms.
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
}
