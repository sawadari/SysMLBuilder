package C19DriveModeStateTransition {
    doc /*
    C19 ドライブモード状態遷移
    このケースは、Eco、Normal、Sportの各ドライブモードと、遷移ガードおよび故障時フォールバックを表します。
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
        C19-RQ-001: システムは、ECO、NORMAL、およびSPORTの各ドライブモードをサポートすること。
        */
    }

    requirement def Req002 {
        doc /*
        C19-RQ-002: システムは、アクセル開度が20%未満の場合にのみドライブモード変更要求を受け付けること。
        */
    }

    requirement def Req003 {
        doc /*
        C19-RQ-003: システムは、ドライブモード故障を検知した場合、100 ms以内にNORMALモードへ戻ること。
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
