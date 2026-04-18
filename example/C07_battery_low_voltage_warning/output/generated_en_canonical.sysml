package C07BatteryLowVoltageWarning {
    doc /*
    C07 Battery Low Voltage Warning
    This case monitors battery voltage, shows a warning, and reports a message after a debounce period.
    */

    item def VoltageValue;
    item def LampCommandValue;
    item def NetworkStatusValue;

    port def VoltageInputPort {
        in item batteryVoltage : VoltageValue;
    }

    port def LampCommandPort {
        out item lampCommand : LampCommandValue;
    }

    port def NetworkStatusPort {
        out item statusMessage : NetworkStatusValue;
    }

    interface def LampCommandInterface {
        end source : LampCommandPort;
        end target : ~LampCommandPort;
        flow source.lampCommand to target.lampCommand;
    }

    interface def NetworkStatusInterface {
        end source : NetworkStatusPort;
        end target : ~NetworkStatusPort;
        flow source.statusMessage to target.statusMessage;
    }

    requirement def Req001 {
        doc /*
        C07-RQ-001: When battery voltage is below 11.5 V for 5 s, the system shall turn on the low-voltage warning lamp.
        */
    }

    requirement def Req002 {
        doc /*
        C07-RQ-002: The system shall send a low-voltage status message on the vehicle network within 100 ms after the warning lamp is turned on.
        */
    }

    requirement def Req003 {
        doc /*
        C07-RQ-003: The system shall clear the warning after battery voltage is above 12.1 V for 10 s.
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C07-RQ-001: When battery voltage is below 11.5 V for 5 s, the system shall turn on the low-voltage warning lamp. */
        action requirementStep002 : RequirementActivityStep;
        doc /* C07-RQ-002: The system shall send a low-voltage status message on the vehicle network within 100 ms after the warning lamp is turned on. */
        action requirementStep003 : RequirementActivityStep;
        doc /* C07-RQ-003: The system shall clear the warning after battery voltage is above 12.1 V for 10 s. */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def BatteryMonitor {
        port voltageIn : VoltageInputPort;
        port lampOut : LampCommandPort;
        port networkOut : NetworkStatusPort;
    }

    part def WarningLamp {
        port commandIn : ~LampCommandPort;
    }

    part def NetworkPublisher {
        port statusIn : ~NetworkStatusPort;
    }

    part def BatteryWarningSystem {
        part monitor : BatteryMonitor;
        part lamp : WarningLamp;
        part publisher : NetworkPublisher;
    }

    part systemUnderTest : BatteryWarningSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C07BatteryLowVoltageWarningStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C07BatteryLowVoltageWarning::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C07BatteryLowVoltageWarning::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C07BatteryLowVoltageWarning::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C07BatteryLowVoltageWarning::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C07BatteryLowVoltageWarning::**;
    }
}
