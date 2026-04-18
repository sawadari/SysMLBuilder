package C11LaneDepartureWarning {
    doc /*
    C11 Lane Departure Warning
    This case triggers an audible warning when lane departure occurs under valid operating conditions.
    */

    item def VehicleSpeedValue;
    item def TurnSignalValue;
    item def LaneDepartureValue;
    item def BuzzerCommandValue;

    port def VehicleSpeedPort {
        in item vehicleSpeed : VehicleSpeedValue;
    }

    port def TurnSignalPort {
        in item turnSignalActive : TurnSignalValue;
    }

    port def LaneDeparturePort {
        in item laneDepartureDetected : LaneDepartureValue;
    }

    port def BuzzerCommandPort {
        out item buzzerCommand : BuzzerCommandValue;
    }

    interface def BuzzerCommandInterface {
        end source : BuzzerCommandPort;
        end target : ~BuzzerCommandPort;
        flow source.buzzerCommand to target.buzzerCommand;
    }

    requirement def Req001 {
        doc /*
        C11-RQ-001: When lane departure is detected at vehicle speed of at least 60 km/h and the turn signal is OFF, the system shall generate an audible warning within 150 ms.
        */
    }

    requirement def Req002 {
        doc /*
        C11-RQ-002: The system shall suppress the warning while the turn signal is active.
        */
    }

    requirement def Req003 {
        doc /*
        C11-RQ-003: The system shall stop the audible warning within 300 ms after the lane departure condition is cleared.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C11-RQ-001: When lane departure is detected at vehicle speed of at least 60 km/h and the turn signal is OFF, the system shall generate an audible warning within 150 ms. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C11-RQ-002: The system shall suppress the warning while the turn signal is active. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C11-RQ-003: The system shall stop the audible warning within 300 ms after the lane departure condition is cleared. */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def LaneMonitor {
        port speedIn : VehicleSpeedPort;
        port turnSignalIn : TurnSignalPort;
        port laneIn : LaneDeparturePort;
        port buzzerOut : BuzzerCommandPort;
    }

    part def Buzzer {
        port commandIn : ~BuzzerCommandPort;
    }

    part def LaneDepartureWarningSystem {
        part monitor : LaneMonitor;
        part buzzer : Buzzer;
    }

    part systemUnderTest : LaneDepartureWarningSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C11LaneDepartureWarningStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C11LaneDepartureWarning::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C11LaneDepartureWarning::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C11LaneDepartureWarning::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C11LaneDepartureWarning::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C11LaneDepartureWarning::**;
    }
}
