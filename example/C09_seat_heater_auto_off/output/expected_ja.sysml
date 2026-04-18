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

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C09SeatHeaterAutoOff::systemUnderTest;
            expose C09SeatHeaterAutoOff::systemUnderTest::controller;
            expose C09SeatHeaterAutoOff::systemUnderTest::element;
        }
    }
}
