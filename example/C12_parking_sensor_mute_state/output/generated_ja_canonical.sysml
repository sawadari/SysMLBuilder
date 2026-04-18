package C12ParkingSensorMuteState {
    doc /*
    C12 パーキングセンサミュート状態
    このケースは、パーキングセンサ音声警報のミュート/ミュート解除切替と電源再投入時リセットを表します。
    */

    item def MuteButtonValue;
    item def AudioAlertValue;
    item def VisualAlertValue;

    port def MuteButtonPort {
        in item muteButtonPressed : MuteButtonValue;
    }

    port def AudioAlertPort {
        out item audioAlertCommand : AudioAlertValue;
    }

    port def VisualAlertPort {
        out item visualAlertCommand : VisualAlertValue;
    }

    interface def AudioAlertInterface {
        end source : AudioAlertPort;
        end target : ~AudioAlertPort;
        flow source.audioAlertCommand to target.audioAlertCommand;
    }

    interface def VisualAlertInterface {
        end source : VisualAlertPort;
        end target : ~VisualAlertPort;
        flow source.visualAlertCommand to target.visualAlertCommand;
    }

    requirement def Req001 {
        doc /*
        C12-RQ-001: システムは、有効なミュートボタン押下ごとに、パーキングセンサ音声警報状態をMUTEDとUNMUTEDの間で切り替えること。
        */
    }

    requirement def Req002 {
        doc /*
        C12-RQ-002: システムは、電源サイクルごとに音声警報状態をUNMUTEDへリセットすること。
        */
    }

    requirement def Req003 {
        doc /*
        C12-RQ-003: システムは、音声警報がミュート中でも視覚警報を維持すること。
        */
    }

    part def ParkingSensorController {
        state def MuteStates {
            entry; then unmuted;

            state unmuted;

            transition unmuted_to_muted
                first unmuted
                then muted;

            state muted;

            transition muted_to_unmuted
                first muted
                then unmuted;

        }

        port muteButtonIn : MuteButtonPort;
        port audioOut : AudioAlertPort;
        port visualOut : VisualAlertPort;
    }

    part def AudioBuzzer {
        port audioIn : ~AudioAlertPort;
    }

    part def VisualDisplay {
        port visualIn : ~VisualAlertPort;
    }

    part def ParkingSensorAlertSystem {
        part controller : ParkingSensorController;
        part buzzer : AudioBuzzer;
        part display : VisualDisplay;
    }

    part systemUnderTest : ParkingSensorAlertSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C12ParkingSensorMuteState::systemUnderTest;
            expose C12ParkingSensorMuteState::systemUnderTest::controller;
            expose C12ParkingSensorMuteState::systemUnderTest::buzzer;
            expose C12ParkingSensorMuteState::systemUnderTest::display;
        }
    }
}
