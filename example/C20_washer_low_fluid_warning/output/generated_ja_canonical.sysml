package C20WasherLowFluidWarning {
    doc /*
    C20 ウォッシャ液残量低下警告
    このケースは、ウォッシャ液残量低下をデバウンス付きで検知し、補充後に警告を解除する機能を表します。
    */

    item def FluidLevelValue;
    item def DisplayCommandValue;

    port def FluidLevelPort {
        in item fluidLow : FluidLevelValue;
    }

    port def DisplayCommandPort {
        out item displayCommand : DisplayCommandValue;
    }

    interface def DisplayCommandInterface {
        end source : DisplayCommandPort;
        end target : ~DisplayCommandPort;
        flow source.displayCommand to target.displayCommand;
    }

    requirement def Req001 {
        doc /*
        C20-RQ-001: システムは、ウォッシャ液残量低下が2 s継続した場合、500 ms以内に残量低下警告を表示すること。
        */
    }

    requirement def Req002 {
        doc /*
        C20-RQ-002: システムは、2 s未満の一時的な低レベル検知に対して警告を表示しないこと。
        */
    }

    requirement def Req003 {
        doc /*
        C20-RQ-003: システムは、液量が正常状態で5 s継続した場合、警告を解除すること。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C20-RQ-001: システムは、ウォッシャ液残量低下が2 s継続した場合、500 ms以内に残量低下警告を表示すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C20-RQ-002: システムは、2 s未満の一時的な低レベル検知に対して警告を表示しないこと。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C20-RQ-003: システムは、液量が正常状態で5 s継続した場合、警告を解除すること。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def FluidLevelMonitor {
        port fluidIn : FluidLevelPort;
        port displayOut : DisplayCommandPort;
    }

    part def ClusterDisplay {
        port commandIn : ~DisplayCommandPort;
    }

    part def WasherFluidWarningSystem {
        part monitor : FluidLevelMonitor;
        part display : ClusterDisplay;
    }

    part systemUnderTest : WasherFluidWarningSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C20WasherLowFluidWarningStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C20WasherLowFluidWarning::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C20WasherLowFluidWarning::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C20WasherLowFluidWarning::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C20WasherLowFluidWarning::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C20WasherLowFluidWarning::**;
    }
}
