package C02AutoWindowAntiPinch {
    doc /*
    C02 オートウインドウ挟み込み防止
    このケースは、挟み込み防止機能とドア開時の禁止条件を持つオートウインドウ機能を表します。
    */

    item def WindowSwitchValue;
    item def DoorStatusValue;
    item def PinchSignalValue;
    item def WindowMotorCommandValue;

    port def WindowSwitchPort {
        in item closeRequest : WindowSwitchValue;
    }

    port def DoorStatusPort {
        in item doorOpen : DoorStatusValue;
    }

    port def PinchSignalPort {
        in item pinchDetected : PinchSignalValue;
    }

    port def WindowMotorCommandPort {
        out item windowCommand : WindowMotorCommandValue;
    }

    interface def WindowMotorCommandInterface {
        end source : WindowMotorCommandPort;
        end target : ~WindowMotorCommandPort;
        flow source.windowCommand to target.windowCommand;
    }

    requirement def Req001 {
        doc /*
        C02-RQ-001: オートウインドウシステムは、閉スイッチが300 ms以上押下された場合に自動閉動作を開始すること。
        */
    }

    requirement def Req002 {
        doc /*
        C02-RQ-002: システムは、対応するドアが開いている間、自動閉動作を禁止すること。
        */
    }

    requirement def Req003 {
        doc /*
        C02-RQ-003: システムは、自動閉動作中に挟み込みを検知した場合、30 ms以内に停止し、ガラスを少なくとも100 mm下降させること。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C02-RQ-001: オートウインドウシステムは、閉スイッチが300 ms以上押下された場合に自動閉動作を開始すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C02-RQ-002: システムは、対応するドアが開いている間、自動閉動作を禁止すること。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C02-RQ-003: システムは、自動閉動作中に挟み込みを検知した場合、30 ms以内に停止し、ガラスを少なくとも100 mm下降させること。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def WindowController {
        state def WindowMotionStates {
            entry; then idle;

            state idle;

            transition idle_to_autoClosing
                first idle
                then autoClosing;

            state autoClosing;

            transition autoClosing_to_reverseOpen
                first autoClosing
                then reverseOpen;

            state reverseOpen;

            transition reverseOpen_to_idle
                first reverseOpen
                then idle;

        }

        port switchIn : WindowSwitchPort;
        port doorStatusIn : DoorStatusPort;
        port pinchIn : PinchSignalPort;
        port commandOut : WindowMotorCommandPort;
    }

    part def WindowMotor {
        port commandIn : ~WindowMotorCommandPort;
    }

    part def PinchSensor {
        port pinchOut : PinchSignalPort;
    }

    part def AutoWindowSystem {
        part controller : WindowController;
        part motor : WindowMotor;
        part sensor : PinchSensor;
    }

    part systemUnderTest : AutoWindowSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C02AutoWindowAntiPinchStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C02AutoWindowAntiPinch::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C02AutoWindowAntiPinch::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C02AutoWindowAntiPinch::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C02AutoWindowAntiPinch::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C02AutoWindowAntiPinch::**;
    }
}
