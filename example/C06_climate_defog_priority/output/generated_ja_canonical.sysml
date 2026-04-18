package C06ClimateDefogPriority {
    doc /*
    C06 空調デフロスト優先制御
    このケースは、前席デフロスト要求時にブロワ段、コンプレッサ状態、吹出口モードを協調制御する機能を表します。
    */

    item def DefogRequestValue;
    item def BlowerCommandValue;
    item def OutletModeValue;
    item def AcCommandValue;

    port def DefogRequestPort {
        in item defogRequest : DefogRequestValue;
    }

    port def BlowerCommandPort {
        out item blowerCommand : BlowerCommandValue;
    }

    port def OutletModePort {
        out item outletModeCommand : OutletModeValue;
    }

    port def AcCommandPort {
        out item acCommand : AcCommandValue;
    }

    interface def BlowerCommandInterface {
        end source : BlowerCommandPort;
        end target : ~BlowerCommandPort;
        flow source.blowerCommand to target.blowerCommand;
    }

    interface def OutletModeInterface {
        end source : OutletModePort;
        end target : ~OutletModePort;
        flow source.outletModeCommand to target.outletModeCommand;
    }

    interface def AcCommandInterface {
        end source : AcCommandPort;
        end target : ~AcCommandPort;
        flow source.acCommand to target.acCommand;
    }

    requirement def Req001 {
        doc /*
        C06-RQ-001: HVACシステムは、前席デフロストが要求された場合、500 ms以内にブロワ段を5以上に設定すること。
        */
    }

    requirement def Req002 {
        doc /*
        C06-RQ-002: システムは、前席デフロストが有効な間、吹出口モードをウインドシールドモードに指令すること。
        */
    }

    requirement def Req003 {
        doc /*
        C06-RQ-003: システムは、コンプレッサ保護が有効でない限り、前席デフロストが有効な間エアコンをONにすること。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C06-RQ-001: HVACシステムは、前席デフロストが要求された場合、500 ms以内にブロワ段を5以上に設定すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C06-RQ-002: システムは、前席デフロストが有効な間、吹出口モードをウインドシールドモードに指令すること。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C06-RQ-003: システムは、コンプレッサ保護が有効でない限り、前席デフロストが有効な間エアコンをONにすること。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def HvacController {
        port defogIn : DefogRequestPort;
        port blowerOut : BlowerCommandPort;
        port outletModeOut : OutletModePort;
        port acOut : AcCommandPort;
    }

    part def BlowerActuator {
        port blowerIn : ~BlowerCommandPort;
    }

    part def AirMixActuator {
        port modeIn : ~OutletModePort;
    }

    part def CompressorRelay {
        port acIn : ~AcCommandPort;
    }

    part def ClimateDefogSystem {
        part controller : HvacController;
        part blower : BlowerActuator;
        part airMix : AirMixActuator;
        part compressor : CompressorRelay;
    }

    part systemUnderTest : ClimateDefogSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C06ClimateDefogPriorityStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C06ClimateDefogPriority::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C06ClimateDefogPriority::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C06ClimateDefogPriority::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C06ClimateDefogPriority::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C06ClimateDefogPriority::**;
    }
}
