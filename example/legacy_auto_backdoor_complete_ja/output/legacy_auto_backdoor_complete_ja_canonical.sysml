package LegacyAutoBackDoorCompleteJa {
    doc /*
    LEGACY_ABD_COMPLETE_JA 自動バックドア制御 完全版 参考入力
    
    */

    item def VehicleStatusSignal;
    item def DoorRequestSignal;
    item def PositionStatusSignal;
    item def PinchStatusSignal;
    item def LatchStatusSignal;
    item def MotorCommandSignal;
    item def BuzzerCommandSignal;

    port def VehicleStatusPort {
        in item vehicleStatus : VehicleStatusSignal;
    }

    port def DoorRequestPort {
        in item doorRequest : DoorRequestSignal;
    }

    port def PositionStatusPort {
        in item positionStatus : PositionStatusSignal;
    }

    port def PinchStatusPort {
        in item pinchStatus : PinchStatusSignal;
    }

    port def LatchStatusPort {
        in item latchStatus : LatchStatusSignal;
    }

    port def MotorCommandPort {
        out item motorCommand : MotorCommandSignal;
    }

    port def BuzzerCommandPort {
        out item buzzerCommand : BuzzerCommandSignal;
    }

    interface def VehicleStatusInterface {
        end source : VehicleStatusPort;
        end target : ~VehicleStatusPort;
        flow source.vehicleStatus to target.vehicleStatus;
    }

    interface def DoorRequestInterface {
        end source : DoorRequestPort;
        end target : ~DoorRequestPort;
        flow source.doorRequest to target.doorRequest;
    }

    interface def MotorCommandInterface {
        end source : MotorCommandPort;
        end target : ~MotorCommandPort;
        flow source.motorCommand to target.motorCommand;
    }

    requirement def Req001 {
        doc /*
        ABD-REQ-001: ShiftPos が P であり、VehSpd が 3 km/h 未満の場合にのみ、BackDoorOpenReq を開要求として受け付けなければならない。
        */
    }

    requirement def Req002 {
        doc /*
        ABD-REQ-003: 開要求を受け付けた場合、100 ms 以内に駆動モータへ開方向駆動を指示しなければならない。
        */
    }

    requirement def Req003 {
        doc /*
        ABD-REQ-004: BackDoorPos が 95 % 以上となった場合、駆動モータを停止し、状態を全開へ遷移しなければならない。
        */
    }

    requirement def Req004 {
        doc /*
        ABD-REQ-007: 閉動作中に PinchDetected = true を検知した場合、50 ms 以内に閉方向駆動を停止し、200 ms 以内に開方向へ反転しなければならない。
        */
    }

    requirement def Req005 {
        doc /*
        ABD-REQ-009: 異常停止状態へ遷移した場合、1 s 以内に BuzzerReq を true にしなければならない。
        */
    }

    requirement def Req006 {
        doc /*
        ABD-REQ-010: 開度センサ値が 500 ms 以上更新されない場合、異常停止状態へ遷移しなければならない。
        */
    }

    requirement def Req007 {
        doc /*
        ABD-REQ-012: 全閉状態で開要求を受け付けた場合、開動作中へ遷移しなければならない。
        */
    }

    requirement def Req008 {
        doc /*
        ABD-REQ-015: 閉動作中で挟み込み検知した場合、反転開へ遷移しなければならない。
        */
    }

    requirement def Req009 {
        doc /*
        ABD-VER-001: ShiftPos=P, VehSpd=0 km/h, BackDoorOpenReq=true のとき、100 ms 以内に開方向駆動が開始されることを確認する。
        */
    }

    part def BodyControlModule {
        port vehicleStatusPort : VehicleStatusPort;
        port requestPort : DoorRequestPort;
    }

    part def PowerBackDoorSystem {
        part controller : BackDoorController;
        part driveMotor : DriveMotorModule;
        part positionSensor : PositionSensorModule;
        part pinchSensor : PinchSensorModule;
        part latchModule : LatchModule;
        part buzzerModule : BuzzerModule;
    }

    part def BackDoorController {
        state def BackDoorMotionStates {
            entry; then Closed;

            state Closed;

            transition Closed_to_Opening
                first Closed
                then Opening;

            state Opening;

            state Closing;

            transition Closing_to_ReverseOpening
                first Closing
                then ReverseOpening;

            state ReverseOpening;

            transition ReverseOpening_to_Closed
                first ReverseOpening
                then Closed;

            state FaultStop;

        }

        port vehicleStatusPort : ~VehicleStatusPort;
        port requestPort : ~DoorRequestPort;
        port positionStatusPort : ~PositionStatusPort;
        port pinchStatusPort : ~PinchStatusPort;
        port latchStatusPort : ~LatchStatusPort;
        port motorCommandPort : MotorCommandPort;
        port buzzerCommandPort : BuzzerCommandPort;
    }

    part def DriveMotorModule {
        port motorCommandPort : ~MotorCommandPort;
    }

    part def PositionSensorModule {
        port positionStatusPort : PositionStatusPort;
    }

    part def PinchSensorModule {
        port pinchStatusPort : PinchStatusPort;
    }

    part def LatchModule {
        port latchStatusPort : LatchStatusPort;
    }

    part def BuzzerModule {
        port buzzerCommandPort : ~BuzzerCommandPort;
    }

    part def VehicleTailgateSystem {
        part bodyControl : BodyControlModule;
        part powerBackDoorSystem : PowerBackDoorSystem;
    }

    part systemUnderTest : VehicleTailgateSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;
    requirement requirement_004 : Req004;
    requirement requirement_005 : Req005;
    requirement requirement_006 : Req006;
    requirement requirement_007 : Req007;
    requirement requirement_008 : Req008;
    requirement requirement_009 : Req009;

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose LegacyAutoBackDoorCompleteJa::systemUnderTest;
            expose LegacyAutoBackDoorCompleteJa::systemUnderTest::bodyControl;
            expose LegacyAutoBackDoorCompleteJa::systemUnderTest::powerBackDoorSystem;
        }
    }
}
