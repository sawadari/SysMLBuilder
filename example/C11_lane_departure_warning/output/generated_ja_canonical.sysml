package C11LaneDepartureWarning {
    doc /*
    C11 車線逸脱警報
    このケースは、有効条件下で車線逸脱が発生したときに可聴警報を出す機能を表します。
    */

    item def VehicleSpeedValue;
    item def TurnSignalValue;
    item def LaneDepartureValue;
    item def BuzzerCommandValue;

    port def VehicleSpeedPort {
        in item vehicleSpeed : VehicleSpeedValue;
    }

    port def TurnSignalPort {
        in item turnSignalActive : TurnSignalValue;
    }

    port def LaneDeparturePort {
        in item laneDepartureDetected : LaneDepartureValue;
    }

    port def BuzzerCommandPort {
        out item buzzerCommand : BuzzerCommandValue;
    }

    interface def BuzzerCommandInterface {
        end source : BuzzerCommandPort;
        end target : ~BuzzerCommandPort;
        flow source.buzzerCommand to target.buzzerCommand;
    }

    requirement def Req001 {
        doc /*
        C11-RQ-001: システムは、車速60 km/h以上かつ方向指示器OFFの状態で車線逸脱を検知した場合、150 ms以内に可聴警報を生成すること。
        */
    }

    requirement def Req002 {
        doc /*
        C11-RQ-002: システムは、方向指示器が有効な間、警報を抑止すること。
        */
    }

    requirement def Req003 {
        doc /*
        C11-RQ-003: システムは、車線逸脱条件が解消された後300 ms以内に可聴警報を停止すること。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C11-RQ-001: システムは、車速60 km/h以上かつ方向指示器OFFの状態で車線逸脱を検知した場合、150 ms以内に可聴警報を生成すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C11-RQ-002: システムは、方向指示器が有効な間、警報を抑止すること。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C11-RQ-003: システムは、車線逸脱条件が解消された後300 ms以内に可聴警報を停止すること。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def LaneMonitor {
        port speedIn : VehicleSpeedPort;
        port turnSignalIn : TurnSignalPort;
        port laneIn : LaneDeparturePort;
        port buzzerOut : BuzzerCommandPort;
    }

    part def Buzzer {
        port commandIn : ~BuzzerCommandPort;
    }

    part def LaneDepartureWarningSystem {
        part monitor : LaneMonitor;
        part buzzer : Buzzer;
    }

    part systemUnderTest : LaneDepartureWarningSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C11LaneDepartureWarningStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C11LaneDepartureWarning::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C11LaneDepartureWarning::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C11LaneDepartureWarning::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C11LaneDepartureWarning::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C11LaneDepartureWarning::**;
    }
}
