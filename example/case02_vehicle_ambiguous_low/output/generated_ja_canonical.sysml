package Case02VehicleAmbiguousLowExpected {
    doc /* Generated canonical model for 車両の曖昧な性能要求. */

    item def InteractionToken;

    port def InteractionPort {
        out item token : InteractionToken;
    }

    interface def InteractionLink {
        end source : InteractionPort;
        end target : ~InteractionPort;
        flow source.token to target.token;
    }

    part def Vehicle {
        port interactionPort : InteractionPort;
    }

    part def Engine {
        port interactionPort : InteractionPort;
    }

    requirement def REQ_VEH_L_001Requirement {
        subject subjectRef : Vehicle;
        doc /*
        REQ-VEH-L-001: 車両は軽量でなければならない。
        */
    }

    requirement def REQ_VEH_L_002Requirement {
        subject subjectRef : Vehicle;
        doc /*
        REQ-VEH-L-002: 車両は燃費が良くなければならない。
        */
    }

    requirement def REQ_VEH_L_003Requirement {
        subject subjectRef : Engine;
        doc /*
        REQ-VEH-L-003: エンジンはトランスミッションへ駆動力を確実に供給しなければならない。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* REQ-VEH-L-001: 車両は軽量でなければならない。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* REQ-VEH-L-002: 車両は燃費が良くなければならない。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* REQ-VEH-L-003: エンジンはトランスミッションへ駆動力を確実に供給しなければならない。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def SystemContext {
        part vehicle : Vehicle;
        part engine : Engine;
        interface subjectInteraction : InteractionLink
        connect vehicle::interactionPort to engine::interactionPort;
    }

    part systemContext : SystemContext;

    requirement extractedRequirements {
        requirement req_veh_l_001 : REQ_VEH_L_001Requirement;
        requirement req_veh_l_002 : REQ_VEH_L_002Requirement;
        requirement req_veh_l_003 : REQ_VEH_L_003Requirement;
    }

}

package Case02VehicleAmbiguousLowExpectedStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose Case02VehicleAmbiguousLowExpected::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose Case02VehicleAmbiguousLowExpected::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose Case02VehicleAmbiguousLowExpected::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose Case02VehicleAmbiguousLowExpected::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose Case02VehicleAmbiguousLowExpected::**;
    }
}
