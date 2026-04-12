package C08CanHeartbeatTimeout {
    doc /*
    C08 CANハートビートタイムアウト反応
    このケースは、ブレーキコントローラからのハートビート消失に対して、依存機能を停止し故障を記録する機能を表します。
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
        C08-RQ-001: システムは、ブレーキコントローラのハートビートが100 ms欠落した場合、通信タイムアウト故障を設定すること。
        */
    }

    requirement def Req002 {
        doc /*
        C08-RQ-002: システムは、通信タイムアウト故障設定後50 ms以内にクルーズコントロールを無効化すること。
        */
    }

    requirement def Req003 {
        doc /*
        C08-RQ-003: システムは、100 ms以内に故障診断コードを保存し、故障状態メッセージを送信すること。
        */
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

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C08CanHeartbeatTimeout::systemUnderTest;
            expose C08CanHeartbeatTimeout::systemUnderTest::monitor;
            expose C08CanHeartbeatTimeout::systemUnderTest::gate;
            expose C08CanHeartbeatTimeout::systemUnderTest::diagnostics;
        }
    }
}
