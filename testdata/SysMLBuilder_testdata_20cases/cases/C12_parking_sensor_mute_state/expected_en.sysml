package C12ParkingSensorMuteState {
    doc /*
    C12 Parking Sensor Mute State
    This case models a mute/unmute toggle and a power-cycle reset for parking sensor audio alerts.
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
        C12-RQ-001: Each valid mute-button press shall toggle the parking sensor audio alert state between MUTED and UNMUTED.
        */
    }

    requirement def Req002 {
        doc /*
        C12-RQ-002: The system shall reset the audio alert state to UNMUTED at every power cycle.
        */
    }

    requirement def Req003 {
        doc /*
        C12-RQ-003: The system shall preserve visual alerts while audio alerts are muted.
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
}
