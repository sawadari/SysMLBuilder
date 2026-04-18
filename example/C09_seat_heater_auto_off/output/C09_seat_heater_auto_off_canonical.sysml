package C09SeatHeaterAutoOff {
    doc /*
    C09 Seat Heater Auto-Off
    This case models a seat heater that steps down and turns off after timed operation.
    */

    item def HeatingRequestValue;
    item def HeatingLevelValue;

    port def HeatingRequestPort {
        in item heaterRequest : HeatingRequestValue;
    }

    port def HeatingLevelPort {
        out item heatingLevelCommand : HeatingLevelValue;
    }

    interface def HeatingLevelInterface {
        end source : HeatingLevelPort;
        end target : ~HeatingLevelPort;
        flow source.heatingLevelCommand to target.heatingLevelCommand;
    }

    requirement def Req001 {
        doc /*
        C09-RQ-001: The seat heater shall allow the HIGH level immediately after user activation.
        */
    }

    requirement def Req002 {
        doc /*
        C09-RQ-002: After 30 min of continuous HIGH operation, the system shall change the level from HIGH to MEDIUM.
        */
    }

    requirement def Req003 {
        doc /*
        C09-RQ-003: After 60 min of total heating operation, the system shall turn the seat heater OFF.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C09-RQ-001: The seat heater shall allow the HIGH level immediately after user activation. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C09-RQ-002: After 30 min of continuous HIGH operation, the system shall change the level from HIGH to MEDIUM. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C09-RQ-003: After 60 min of total heating operation, the system shall turn the seat heater OFF. */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def SeatHeaterController {
        state def SeatHeaterLevels {
            entry; then off;

            state off;

            transition off_to_high
                first off
                then high;

            state high;

            transition high_to_medium
                first high
                then medium;

            state medium;

            transition medium_to_off
                first medium
                then off;

        }

        port requestIn : HeatingRequestPort;
        port levelOut : HeatingLevelPort;
    }

    part def SeatHeaterElement {
        port levelIn : ~HeatingLevelPort;
    }

    part def SeatHeaterSystem {
        part controller : SeatHeaterController;
        part element : SeatHeaterElement;
    }

    part systemUnderTest : SeatHeaterSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C09SeatHeaterAutoOffStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C09SeatHeaterAutoOff::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C09SeatHeaterAutoOff::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C09SeatHeaterAutoOff::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C09SeatHeaterAutoOff::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C09SeatHeaterAutoOff::**;
    }
}
