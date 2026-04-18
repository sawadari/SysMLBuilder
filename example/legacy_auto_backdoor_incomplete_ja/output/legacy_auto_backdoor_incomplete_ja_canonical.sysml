package LegacyAutoBackDoorIncompleteJa {
    doc /*
    LEGACY_ABD_INCOMPLETE_JA 自動バックドア制御 不足情報版 参考入力
    
    */

    item def VehicleStatusSignal;
    item def DoorRequestSignal;
    item def PositionStatusSignal;
    item def PinchStatusSignal;
    item def MotorCommandSignal;

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

    port def MotorCommandPort {
        out item motorCommand : MotorCommandSignal;
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
        ABD-REQ-101: ShiftPos が P であり、車両が低速時のみ、BackDoorOpenReq を開要求として受け付けなければならない。
        */
    }

    requirement def Req002 {
        doc /*
        ABD-REQ-103: 開要求を受け付けた場合、所定時間以内に駆動モータへ開方向駆動を指示しなければならない。
        */
    }

    requirement def Req003 {
        doc /*
        ABD-REQ-104: バックドアがほぼ全開となった場合、駆動モータを停止し、状態を全開へ遷移しなければならない。
        */
    }

    requirement def Req004 {
        doc /*
        ABD-REQ-105: 短時間で閉方向駆動を停止し、その後に開方向へ反転しなければならない。
        */
    }

    requirement def Req005 {
        doc /*
        ABD-REQ-106: センサ異常を検知した場合、異常停止状態へ遷移しなければならない。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* ABD-REQ-101: ShiftPos が P であり、車両が低速時のみ、BackDoorOpenReq を開要求として受け付けなければならない。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* ABD-REQ-103: 開要求を受け付けた場合、所定時間以内に駆動モータへ開方向駆動を指示しなければならない。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* ABD-REQ-104: バックドアがほぼ全開となった場合、駆動モータを停止し、状態を全開へ遷移しなければならない。 */
        action requirementStep004 : RequirementActivityStep;
        doc /* ABD-REQ-105: 短時間で閉方向駆動を停止し、その後に開方向へ反転しなければならない。 */
        action requirementStep005 : RequirementActivityStep;
        doc /* ABD-REQ-106: センサ異常を検知した場合、異常停止状態へ遷移しなければならない。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
        flow of ActivityToken from requirementStep003.outToken to requirementStep004.inToken;
        flow of ActivityToken from requirementStep004.outToken to requirementStep005.inToken;
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
        port motorCommandPort : MotorCommandPort;
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
    }

    part def BuzzerModule {
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

}

package LegacyAutoBackDoorIncompleteJaStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose LegacyAutoBackDoorIncompleteJa::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose LegacyAutoBackDoorIncompleteJa::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose LegacyAutoBackDoorIncompleteJa::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose LegacyAutoBackDoorIncompleteJa::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose LegacyAutoBackDoorIncompleteJa::**;
    }
}
