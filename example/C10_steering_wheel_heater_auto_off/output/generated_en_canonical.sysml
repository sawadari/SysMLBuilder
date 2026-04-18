package C10SteeringWheelHeaterAutoOff {
    doc /*
    C10 Steering Wheel Heater Auto-Off
    This case combines ambient temperature gating with automatic timeout for steering wheel heating.
    */

    item def TemperatureValue;
    item def HeatingRequestValue;
    item def HeatingLevelValue;

    port def AmbientTemperaturePort {
        in item ambientTemperature : TemperatureValue;
    }

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
        C10-RQ-001: The system shall reject a steering wheel heater request when ambient temperature is above 20 degC.
        */
    }

    requirement def Req002 {
        doc /*
        C10-RQ-002: The system shall turn the steering wheel heater OFF after 30 min of continuous heating.
        */
    }

    requirement def Req003 {
        doc /*
        C10-RQ-003: The system shall restore the heater to OFF after every ignition cycle.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C10-RQ-001: The system shall reject a steering wheel heater request when ambient temperature is above 20 degC. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C10-RQ-002: The system shall turn the steering wheel heater OFF after 30 min of continuous heating. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C10-RQ-003: The system shall restore the heater to OFF after every ignition cycle. */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def SteeringWheelHeaterController {
        port tempIn : AmbientTemperaturePort;
        port requestIn : HeatingRequestPort;
        port levelOut : HeatingLevelPort;
    }

    part def SteeringWheelHeaterElement {
        port levelIn : ~HeatingLevelPort;
    }

    part def SteeringWheelHeaterSystem {
        part controller : SteeringWheelHeaterController;
        part element : SteeringWheelHeaterElement;
    }

    part systemUnderTest : SteeringWheelHeaterSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C10SteeringWheelHeaterAutoOffStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C10SteeringWheelHeaterAutoOff::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C10SteeringWheelHeaterAutoOff::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C10SteeringWheelHeaterAutoOff::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C10SteeringWheelHeaterAutoOff::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C10SteeringWheelHeaterAutoOff::**;
    }
}
