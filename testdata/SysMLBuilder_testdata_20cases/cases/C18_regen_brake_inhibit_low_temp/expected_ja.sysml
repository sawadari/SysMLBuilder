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
