package C08CanHeartbeatTimeout {
    doc /*
    C08 CAN Heartbeat Timeout Reaction
    This case reacts to a missing heartbeat from a brake controller by disabling a dependent function and storing a fault.
    */

    item def HeartbeatValue;
    item def FunctionControlValue;
    item def DiagnosticStatusValue;

    port def HeartbeatPort {
        in item heartbeat : HeartbeatValue;
    }

    port def FunctionControlPort {
        out item cruiseEnable : FunctionControlValue;
    }

    port def DiagnosticStatusPort {
        out item diagnosticStatus : DiagnosticStatusValue;
    }

    interface def CruiseControlInterface {
        end source : FunctionControlPort;
        end target : ~FunctionControlPort;
        flow source.cruiseEnable to target.cruiseEnable;
    }

    interface def DiagnosticStatusInterface {
        end source : DiagnosticStatusPort;
        end target : ~DiagnosticStatusPort;
        flow source.diagnosticStatus to target.diagnosticStatus;
    }

    requirement def Req001 {
        doc /*
        C08-RQ-001: When the brake controller heartbeat is missing for 100 ms, the system shall set a communication-timeout fault.
        */
    }

    requirement def Req002 {
        doc /*
        C08-RQ-002: The system shall disable cruise control within 50 ms after the communication-timeout fault is set.
        */
    }

    requirement def Req003 {
        doc /*
        C08-RQ-003: The system shall store a diagnostic trouble code and send a fault status message within 100 ms.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C08-RQ-001: When the brake controller heartbeat is missing for 100 ms, the system shall set a communication-timeout fault. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C08-RQ-002: The system shall disable cruise control within 50 ms after the communication-timeout fault is set. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C08-RQ-003: The system shall store a diagnostic trouble code and send a fault status message within 100 ms. */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def HeartbeatMonitor {
        state def CommunicationStates {
            entry; then healthy;

            state healthy;

            transition healthy_to_timeoutDetected
                first healthy
                then timeoutDetected;

            state timeoutDetected;

            transition timeoutDetected_to_safeState
                first timeoutDetected
                then safeState;

            state safeState;

            transition safeState_to_healthy
                first safeState
                then healthy;

        }

        port heartbeatIn : HeartbeatPort;
        port functionOut : FunctionControlPort;
        port diagOut : DiagnosticStatusPort;
    }

    part def CruiseControlGate {
        port functionIn : ~FunctionControlPort;
    }

    part def DiagnosticManager {
        port diagIn : ~DiagnosticStatusPort;
    }

    part def CommunicationMonitoringSystem {
        state def CommunicationStates {
            entry; then healthy;

            state healthy;

            transition healthy_to_timeoutDetected
                first healthy
                then timeoutDetected;

            state timeoutDetected;

            transition timeoutDetected_to_safeState
                first timeoutDetected
                then safeState;

            state safeState;

            transition safeState_to_healthy
                first safeState
                then healthy;

        }

        part monitor : HeartbeatMonitor;
        part gate : CruiseControlGate;
        part diagnostics : DiagnosticManager;
    }

    part systemUnderTest : CommunicationMonitoringSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C08CanHeartbeatTimeoutStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C08CanHeartbeatTimeout::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C08CanHeartbeatTimeout::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C08CanHeartbeatTimeout::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C08CanHeartbeatTimeout::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C08CanHeartbeatTimeout::**;
    }
}
