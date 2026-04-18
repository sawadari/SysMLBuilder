package C05RearWiperReverseLink {
    doc /*
    C05 Rear Wiper Reverse Link
    This case links a rear wiper one-wipe action to reverse gear when the front wiper is already active.
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
        C05-RQ-001: When reverse gear is engaged while the front wiper is active, the system shall command one rear-wiper wipe within 1 s.
        */
    }

    requirement def Req002 {
        doc /*
        C05-RQ-002: The system shall not issue more than one reverse-linked rear-wiper wipe within 10 s.
        */
    }

    requirement def Req003 {
        doc /*
        C05-RQ-003: The system shall disable the reverse-linked wipe while the rear wiper service mode is active.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C05-RQ-001: When reverse gear is engaged while the front wiper is active, the system shall command one rear-wiper wipe within 1 s. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C05-RQ-002: The system shall not issue more than one reverse-linked rear-wiper wipe within 10 s. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C05-RQ-003: The system shall disable the reverse-linked wipe while the rear wiper service mode is active. */

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
