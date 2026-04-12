package C19DriveModeStateTransition {
    doc /*
    C19 Drive Mode State Transition
    This case models Eco, Normal, and Sport drive modes with transition guards and a fault fallback.
    */

    item def AcceleratorValue;
    item def DriveModeRequestValue;
    item def DriveModeStatusValue;

    port def AcceleratorPort {
        in item acceleratorOpening : AcceleratorValue;
    }

    port def DriveModeRequestPort {
        in item driveModeRequest : DriveModeRequestValue;
    }

    port def DriveModeStatusPort {
        out item driveModeStatus : DriveModeStatusValue;
    }

    interface def DriveModeStatusInterface {
        end source : DriveModeStatusPort;
        end target : ~DriveModeStatusPort;
        flow source.driveModeStatus to target.driveModeStatus;
    }

    requirement def Req001 {
        doc /*
        C19-RQ-001: The system shall support ECO, NORMAL, and SPORT drive modes.
        */
    }

    requirement def Req002 {
        doc /*
        C19-RQ-002: The system shall accept a drive-mode change request only when accelerator pedal opening is less than 20 percent.
        */
    }

    requirement def Req003 {
        doc /*
        C19-RQ-003: When a drive-mode fault is detected, the system shall return to NORMAL mode within 100 ms.
        */
    }

    part def DriveModeController {
        state def DriveModes {
            entry; then eco;

            state eco;

            transition eco_to_normal
                first eco
                then normal;

            state normal;

            transition normal_to_eco
                first normal
                then eco;

            transition normal_to_sport
                first normal
                then sport;

            state sport;

            transition sport_to_normal
                first sport
                then normal;

        }

        port acceleratorIn : AcceleratorPort;
        port requestIn : DriveModeRequestPort;
        port statusOut : DriveModeStatusPort;
    }

    part def DriveModeSystem {
        part controller : DriveModeController;
    }

    part systemUnderTest : DriveModeSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;
}
