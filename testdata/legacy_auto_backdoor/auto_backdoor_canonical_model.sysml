package AutoBackDoorCanonicalModel {

package Structure {

  item def VehicleSpeedSignal;
  item def ShiftPositionSignal;
  item def DoorOpenRequestSignal;
  item def DoorCloseRequestSignal;
  item def PositionStatusSignal;
  item def PinchStatusSignal;
  item def LatchStatusSignal;
  item def MotorCommandSignal;
  item def BuzzerCommandSignal;

  port def VehicleStatusPort {
    out item vehicleSpeed : VehicleSpeedSignal;
    out item shiftPosition : ShiftPositionSignal;
  }

  port def DoorRequestPort {
    out item openRequest : DoorOpenRequestSignal;
    out item closeRequest : DoorCloseRequestSignal;
  }

  port def PositionStatusPort {
    out item positionStatus : PositionStatusSignal;
  }

  port def PinchStatusPort {
    out item pinchStatus : PinchStatusSignal;
  }

  port def LatchStatusPort {
    out item latchStatus : LatchStatusSignal;
  }

  port def MotorCommandPort {
    out item motorCommand : MotorCommandSignal;
  }

  port def BuzzerCommandPort {
    out item buzzerCommand : BuzzerCommandSignal;
  }

  part def BodyControlModule {
    port vehicleStatusPort : VehicleStatusPort;
    port requestPort : DoorRequestPort;
  }

  part def BackDoorController {
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

  part def PowerBackDoorSystem {
    part controller : BackDoorController;
    part driveMotor : DriveMotorModule;
    part positionSensor : PositionSensorModule;
    part pinchSensor : PinchSensorModule;
    part latchModule : LatchModule;
    part buzzerModule : BuzzerModule;
  }

  part def VehicleTailgateSystem {
    part bodyControl : BodyControlModule;
    part powerBackDoorSystem : PowerBackDoorSystem;
  }
}

package RequirementPatternLibrary {

  requirement def GatedCapabilityRequirement {
    subject gatedSystem;
    doc /* Generic pattern: a system accepts or performs an action only when gate conditions hold. */
  }

  requirement def TimedCommandRequirement {
    subject controlledElement;
    attribute responseLimitValue : Integer;
    attribute responseLimitUnit : String;
    doc /* Generic pattern: a controlled element shall issue a command within a bounded time. */
  }

  requirement def ThresholdReactionRequirement {
    subject controlledElement;
    attribute thresholdValue : Integer;
    attribute thresholdUnit : String;
    doc /* Generic pattern: a controlled element reacts when a monitored signal crosses a threshold. */
  }

  requirement def FaultReactionRequirement {
    subject controlledElement;
    attribute firstReactionLimitValue : Integer;
    attribute firstReactionLimitUnit : String;
    attribute secondReactionLimitValue : Integer;
    attribute secondReactionLimitUnit : String;
    doc /* Generic pattern: stop hazardous motion first, then perform a safe reaction. */
  }

  requirement def FaultDetectionRequirement {
    subject controlledElement;
    attribute detectionLimitValue : Integer;
    attribute detectionLimitUnit : String;
    doc /* Generic pattern: detect a fault condition and move to a safe state. */
  }

  requirement def StateTransitionRequirement {
    subject controlledElement;
    doc /* Generic pattern: transition from source state to target state on an event. */
  }
}

package Requirements {

  requirement def ABD_REQ_001_OpenRequestAcceptance :> GatedCapabilityRequirement {
    subject subjectSystem : Structure::PowerBackDoorSystem;
    doc /* [source-requirement-id] ABD-REQ-001
           [pattern-id] gated_capability
           [evidence] ShiftPos が P であり、VehSpd が 3 km/h 未満の場合にのみ、BackDoorOpenReq を開要求として受け付けなければならない。 */
  }

  requirement def ABD_REQ_003_OpenCommandStart :> TimedCommandRequirement {
    subject subjectController : Structure::BackDoorController;
    attribute responseLimitValue = 100;
    attribute responseLimitUnit = "ms";
    doc /* [source-requirement-id] ABD-REQ-003
           [pattern-id] timed_command
           [evidence] 開要求を受け付けた場合、100 ms 以内に駆動モータへ開方向駆動を指示しなければならない。 */
  }

  requirement def ABD_REQ_004_OpenCompleteStop :> ThresholdReactionRequirement {
    subject subjectController : Structure::BackDoorController;
    attribute thresholdValue = 95;
    attribute thresholdUnit = "%";
    doc /* [source-requirement-id] ABD-REQ-004
           [pattern-id] threshold_stop_or_transition
           [evidence] BackDoorPos が 95 % 以上となった場合、駆動モータを停止し、状態を全開へ遷移しなければならない。 */
  }

  requirement def ABD_REQ_007_PinchReaction :> FaultReactionRequirement {
    subject subjectController : Structure::BackDoorController;
    attribute firstReactionLimitValue = 50;
    attribute firstReactionLimitUnit = "ms";
    attribute secondReactionLimitValue = 200;
    attribute secondReactionLimitUnit = "ms";
    doc /* [source-requirement-id] ABD-REQ-007
           [pattern-id] fault_reaction
           [evidence] 閉動作中に PinchDetected = true を検知した場合、50 ms 以内に閉方向駆動を停止し、200 ms 以内に開方向へ反転しなければならない。 */
  }

  requirement def ABD_REQ_009_BuzzerAfterFaultStop :> TimedCommandRequirement {
    subject subjectController : Structure::BackDoorController;
    attribute responseLimitValue = 1;
    attribute responseLimitUnit = "s";
    doc /* [source-requirement-id] ABD-REQ-009
           [pattern-id] timed_command
           [evidence] 異常停止状態へ遷移した場合、1 s 以内に BuzzerReq を true にしなければならない。 */
  }

  requirement def ABD_REQ_010_PositionTimeoutFault :> FaultDetectionRequirement {
    subject subjectController : Structure::BackDoorController;
    attribute detectionLimitValue = 500;
    attribute detectionLimitUnit = "ms";
    doc /* [source-requirement-id] ABD-REQ-010
           [pattern-id] fault_detection
           [evidence] 開度センサ値が 500 ms 以上更新されない場合、異常停止状態へ遷移しなければならない。 */
  }

  requirement def ABD_REQ_012_ClosedToOpening :> StateTransitionRequirement {
    subject subjectController : Structure::BackDoorController;
    doc /* [source-requirement-id] ABD-REQ-012
           [pattern-id] state_transition
           [evidence] 全閉状態で開要求を受け付けた場合、開動作中へ遷移しなければならない。 */
  }

  requirement def ABD_REQ_015_ClosingToReverseOpening :> StateTransitionRequirement {
    subject subjectController : Structure::BackDoorController;
    doc /* [source-requirement-id] ABD-REQ-015
           [pattern-id] state_transition
           [evidence] 閉動作中で挟み込み検知した場合、反転開へ遷移しなければならない。 */
  }
}

package Interfaces {

  interface extVehicleStatus connect Structure::VehicleTailgateSystem::bodyControl.vehicleStatusPort
      to Structure::VehicleTailgateSystem::powerBackDoorSystem.controller.vehicleStatusPort;

  interface extDoorRequest connect Structure::VehicleTailgateSystem::bodyControl.requestPort
      to Structure::VehicleTailgateSystem::powerBackDoorSystem.controller.requestPort;

  interface intMotorCommand connect Structure::PowerBackDoorSystem::controller.motorCommandPort
      to Structure::PowerBackDoorSystem::driveMotor.motorCommandPort;

  interface intPositionStatus connect Structure::PowerBackDoorSystem::positionSensor.positionStatusPort
      to Structure::PowerBackDoorSystem::controller.positionStatusPort;

  interface intPinchStatus connect Structure::PowerBackDoorSystem::pinchSensor.pinchStatusPort
      to Structure::PowerBackDoorSystem::controller.pinchStatusPort;

  interface intLatchStatus connect Structure::PowerBackDoorSystem::latchModule.latchStatusPort
      to Structure::PowerBackDoorSystem::controller.latchStatusPort;

  interface intBuzzerCommand connect Structure::PowerBackDoorSystem::controller.buzzerCommandPort
      to Structure::PowerBackDoorSystem::buzzerModule.buzzerCommandPort;
}

package AllocationManifest {
  doc /* exact allocation records are maintained in auto_backdoor_projection_manifest.yaml
         [allocation] RC-ABD-001 allocates_to PowerBackDoorSystem.controller
         [allocation] RC-ABD-003 allocates_to PowerBackDoorSystem.controller
         [allocation] RC-ABD-004 allocates_to PowerBackDoorSystem.controller
         [allocation] RC-ABD-007 allocates_to PowerBackDoorSystem.controller
         [allocation] RC-ABD-009 allocates_to PowerBackDoorSystem.controller
         [allocation] RC-ABD-010 allocates_to PowerBackDoorSystem.controller */
}

package SatisfactionManifest {
  doc /* exact satisfy claims are maintained in auto_backdoor_projection_manifest.yaml
         [satisfy] ABD_REQ_001_OpenRequestAcceptance by PowerBackDoorSystem.controller
         [satisfy] ABD_REQ_003_OpenCommandStart by PowerBackDoorSystem.controller
         [satisfy] ABD_REQ_004_OpenCompleteStop by PowerBackDoorSystem.controller
         [satisfy] ABD_REQ_007_PinchReaction by PowerBackDoorSystem.controller
         [satisfy] ABD_REQ_009_BuzzerAfterFaultStop by PowerBackDoorSystem.controller
         [satisfy] ABD_REQ_010_PositionTimeoutFault by PowerBackDoorSystem.controller */
}

package ViewTargets {
  doc /* render target 1: Structure::VehicleTailgateSystem::powerBackDoorSystem as interconnection view
         render target 2: Structure::VehicleTailgateSystem as structural context view
         layout is intentionally not fixed in the canonical file. */
}

}
