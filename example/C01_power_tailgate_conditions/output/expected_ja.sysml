package C01PowerTailgateConditions {
    doc /*
    C01 パワーバックドア開条件
    このケースは、開動作前に車両条件を確認し、閉動作中の障害物にも反応するパワーバックドアを表します。
    */

    item def VehicleSpeedValue;
    item def ShiftPositionValue;
    item def TailgateCommandValue;
    item def ObstacleSignalValue;

    port def VehicleSpeedPort {
        in item vehicleSpeed : VehicleSpeedValue;
    }

    port def ShiftPositionPort {
        in item shiftPosition : ShiftPositionValue;
    }

    port def TailgateCommandPort {
        out item tailgateCommand : TailgateCommandValue;
    }

    port def ObstacleSignalPort {
        in item obstacleDetected : ObstacleSignalValue;
    }

    interface def TailgateCommandInterface {
        end source : TailgateCommandPort;
        end target : ~TailgateCommandPort;
        flow source.tailgateCommand to target.tailgateCommand;
    }

    requirement def Req001 {
        doc /*
        C01-RQ-001: パワーバックドアシステムは、車速が3 km/h未満かつシフト位置がPの場合にのみ開要求を受け付けること。
        */
    }

    requirement def Req002 {
        doc /*
        C01-RQ-002: システムは、有効な閉要求の後、200 ms以内に閉動作を開始すること。
        */
    }

    requirement def Req003 {
        doc /*
        C01-RQ-003: システムは、閉動作中に障害物を検知した場合、50 ms以内に停止し、少なくとも200 msは反転動作すること。
        */
    }

    part def TailgateController {
        state def TailgateMotionStates {
            entry; then idle;

            state idle;

            transition idle_to_closing
                first idle
                then closing;

            state closing;

            transition closing_to_reversing
                first closing
                then reversing;

            state reversing;

            transition reversing_to_idle
                first reversing
                then idle;

        }

        port speedIn : VehicleSpeedPort;
        port shiftIn : ShiftPositionPort;
        port obstacleIn : ObstacleSignalPort;
        port commandOut : TailgateCommandPort;
    }

    part def TailgateActuator {
        port commandIn : ~TailgateCommandPort;
    }

    part def ObstacleSensor {
        port obstacleOut : ObstacleSignalPort;
    }

    part def PowerTailgateSystem {
        part controller : TailgateController;
        part actuator : TailgateActuator;
        part sensor : ObstacleSensor;
    }

    part systemUnderTest : PowerTailgateSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C01PowerTailgateConditions::systemUnderTest;
            expose C01PowerTailgateConditions::systemUnderTest::controller;
            expose C01PowerTailgateConditions::systemUnderTest::actuator;
            expose C01PowerTailgateConditions::systemUnderTest::sensor;
        }
    }
}
