package C06ClimateDefogPriority {
    doc /*
    C06 Climate Defog Priority
    This case coordinates blower level, compressor state, and outlet mode when front defog is requested.
    */

    item def DefogRequestValue;
    item def BlowerCommandValue;
    item def OutletModeValue;
    item def AcCommandValue;

    port def DefogRequestPort {
        in item defogRequest : DefogRequestValue;
    }

    port def BlowerCommandPort {
        out item blowerCommand : BlowerCommandValue;
    }

    port def OutletModePort {
        out item outletModeCommand : OutletModeValue;
    }

    port def AcCommandPort {
        out item acCommand : AcCommandValue;
    }

    interface def BlowerCommandInterface {
        end source : BlowerCommandPort;
        end target : ~BlowerCommandPort;
        flow source.blowerCommand to target.blowerCommand;
    }

    interface def OutletModeInterface {
        end source : OutletModePort;
        end target : ~OutletModePort;
        flow source.outletModeCommand to target.outletModeCommand;
    }

    interface def AcCommandInterface {
        end source : AcCommandPort;
        end target : ~AcCommandPort;
        flow source.acCommand to target.acCommand;
    }

    requirement def Req001 {
        doc /*
        C06-RQ-001: When front defog is requested, the HVAC system shall set blower level to 5 or higher within 500 ms.
        */
    }

    requirement def Req002 {
        doc /*
        C06-RQ-002: The system shall command the air outlet mode to windshield mode while front defog is active.
        */
    }

    requirement def Req003 {
        doc /*
        C06-RQ-003: The system shall turn the air conditioner ON while front defog is active unless compressor protection is active.
        */
    }

    part def HvacController {
        port defogIn : DefogRequestPort;
        port blowerOut : BlowerCommandPort;
        port outletModeOut : OutletModePort;
        port acOut : AcCommandPort;
    }

    part def BlowerActuator {
        port blowerIn : ~BlowerCommandPort;
    }

    part def AirMixActuator {
        port modeIn : ~OutletModePort;
    }

    part def CompressorRelay {
        port acIn : ~AcCommandPort;
    }

    part def ClimateDefogSystem {
        part controller : HvacController;
        part blower : BlowerActuator;
        part airMix : AirMixActuator;
        part compressor : CompressorRelay;
    }

    part systemUnderTest : ClimateDefogSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;
}
