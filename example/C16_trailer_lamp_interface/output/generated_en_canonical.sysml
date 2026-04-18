package C16TrailerLampInterface {
    doc /*
    C16 Trailer Lamp Interface
    This case focuses on typed signal interfaces between the trailer controller and the trailer lamp connector.
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
        C16-RQ-001: The trailer lamp controller shall output left-turn, right-turn, and stop-lamp commands on the trailer connector interface.
        */
    }

    requirement def Req002 {
        doc /*
        C16-RQ-002: The system shall detect trailer disconnect within 500 ms after connector continuity is lost.
        */
    }

    requirement def Req003 {
        doc /*
        C16-RQ-003: The system shall suppress trailer-lamp commands when no trailer is detected.
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

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C16TrailerLampInterface::systemUnderTest;
            expose C16TrailerLampInterface::systemUnderTest::controller;
            expose C16TrailerLampInterface::systemUnderTest::connector;
        }
    }
}
