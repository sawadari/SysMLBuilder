package C16TrailerLampInterface {
    doc /*
    C16 トレーラランプインタフェース
    このケースは、トレーラコントローラとトレーラランプコネクタ間の型付き信号インタフェースに焦点を当てます。
    */

    item def LampCommandValue;
    item def TrailerPresenceValue;

    port def LeftTurnLampPort {
        out item leftTurnLampCommand : LampCommandValue;
    }

    port def RightTurnLampPort {
        out item rightTurnLampCommand : LampCommandValue;
    }

    port def StopLampPort {
        out item stopLampCommand : LampCommandValue;
    }

    port def TrailerPresencePort {
        in item trailerDetected : TrailerPresenceValue;
    }

    interface def LeftTurnLampInterface {
        end source : LeftTurnLampPort;
        end target : ~LeftTurnLampPort;
        flow source.leftTurnLampCommand to target.leftTurnLampCommand;
    }

    interface def RightTurnLampInterface {
        end source : RightTurnLampPort;
        end target : ~RightTurnLampPort;
        flow source.rightTurnLampCommand to target.rightTurnLampCommand;
    }

    interface def StopLampInterface {
        end source : StopLampPort;
        end target : ~StopLampPort;
        flow source.stopLampCommand to target.stopLampCommand;
    }

    requirement def Req001 {
        doc /*
        C16-RQ-001: トレーラランプコントローラは、左方向指示、右方向指示、および制動灯の各指令をトレーラコネクタインタフェースへ出力すること。
        */
    }

    requirement def Req002 {
        doc /*
        C16-RQ-002: システムは、コネクタ導通が失われた後500 ms以内にトレーラ切断を検知すること。
        */
    }

    requirement def Req003 {
        doc /*
        C16-RQ-003: システムは、トレーラ未接続時にトレーラランプ指令を抑止すること。
        */
    }

    part def TrailerLampController {
        port trailerPresenceIn : TrailerPresencePort;
        port leftOut : LeftTurnLampPort;
        port rightOut : RightTurnLampPort;
        port stopOut : StopLampPort;
    }

    part def TrailerConnector {
        port leftIn : ~LeftTurnLampPort;
        port rightIn : ~RightTurnLampPort;
        port stopIn : ~StopLampPort;
    }

    part def TrailerLampSystem {
        part controller : TrailerLampController;
        part connector : TrailerConnector;
    }

    part systemUnderTest : TrailerLampSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;
}
