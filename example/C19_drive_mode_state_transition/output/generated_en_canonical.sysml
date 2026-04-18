package C19DriveModeStateTransition {
    doc /*
    C19 Drive Mode State Transition
    This case models Eco, Normal, and Sport drive modes with transition guards and a fault fallback.
    */

    item def AcceleratorValue;
    item def DriveModeRequestValue;
    item def DriveModeStatusValue;

    port def AcceleratorPort {
        in item acceleratorOpening : AcceleratorValue;
    }

    port def DriveModeRequestPort {
        in item driveModeRequest : DriveModeRequestValue;
    }

    port def DriveModeStatusPort {
        out item driveModeStatus : DriveModeStatusValue;
    }

    interface def DriveModeStatusInterface {
        end source : DriveModeStatusPort;
        end target : ~DriveModeStatusPort;
        flow source.driveModeStatus to target.driveModeStatus;
    }

    requirement def Req001 {
        doc /*
        C19-RQ-001: The system shall support ECO, NORMAL, and SPORT drive modes.
        */
    }

    requirement def Req002 {
        doc /*
        C19-RQ-002: The system shall accept a drive-mode change request only when accelerator pedal opening is less than 20 percent.
        */
    }

    requirement def Req003 {
        doc /*
        C19-RQ-003: When a drive-mode fault is detected, the system shall return to NORMAL mode within 100 ms.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C19-RQ-001: The system shall support ECO, NORMAL, and SPORT drive modes. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C19-RQ-002: The system shall accept a drive-mode change request only when accelerator pedal opening is less than 20 percent. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C19-RQ-003: When a drive-mode fault is detected, the system shall return to NORMAL mode within 100 ms. */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def DriveModeController {
        state def DriveModes {
            entry; then eco;

            state eco;

            transition eco_to_normal
                first eco
                then normal;

            state normal;

            transition normal_to_eco
                first normal
                then eco;

            transition normal_to_sport
                first normal
                then sport;

            state sport;

            transition sport_to_normal
                first sport
                then normal;

        }

        port acceleratorIn : AcceleratorPort;
        port requestIn : DriveModeRequestPort;
        port statusOut : DriveModeStatusPort;
    }

    part def DriveModeSystem {
        part controller : DriveModeController;
    }

    part systemUnderTest : DriveModeSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C19DriveModeStateTransitionStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C19DriveModeStateTransition::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C19DriveModeStateTransition::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C19DriveModeStateTransition::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C19DriveModeStateTransition::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C19DriveModeStateTransition::**;
    }
}
