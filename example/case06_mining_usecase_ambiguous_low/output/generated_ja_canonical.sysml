package Case06MiningUsecaseAmbiguousLowExpected {
    doc /* Generated canonical model for 採掘フリゲートの曖昧な運用記述. */

    part def MiningFrigate {
    }

    requirement def REQ_UC_L_001Requirement {
        subject subjectRef : MiningFrigate;
        doc /*
        REQ-UC-L-001: 採掘フリゲートは小惑星を効率的に採掘できるべきである。
        */
    }

    requirement def REQ_UC_L_002Requirement {
        subject subjectRef : MiningFrigate;
        doc /*
        REQ-UC-L-002: 採掘フリゲートは脅威を受けたとき自己防衛できるべきである。
        */
    }

    requirement def REQ_UC_L_003Requirement {
        subject subjectRef : MiningFrigate;
        doc /*
        REQ-UC-L-003: 採掘フリゲートは必要時に補給できるべきである。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* REQ-UC-L-001: 採掘フリゲートは小惑星を効率的に採掘できるべきである。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* REQ-UC-L-002: 採掘フリゲートは脅威を受けたとき自己防衛できるべきである。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* REQ-UC-L-003: 採掘フリゲートは必要時に補給できるべきである。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def SystemContext {
        part miningFrigate : MiningFrigate;
    }

    part systemContext : SystemContext;

    requirement extractedRequirements {
        requirement req_uc_l_001 : REQ_UC_L_001Requirement;
        requirement req_uc_l_002 : REQ_UC_L_002Requirement;
        requirement req_uc_l_003 : REQ_UC_L_003Requirement;
    }

}

package Case06MiningUsecaseAmbiguousLowExpectedStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose Case06MiningUsecaseAmbiguousLowExpected::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose Case06MiningUsecaseAmbiguousLowExpected::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose Case06MiningUsecaseAmbiguousLowExpected::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose Case06MiningUsecaseAmbiguousLowExpected::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose Case06MiningUsecaseAmbiguousLowExpected::**;
    }
}
