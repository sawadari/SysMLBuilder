package C02AutoWindowAntiPinch {
    doc /*
    C02 Auto Window Anti-Pinch
    This case models an automatic window feature with anti-pinch protection and a door-open inhibit condition.
    */

    item def WindowSwitchValue;
    item def DoorStatusValue;
    item def PinchSignalValue;
    item def WindowMotorCommandValue;

    port def WindowSwitchPort {
        in item closeRequest : WindowSwitchValue;
    }

    port def DoorStatusPort {
        in item doorOpen : DoorStatusValue;
    }

    port def PinchSignalPort {
        in item pinchDetected : PinchSignalValue;
    }

    port def WindowMotorCommandPort {
        out item windowCommand : WindowMotorCommandValue;
    }

    interface def WindowMotorCommandInterface {
        end source : WindowMotorCommandPort;
        end target : ~WindowMotorCommandPort;
        flow source.windowCommand to target.windowCommand;
    }

    requirement def Req001 {
        doc /*
        C02-RQ-001: The auto window system shall start automatic closing when the close switch is held for at least 300 ms.
        */
    }

    requirement def Req002 {
        doc /*
        C02-RQ-002: The system shall inhibit automatic closing while the corresponding door is open.
        */
    }

    requirement def Req003 {
        doc /*
        C02-RQ-003: When pinch is detected during automatic closing, the system shall stop within 30 ms and lower the glass by at least 100 mm.
        */
    }

    part def WindowController {
        state def WindowMotionStates {
            entry; then idle;

            state idle;

            transition idle_to_autoClosing
                first idle
                then autoClosing;

            state autoClosing;

            transition autoClosing_to_reverseOpen
                first autoClosing
                then reverseOpen;

            state reverseOpen;

            transition reverseOpen_to_idle
                first reverseOpen
                then idle;

        }

        port switchIn : WindowSwitchPort;
        port doorStatusIn : DoorStatusPort;
        port pinchIn : PinchSignalPort;
        port commandOut : WindowMotorCommandPort;
    }

    part def WindowMotor {
        port commandIn : ~WindowMotorCommandPort;
    }

    part def PinchSensor {
        port pinchOut : PinchSignalPort;
    }

    part def AutoWindowSystem {
        part controller : WindowController;
        part motor : WindowMotor;
        part sensor : PinchSensor;
    }

    part systemUnderTest : AutoWindowSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;

    package ViewDefinitions {
        private import Views::*;
        private import DS_Views::*;

        view systemContextView : DS_Views::SymbolicViews::gv {
            expose C02AutoWindowAntiPinch::systemUnderTest;
            expose C02AutoWindowAntiPinch::systemUnderTest::controller;
            expose C02AutoWindowAntiPinch::systemUnderTest::motor;
            expose C02AutoWindowAntiPinch::systemUnderTest::sensor;
        }
    }
}
