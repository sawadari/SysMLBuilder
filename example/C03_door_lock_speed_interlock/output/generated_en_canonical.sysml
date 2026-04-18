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

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C03-RQ-001: The door lock system shall lock all doors when vehicle speed is at least 20 km/h for 3 s. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C03-RQ-002: The system shall not perform automatic locking while any door is ajar. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C03-RQ-003: When ignition is OFF and shift position changes to P, the system shall unlock the driver door within 500 ms. */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
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

package C03DoorLockSpeedInterlockStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C03DoorLockSpeedInterlock::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C03DoorLockSpeedInterlock::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C03DoorLockSpeedInterlock::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C03DoorLockSpeedInterlock::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C03DoorLockSpeedInterlock::**;
    }
}
