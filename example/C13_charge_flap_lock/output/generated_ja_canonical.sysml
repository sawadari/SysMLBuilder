package C13ChargeFlapLockControl {
    doc /*
    C13 充電フラップロック制御
    このケースは、走行状態と充電状態に応じて充電フラップを施錠・解錠する機能を表します。
    */

    item def VehicleMotionValue;
    item def ChargingStatusValue;
    item def LockCommandValue;

    port def VehicleMotionPort {
        in item vehicleMoving : VehicleMotionValue;
    }

    port def ChargingStatusPort {
        in item chargingActive : ChargingStatusValue;
    }

    port def LockCommandPort {
        out item lockCommand : LockCommandValue;
    }

    interface def LockCommandInterface {
        end source : LockCommandPort;
        end target : ~LockCommandPort;
        flow source.lockCommand to target.lockCommand;
    }

    requirement def Req001 {
        doc /*
        C13-RQ-001: システムは、車両走行中に充電フラップを施錠すること。
        */
    }

    requirement def Req002 {
        doc /*
        C13-RQ-002: システムは、充電中に充電フラップを施錠すること。
        */
    }

    requirement def Req003 {
        doc /*
        C13-RQ-003: システムは、車両が駐車状態で充電完了時、または有効なユーザー解錠要求を受信した場合、充電フラップを解錠すること。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C13-RQ-001: システムは、車両走行中に充電フラップを施錠すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C13-RQ-002: システムは、充電中に充電フラップを施錠すること。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C13-RQ-003: システムは、車両が駐車状態で充電完了時、または有効なユーザー解錠要求を受信した場合、充電フラップを解錠すること。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def ChargeFlapController {
        port motionIn : VehicleMotionPort;
        port chargingIn : ChargingStatusPort;
        port commandOut : LockCommandPort;
    }

    part def ChargeFlapActuator {
        port commandIn : ~LockCommandPort;
    }

    part def ChargeFlapLockSystem {
        part controller : ChargeFlapController;
        part actuator : ChargeFlapActuator;
    }

    part systemUnderTest : ChargeFlapLockSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C13ChargeFlapLockControlStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C13ChargeFlapLockControl::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C13ChargeFlapLockControl::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C13ChargeFlapLockControl::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C13ChargeFlapLockControl::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C13ChargeFlapLockControl::**;
    }
}
