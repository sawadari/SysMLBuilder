package C18RegenBrakeInhibitLowTemp {
    doc /*
    C18 Regenerative Brake Inhibit at Low Temperature
    This case applies different regenerative braking limits according to battery temperature.
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
        C18-RQ-001: When battery temperature is below -10 degC, the system shall inhibit the HIGH regenerative braking level.
        */
    }

    requirement def Req002 {
        doc /*
        C18-RQ-002: When battery temperature is below -20 degC, the system shall inhibit all regenerative braking levels.
        */
    }

    requirement def Req003 {
        doc /*
        C18-RQ-003: The system shall restore the HIGH regenerative braking level only after battery temperature rises above -8 degC.
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
