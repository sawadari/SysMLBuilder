package C17OtaUpdatePreconditions {
    doc /*
    C17 OTA Update Preconditions
    This case models update-start gating and suspension conditions during an over-the-air software update.
    */

    item def VehicleParkValue;
    item def DoorLockStatusValue;
    item def BatterySocValue;
    item def UpdateControlValue;

    port def VehicleParkPort {
        in item vehicleParked : VehicleParkValue;
    }

    port def DoorLockStatusPort {
        in item doorsLocked : DoorLockStatusValue;
    }

    port def BatterySocPort {
        in item batterySoc : BatterySocValue;
    }

    port def UpdateControlPort {
        out item updateControl : UpdateControlValue;
    }

    interface def UpdateControlInterface {
        end source : UpdateControlPort;
        end target : ~UpdateControlPort;
        flow source.updateControl to target.updateControl;
    }

    requirement def Req001 {
        doc /*
        C17-RQ-001: The OTA update system shall start an update only when the vehicle is parked, doors are locked, and battery state of charge is at least 40 percent.
        */
    }

    requirement def Req002 {
        doc /*
        C17-RQ-002: When ignition turns ON during an update, the system shall suspend the update within 1 s.
        */
    }

    requirement def Req003 {
        doc /*
        C17-RQ-003: When any door is unlocked during an update, the system shall suspend the update within 1 s.
        */
    }

    part def UpdateManager {
        port updateControlOut : UpdateControlPort;
    }

    part def VehicleConditionMonitor {
        state def UpdateStates {
            entry; then idle;

            state idle;

            transition idle_to_updating
                first idle
                then updating;

            state updating;

            transition updating_to_suspended
                first updating
                then suspended;

            state suspended;

            transition suspended_to_idle
                first suspended
                then idle;

        }

        port parkIn : VehicleParkPort;
        port lockIn : DoorLockStatusPort;
        port socIn : BatterySocPort;
        port updateControlOut : UpdateControlPort;
    }

    part def OtaUpdateSystem {
        part manager : UpdateManager;
        part monitor : VehicleConditionMonitor;
    }

    part systemUnderTest : OtaUpdateSystem;

    requirement requirement_001 : Req001;
    requirement requirement_002 : Req002;
    requirement requirement_003 : Req003;
}
