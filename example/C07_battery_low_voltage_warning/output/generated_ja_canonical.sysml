package C07BatteryLowVoltageWarning {
    doc /*
    C07 低電圧警告
    このケースは、バッテリ電圧を監視し、デバウンス後に警告表示とメッセージ送信を行う機能を表します。
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
        C07-RQ-001: システムは、バッテリ電圧が11.5 V未満の状態が5 s継続した場合、低電圧警告灯を点灯すること。
        */
    }

    requirement def Req002 {
        doc /*
        C07-RQ-002: システムは、警告灯点灯後100 ms以内に車載ネットワークへ低電圧状態メッセージを送信すること。
        */
    }

    requirement def Req003 {
        doc /*
        C07-RQ-003: システムは、バッテリ電圧が12.1 Vを超える状態が10 s継続した場合、警告を解除すること。
        */
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

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C07BatteryLowVoltageWarning::systemUnderTest;
            expose C07BatteryLowVoltageWarning::systemUnderTest::monitor;
            expose C07BatteryLowVoltageWarning::systemUnderTest::lamp;
            expose C07BatteryLowVoltageWarning::systemUnderTest::publisher;
        }
    }
}
