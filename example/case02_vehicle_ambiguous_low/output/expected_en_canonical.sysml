package Case02VehicleAmbiguousLowExpected {
    doc /* Generated canonical model for Vehicle ambiguous performance requirements. */

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
        REQ-VEH-L-001: The vehicle shall be lightweight.
        */
    }

    requirement def REQ_VEH_L_002Requirement {
        subject subjectRef : Vehicle;
        doc /*
        REQ-VEH-L-002: The vehicle shall be fuel efficient.
        */
    }

    requirement def REQ_VEH_L_003Requirement {
        subject subjectRef : Engine;
        doc /*
        REQ-VEH-L-003: The engine shall provide drive power to the transmission reliably.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* REQ-VEH-L-001: The vehicle shall be lightweight. */
        action requirementStep002 : RequirementActivityStep;
        doc /* REQ-VEH-L-002: The vehicle shall be fuel efficient. */
        action requirementStep003 : RequirementActivityStep;
        doc /* REQ-VEH-L-003: The engine shall provide drive power to the transmission reliably. */

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
