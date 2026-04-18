package C17OtaUpdatePreconditions {
    doc /*
    C17 OTA Update Preconditions
    This case models update-start gating and suspension conditions during an over-the-air software update.
    */

    item def VehicleParkValue;
    item def DoorLockStatusValue;
    item def BatterySocValue;
    item def UpdateControlValue;

    port def VehicleParkPort {
        in item vehicleParked : VehicleParkValue;
    }

    port def DoorLockStatusPort {
        in item doorsLocked : DoorLockStatusValue;
    }

    port def BatterySocPort {
        in item batterySoc : BatterySocValue;
    }

    port def UpdateControlPort {
        out item updateControl : UpdateControlValue;
    }

    interface def UpdateControlInterface {
        end source : UpdateControlPort;
        end target : ~UpdateControlPort;
        flow source.updateControl to target.updateControl;
    }

    requirement def Req001 {
        doc /*
        C17-RQ-001: The OTA update system shall start an update only when the vehicle is parked, doors are locked, and battery state of charge is at least 40 percent.
        */
    }

    requirement def Req002 {
        doc /*
        C17-RQ-002: When ignition turns ON during an update, the system shall suspend the update within 1 s.
        */
    }

    requirement def Req003 {
        doc /*
        C17-RQ-003: When any door is unlocked during an update, the system shall suspend the update within 1 s.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C17-RQ-001: The OTA update system shall start an update only when the vehicle is parked, doors are locked, and battery state of charge is at least 40 percent. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C17-RQ-002: When ignition turns ON during an update, the system shall suspend the update within 1 s. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C17-RQ-003: When any door is unlocked during an update, the system shall suspend the update within 1 s. */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def UpdateManager {
        port updateControlOut : UpdateControlPort;
    }

    part def VehicleConditionMonitor {
        state def UpdateStates {
            entry; then idle;

            state idle;

            transition idle_to_updating
                first idle
                then updating;

            state updating;

            transition updating_to_suspended
                first updating
                then suspended;

            state suspended;

            transition suspended_to_idle
                first suspended
                then idle;

        }

        port parkIn : VehicleParkPort;
        port lockIn : DoorLockStatusPort;
        port socIn : BatterySocPort;
        port updateControlOut : UpdateControlPort;
    }

    part def OtaUpdateSystem {
        part manager : UpdateManager;
        part monitor : VehicleConditionMonitor;
    }

    part systemUnderTest : OtaUpdateSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C17OtaUpdatePreconditionsStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C17OtaUpdatePreconditions::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C17OtaUpdatePreconditions::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C17OtaUpdatePreconditions::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C17OtaUpdatePreconditions::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C17OtaUpdatePreconditions::**;
    }
}
