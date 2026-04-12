package C10SteeringWheelHeaterAutoOff {
    doc /*
    C10 ステアリングヒータ自動オフ
    このケースは、周囲温度条件と自動タイムアウトを組み合わせたステアリングヒータを表します。
    */

    item def TemperatureValue;
    item def HeatingRequestValue;
    item def HeatingLevelValue;

    port def AmbientTemperaturePort {
        in item ambientTemperature : TemperatureValue;
    }

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
        C10-RQ-001: システムは、外気温が20℃を超える場合、ステアリングヒータ要求を拒否すること。
        */
    }

    requirement def Req002 {
        doc /*
        C10-RQ-002: システムは、加熱が30 min連続した後、ステアリングヒータをOFFにすること。
        */
    }

    requirement def Req003 {
        doc /*
        C10-RQ-003: システムは、イグニッションサイクルごとにヒータ状態をOFFへ戻すこと。
        */
    }

    part def SteeringWheelHeaterController {
        port tempIn : AmbientTemperaturePort;
        port requestIn : HeatingRequestPort;
        port levelOut : HeatingLevelPort;
    }

    part def SteeringWheelHeaterElement {
        port levelIn : ~HeatingLevelPort;
    }

    part def SteeringWheelHeaterSystem {
        part controller : SteeringWheelHeaterController;
        part element : SteeringWheelHeaterElement;
    }

    part systemUnderTest : SteeringWheelHeaterSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C10SteeringWheelHeaterAutoOff::systemUnderTest;
            expose C10SteeringWheelHeaterAutoOff::systemUnderTest::controller;
            expose C10SteeringWheelHeaterAutoOff::systemUnderTest::element;
        }
    }
}
