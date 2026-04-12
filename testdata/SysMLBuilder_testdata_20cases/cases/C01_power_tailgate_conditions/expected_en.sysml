package C01PowerTailgateConditions {
    doc /*
    C01 Power Tailgate Opening Conditions
    This case describes a power tailgate that checks vehicle conditions before opening and reacts to obstacles during closing.
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
        C01-RQ-001: The power tailgate system shall accept an open request only when vehicle speed is less than 3 km/h and shift position is P.
        */
    }

    requirement def Req002 {
        doc /*
        C01-RQ-002: After a valid close request, the system shall start closing within 200 ms.
        */
    }

    requirement def Req003 {
        doc /*
        C01-RQ-003: When an obstacle is detected during closing, the system shall stop within 50 ms and reverse for at least 200 ms.
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
}
