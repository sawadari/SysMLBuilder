package C09SeatHeaterAutoOff {
    doc /*
    C09 シートヒータ自動オフ
    このケースは、時間経過に応じて段下げとOFFを行うシートヒータを表します。
    */

    item def HeatingRequestValue;
    item def HeatingLevelValue;

    port def HeatingRequestPort {
        in item heaterRequest : HeatingRequestValue;
    }

    port def HeatingLevelPort {
        out item heatingLevelCommand : HeatingLevelValue;
    }

    interface def HeatingLevelInterface {
        end source : HeatingLevelPort;
        end target : ~HeatingLevelPort;
        flow source.heatingLevelCommand to target.heatingLevelCommand;
    }

    requirement def Req001 {
        doc /*
        C09-RQ-001: シートヒータは、ユーザー起動直後にHIGHレベルを許可すること。
        */
    }

    requirement def Req002 {
        doc /*
        C09-RQ-002: システムは、HIGHレベル連続動作が30 min継続した場合、HIGHからMEDIUMへ変更すること。
        */
    }

    requirement def Req003 {
        doc /*
        C09-RQ-003: システムは、加熱動作が合計60 min継続した場合、シートヒータをOFFにすること。
        */
    }

    item def ActivityToken;

    action def RequirementActivityStep {
        in item inToken : ActivityToken;
        out item outToken : ActivityToken;
    }

    action systemActivity {
        action requirementStep001 : RequirementActivityStep;
        doc /* C09-RQ-001: シートヒータは、ユーザー起動直後にHIGHレベルを許可すること。 */
        action requirementStep002 : RequirementActivityStep;
        doc /* C09-RQ-002: システムは、HIGHレベル連続動作が30 min継続した場合、HIGHからMEDIUMへ変更すること。 */
        action requirementStep003 : RequirementActivityStep;
        doc /* C09-RQ-003: システムは、加熱動作が合計60 min継続した場合、シートヒータをOFFにすること。 */

        flow of ActivityToken from requirementStep001.outToken to requirementStep002.inToken;
        flow of ActivityToken from requirementStep002.outToken to requirementStep003.inToken;
    }

    part def SeatHeaterController {
        state def SeatHeaterLevels {
            entry; then off;

            state off;

            transition off_to_high
                first off
                then high;

            state high;

            transition high_to_medium
                first high
                then medium;

            state medium;

            transition medium_to_off
                first medium
                then off;

        }

        port requestIn : HeatingRequestPort;
        port levelOut : HeatingLevelPort;
    }

    part def SeatHeaterElement {
        port levelIn : ~HeatingLevelPort;
    }

    part def SeatHeaterSystem {
        part controller : SeatHeaterController;
        part element : SeatHeaterElement;
    }

    part systemUnderTest : SeatHeaterSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

}

package C09SeatHeaterAutoOffStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose C09SeatHeaterAutoOff::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose C09SeatHeaterAutoOff::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose C09SeatHeaterAutoOff::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose C09SeatHeaterAutoOff::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose C09SeatHeaterAutoOff::**;
    }
}
