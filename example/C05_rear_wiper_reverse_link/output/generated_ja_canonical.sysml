package C05RearWiperReverseLink {
    doc /*
    C05 後ワイパリバース連動
    このケースは、前ワイパ動作中にリバースへ入れたとき、後ワイパを1回作動させる機能を表します。
    */

    item def WiperStatusValue;
    item def ShiftPositionValue;
    item def WiperCommandValue;

    port def WiperStatusPort {
        in item frontWiperActive : WiperStatusValue;
    }

    port def ShiftPositionPort {
        in item shiftPosition : ShiftPositionValue;
    }

    port def WiperCommandPort {
        out item rearWiperCommand : WiperCommandValue;
    }

    interface def RearWiperCommandInterface {
        end source : WiperCommandPort;
        end target : ~WiperCommandPort;
        flow source.rearWiperCommand to target.rearWiperCommand;
    }

    requirement def Req001 {
        doc /*
        C05-RQ-001: システムは、前ワイパ動作中にリバースギヤへ入った場合、1 s以内に後ワイパ1回作動を指令すること。
        */
    }

    requirement def Req002 {
        doc /*
        C05-RQ-002: システムは、10 s以内にリバース連動後ワイパ1回作動を複数回発行しないこと。
        */
    }

    requirement def Req003 {
        doc /*
        C05-RQ-003: システムは、後ワイパサービスモードが有効な間、リバース連動作動を禁止すること。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C05-RQ-001: システムは、前ワイパ動作中にリバースギヤへ入った場合、1 s以内に後ワイパ1回作動を指令すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C05-RQ-002: システムは、10 s以内にリバース連動後ワイパ1回作動を複数回発行しないこと。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C05-RQ-003: システムは、後ワイパサービスモードが有効な間、リバース連動作動を禁止すること。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def RearWiperController {
        port frontWiperIn : WiperStatusPort;
        port shiftIn : ShiftPositionPort;
        port commandOut : WiperCommandPort;
    }

    part def RearWiperMotor {
        port commandIn : ~WiperCommandPort;
    }

    part def RearWiperLinkSystem {
        part controller : RearWiperController;
        part motor : RearWiperMotor;
    }

    part systemUnderTest : RearWiperLinkSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C05RearWiperReverseLinkStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C05RearWiperReverseLink::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C05RearWiperReverseLink::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C05RearWiperReverseLink::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C05RearWiperReverseLink::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C05RearWiperReverseLink::**;
    }
}
