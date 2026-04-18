package C18RegenBrakeInhibitLowTemp {
    doc /*
    C18 低温時回生制動抑制
    このケースは、バッテリ温度に応じて回生制動制限を切り替える機能を表します。
    */

    item def TemperatureValue;
    item def RegenLevelValue;

    port def BatteryTemperaturePort {
        in item batteryTemperature : TemperatureValue;
    }

    port def RegenLevelPort {
        out item regenLevelCommand : RegenLevelValue;
    }

    interface def RegenLevelInterface {
        end source : RegenLevelPort;
        end target : ~RegenLevelPort;
        flow source.regenLevelCommand to target.regenLevelCommand;
    }

    requirement def Req001 {
        doc /*
        C18-RQ-001: システムは、バッテリ温度が-10℃未満の場合、HIGH回生制動レベルを禁止すること。
        */
    }

    requirement def Req002 {
        doc /*
        C18-RQ-002: システムは、バッテリ温度が-20℃未満の場合、すべての回生制動レベルを禁止すること。
        */
    }

    requirement def Req003 {
        doc /*
        C18-RQ-003: システムは、バッテリ温度が-8℃を超えた後にのみHIGH回生制動レベルを再許可すること。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C18-RQ-001: システムは、バッテリ温度が-10℃未満の場合、HIGH回生制動レベルを禁止すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C18-RQ-002: システムは、バッテリ温度が-20℃未満の場合、すべての回生制動レベルを禁止すること。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C18-RQ-003: システムは、バッテリ温度が-8℃を超えた後にのみHIGH回生制動レベルを再許可すること。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def RegenBrakeController {
        port temperatureIn : BatteryTemperaturePort;
        port regenLevelOut : RegenLevelPort;
    }

    part def BatteryTemperatureMonitor {
        port temperatureOut : BatteryTemperaturePort;
    }

    part def RegenBrakeSystem {
        part controller : RegenBrakeController;
        part monitor : BatteryTemperatureMonitor;
    }

    part systemUnderTest : RegenBrakeSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C18RegenBrakeInhibitLowTempStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C18RegenBrakeInhibitLowTemp::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C18RegenBrakeInhibitLowTemp::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C18RegenBrakeInhibitLowTemp::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C18RegenBrakeInhibitLowTemp::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C18RegenBrakeInhibitLowTemp::**;
    }
}
