package C04HeadlampAutoOffDelay {
    doc /*
    C04 ヘッドランプ自動消灯遅延
    このケースは、イグニッションOFF後のヘッドランプ遅延消灯と、手動操作によるタイマ解除を表します。
    */

    item def IgnitionStatusValue;
    item def DoorStatusValue;
    item def LampCommandValue;

    port def IgnitionStatusPort {
        in item ignitionOn : IgnitionStatusValue;
    }

    port def DoorStatusPort {
        in item driverDoorOpen : DoorStatusValue;
    }

    port def LampCommandPort {
        out item lampCommand : LampCommandValue;
    }

    interface def LampCommandInterface {
        end source : LampCommandPort;
        end target : ~LampCommandPort;
        flow source.lampCommand to target.lampCommand;
    }

    requirement def Req001 {
        doc /*
        C04-RQ-001: システムは、イグニッションがOFFになり運転席ドアが閉じている場合、30 s後にヘッドランプを消灯すること。
        */
    }

    requirement def Req002 {
        doc /*
        C04-RQ-002: システムは、ユーザーがヘッドランプを再度手動でONした場合、自動消灯タイマを解除すること。
        */
    }

    requirement def Req003 {
        doc /*
        C04-RQ-003: システムは、運転席ドアが開いている間、ヘッドランプを点灯状態に維持すること。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C04-RQ-001: システムは、イグニッションがOFFになり運転席ドアが閉じている場合、30 s後にヘッドランプを消灯すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C04-RQ-002: システムは、ユーザーがヘッドランプを再度手動でONした場合、自動消灯タイマを解除すること。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C04-RQ-003: システムは、運転席ドアが開いている間、ヘッドランプを点灯状態に維持すること。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def HeadlampController {
        state def HeadlampTimerStates {
            entry; then active;

            state active;

            transition active_to_timerRunning
                first active
                then timerRunning;

            state timerRunning;

            transition timerRunning_to_off
                first timerRunning
                then off;

            state off;

            transition off_to_active
                first off
                then active;

        }

        port ignitionIn : IgnitionStatusPort;
        port doorStatusIn : DoorStatusPort;
        port commandOut : LampCommandPort;
    }

    part def HeadlampRelay {
        port commandIn : ~LampCommandPort;
    }

    part def HeadlampControlSystem {
        part controller : HeadlampController;
        part relay : HeadlampRelay;
    }

    part systemUnderTest : HeadlampControlSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C04HeadlampAutoOffDelayStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C04HeadlampAutoOffDelay::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C04HeadlampAutoOffDelay::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C04HeadlampAutoOffDelay::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C04HeadlampAutoOffDelay::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C04HeadlampAutoOffDelay::**;
    }
}
