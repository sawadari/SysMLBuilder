package C11LaneDepartureWarning {
    doc /*
    C11 Lane Departure Warning
    This case triggers an audible warning when lane departure occurs under valid operating conditions.
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
        C11-RQ-001: When lane departure is detected at vehicle speed of at least 60 km/h and the turn signal is OFF, the system shall generate an audible warning within 150 ms.
        */
    }

    requirement def Req002 {
        doc /*
        C11-RQ-002: The system shall suppress the warning while the turn signal is active.
        */
    }

    requirement def Req003 {
        doc /*
        C11-RQ-003: The system shall stop the audible warning within 300 ms after the lane departure condition is cleared.
        */
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

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C11LaneDepartureWarning::systemUnderTest;
            expose C11LaneDepartureWarning::systemUnderTest::monitor;
            expose C11LaneDepartureWarning::systemUnderTest::buzzer;
        }
    }
}
