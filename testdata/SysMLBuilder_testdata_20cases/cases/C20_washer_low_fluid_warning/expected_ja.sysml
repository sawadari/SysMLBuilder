package C20WasherLowFluidWarning {
    doc /*
    C20 ウォッシャ液残量低下警告
    このケースは、ウォッシャ液残量低下をデバウンス付きで検知し、補充後に警告を解除する機能を表します。
    */

    item def FluidLevelValue;
    item def DisplayCommandValue;

    port def FluidLevelPort {
        in item fluidLow : FluidLevelValue;
    }

    port def DisplayCommandPort {
        out item displayCommand : DisplayCommandValue;
    }

    interface def DisplayCommandInterface {
        end source : DisplayCommandPort;
        end target : ~DisplayCommandPort;
        flow source.displayCommand to target.displayCommand;
    }

    requirement def Req001 {
        doc /*
        C20-RQ-001: システムは、ウォッシャ液残量低下が2 s継続した場合、500 ms以内に残量低下警告を表示すること。
        */
    }

    requirement def Req002 {
        doc /*
        C20-RQ-002: システムは、2 s未満の一時的な低レベル検知に対して警告を表示しないこと。
        */
    }

    requirement def Req003 {
        doc /*
        C20-RQ-003: システムは、液量が正常状態で5 s継続した場合、警告を解除すること。
        */
    }

    part def FluidLevelMonitor {
        port fluidIn : FluidLevelPort;
        port displayOut : DisplayCommandPort;
    }

    part def ClusterDisplay {
        port commandIn : ~DisplayCommandPort;
    }

    part def WasherFluidWarningSystem {
        part monitor : FluidLevelMonitor;
        part display : ClusterDisplay;
    }

    part systemUnderTest : WasherFluidWarningSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;
}
