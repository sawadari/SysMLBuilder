package C14KeylessEntryUnlock {
    doc /*
    C14 Keyless Entry Unlock
    This case models valid key detection, unlock timing, and a lockout after repeated invalid attempts.
    */

    item def KeyPresenceValue;
    item def HandleTouchValue;
    item def DoorLockCommandValue;

    port def KeyPresencePort {
        in item validKeyPresent : KeyPresenceValue;
    }

    port def HandleTouchPort {
        in item handleTouched : HandleTouchValue;
    }

    port def DoorLockCommandPort {
        out item doorUnlockCommand : DoorLockCommandValue;
    }

    interface def DoorUnlockInterface {
        end source : DoorLockCommandPort;
        end target : ~DoorLockCommandPort;
        flow source.doorUnlockCommand to target.doorUnlockCommand;
    }

    requirement def Req001 {
        doc /*
        C14-RQ-001: When a valid key is within 1 m and the driver door handle is touched, the system shall unlock the driver door within 300 ms.
        */
    }

    requirement def Req002 {
        doc /*
        C14-RQ-002: The system shall reject unlock requests from invalid keys.
        */
    }

    requirement def Req003 {
        doc /*
        C14-RQ-003: When 5 invalid key attempts occur within 60 s, the system shall inhibit further keyless unlock processing for 5 min.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C14-RQ-001: When a valid key is within 1 m and the driver door handle is touched, the system shall unlock the driver door within 300 ms. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C14-RQ-002: The system shall reject unlock requests from invalid keys. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C14-RQ-003: When 5 invalid key attempts occur within 60 s, the system shall inhibit further keyless unlock processing for 5 min. */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def AccessController {
        state def AccessStates {
            entry; then ready;

            state ready;

            transition ready_to_lockedOut
                first ready
                then lockedOut;

            state lockedOut;

            transition lockedOut_to_ready
                first lockedOut
                then ready;

        }

        port keyIn : KeyPresencePort;
        port touchIn : HandleTouchPort;
        port commandOut : DoorLockCommandPort;
    }

    part def RfReceiver {
        port keyOut : KeyPresencePort;
    }

    part def DoorLockActuator {
        port commandIn : ~DoorLockCommandPort;
    }

    part def KeylessEntrySystem {
        part controller : AccessController;
        part receiver : RfReceiver;
        part actuator : DoorLockActuator;
    }

    part systemUnderTest : KeylessEntrySystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C14KeylessEntryUnlockStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C14KeylessEntryUnlock::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C14KeylessEntryUnlock::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C14KeylessEntryUnlock::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C14KeylessEntryUnlock::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C14KeylessEntryUnlock::**;
    }
}
