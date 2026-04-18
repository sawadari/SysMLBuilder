package C10SteeringWheelHeaterAutoOff {
    doc /*
    C10 ステアリングヒータ自動オフ
    このケースは、周囲温度条件と自動タイムアウトを組み合わせたステアリングヒータを表します。
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
        C10-RQ-001: システムは、外気温が20℃を超える場合、ステアリングヒータ要求を拒否すること。
        */
    }

    requirement def Req002 {
        doc /*
        C10-RQ-002: システムは、加熱が30 min連続した後、ステアリングヒータをOFFにすること。
        */
    }

    requirement def Req003 {
        doc /*
        C10-RQ-003: システムは、イグニッションサイクルごとにヒータ状態をOFFへ戻すこと。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C10-RQ-001: システムは、外気温が20℃を超える場合、ステアリングヒータ要求を拒否すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C10-RQ-002: システムは、加熱が30 min連続した後、ステアリングヒータをOFFにすること。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C10-RQ-003: システムは、イグニッションサイクルごとにヒータ状態をOFFへ戻すこと。 */

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
