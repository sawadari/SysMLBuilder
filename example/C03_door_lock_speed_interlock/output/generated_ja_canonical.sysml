package C03DoorLockSpeedInterlock {
    doc /*
    C03 ドアロック車速連動
    このケースは、車速、シフト位置、ドア状態に基づく自動ロック・自動アンロックを表します。
    */

    item def VehicleSpeedValue;
    item def DoorStatusValue;
    item def ShiftPositionValue;
    item def DoorLockCommandValue;

    port def VehicleSpeedPort {
        in item vehicleSpeed : VehicleSpeedValue;
    }

    port def DoorStatusPort {
        in item doorAjar : DoorStatusValue;
    }

    port def ShiftPositionPort {
        in item shiftPosition : ShiftPositionValue;
    }

    port def DoorLockCommandPort {
        out item lockCommand : DoorLockCommandValue;
    }

    interface def DoorLockCommandInterface {
        end source : DoorLockCommandPort;
        end target : ~DoorLockCommandPort;
        flow source.lockCommand to target.lockCommand;
    }

    requirement def Req001 {
        doc /*
        C03-RQ-001: ドアロックシステムは、車速が20 km/h以上の状態が3 s継続した場合、全ドアを施錠すること。
        */
    }

    requirement def Req002 {
        doc /*
        C03-RQ-002: システムは、いずれかのドアが半ドアの間、自動施錠を実行しないこと。
        */
    }

    requirement def Req003 {
        doc /*
        C03-RQ-003: システムは、イグニッションがOFFでシフト位置がPに変化した場合、500 ms以内に運転席ドアを解錠すること。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C03-RQ-001: ドアロックシステムは、車速が20 km/h以上の状態が3 s継続した場合、全ドアを施錠すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C03-RQ-002: システムは、いずれかのドアが半ドアの間、自動施錠を実行しないこと。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C03-RQ-003: システムは、イグニッションがOFFでシフト位置がPに変化した場合、500 ms以内に運転席ドアを解錠すること。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def DoorLockController {
        port speedIn : VehicleSpeedPort;
        port doorStatusIn : DoorStatusPort;
        port shiftIn : ShiftPositionPort;
        port commandOut : DoorLockCommandPort;
    }

    part def DoorLockActuator {
        port commandIn : ~DoorLockCommandPort;
    }

    part def DoorLockSystem {
        part controller : DoorLockController;
        part actuator : DoorLockActuator;
    }

    part systemUnderTest : DoorLockSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C03DoorLockSpeedInterlockStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C03DoorLockSpeedInterlock::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C03DoorLockSpeedInterlock::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C03DoorLockSpeedInterlock::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C03DoorLockSpeedInterlock::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C03DoorLockSpeedInterlock::**;
    }
}
