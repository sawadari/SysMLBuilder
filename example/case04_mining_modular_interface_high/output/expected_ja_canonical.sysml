package Case04MiningModularInterfaceHighExpected {

package DomainDefinitions {

  item def PowerSupply {
    attribute energyTransfer : ScalarValues::Real;
  }

  item def HighSlotCommand {
    attribute activation : ScalarValues::Boolean;
  }

  item def MediumSlotCommand {
    attribute activation : ScalarValues::Boolean;
  }

  port def HighSlotPort {
    in power : PowerSupply;
    in control : HighSlotCommand;
  }

  port def MediumSlotPort {
    in power : PowerSupply;
    in control : MediumSlotCommand;
  }

  interface def HighSlotInterface {
    end hullPort : HighSlotPort;
    end modulePort : ~HighSlotPort;
    flow of PowerSupply from hullPort.power to modulePort.power;
    flow of HighSlotCommand from hullPort.control to modulePort.control;
  }

  interface def MediumSlotInterface {
    end hullPort : MediumSlotPort;
    end modulePort : ~MediumSlotPort;
    flow of PowerSupply from hullPort.power to modulePort.power;
    flow of MediumSlotCommand from hullPort.control to modulePort.control;
  }

  part def MiningFrigateHull {
    port highSlot1 : HighSlotPort;
    port mediumSlot1 : MediumSlotPort;
  }

  part def MiningLaserModule {
    port modulePort : ~HighSlotPort;
  }

  part def ShieldHardenerModule {
    port modulePort : ~MediumSlotPort;
  }

  part def MiningFrigate {
    part hull : MiningFrigateHull;
    part miningLaser : MiningLaserModule;
    part shieldHardener : ShieldHardenerModule;
  }
}

package RequirementDefinitions {

  requirement def HighSlotInterfaceRequirement {
    subject hull : DomainDefinitions::MiningFrigateHull;
    doc /* 船体は採掘レーザーモジュールに対して型付きHighSlotインタフェースを提供しなければならない。 */
  }

  requirement def MediumSlotInterfaceRequirement {
    subject hull : DomainDefinitions::MiningFrigateHull;
    doc /* 船体はシールドハードナーモジュールに対して型付きMediumSlotインタフェースを提供しなければならない。 */
  }
}

package Requirements {
  requirement architectureSpecification {
    subject hull : DomainDefinitions::MiningFrigateHull;
    requirement highSlotInterfaceRequirement : RequirementDefinitions::HighSlotInterfaceRequirement;
    requirement mediumSlotInterfaceRequirement : RequirementDefinitions::MediumSlotInterfaceRequirement;
  }
}

package Structure {

  part frigate_ref : DomainDefinitions::MiningFrigate {
    part hull : DomainDefinitions::MiningFrigateHull;
    part miningLaser : DomainDefinitions::MiningLaserModule;
    part shieldHardener : DomainDefinitions::ShieldHardenerModule;

    interface miningLaserIf : DomainDefinitions::HighSlotInterface
      connect hull::highSlot1 to miningLaser::modulePort;

    interface shieldIf : DomainDefinitions::MediumSlotInterface
      connect hull::mediumSlot1 to shieldHardener::modulePort;
  }
}

package SatisfactionManifest {
  doc /* [satisfy] Requirements::architectureSpecification::highSlotInterfaceRequirement by Structure::frigate_ref::hull
         [satisfy] Requirements::architectureSpecification::mediumSlotInterfaceRequirement by Structure::frigate_ref::hull */
}

package AllocationManifest {
  doc /* [allocation] C-MFI-001 allocated_to Structure::frigate_ref::hull
         [allocation] C-MFI-002 allocated_to Structure::frigate_ref::hull
         [allocation] C-MFI-003 allocated_to Structure::frigate_ref::hull
         [allocation] C-MFI-004 allocated_to Structure::frigate_ref::hull */
}

package ViewDefinitions {
  private import Views::*;
  private import DS_Views::*;

  view miningFrigateInterconnectionView : DS_Views::SymbolicViews::gv {
    expose Structure::frigate_ref;
    expose Structure::frigate_ref::hull;
    expose Structure::frigate_ref::miningLaser;
    expose Structure::frigate_ref::shieldHardener;
  }
}

}
