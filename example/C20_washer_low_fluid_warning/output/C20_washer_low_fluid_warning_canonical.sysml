package C20WasherLowFluidWarning {
    doc /*
    C20 Washer Low Fluid Warning
    This case shows a warning after low fluid is detected with debounce and clears it after refill.
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
        C20-RQ-001: When washer fluid level is low for 2 s, the system shall display a low-fluid warning within 500 ms.
        */
    }

    requirement def Req002 {
        doc /*
        C20-RQ-002: The system shall not display the warning for transient low-level detections shorter than 2 s.
        */
    }

    requirement def Req003 {
        doc /*
        C20-RQ-003: The system shall clear the warning after fluid level is normal for 5 s.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C20-RQ-001: When washer fluid level is low for 2 s, the system shall display a low-fluid warning within 500 ms. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C20-RQ-002: The system shall not display the warning for transient low-level detections shorter than 2 s. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C20-RQ-003: The system shall clear the warning after fluid level is normal for 5 s. */

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
