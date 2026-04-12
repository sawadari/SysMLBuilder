package Case01VehicleExplicitHighExpected {

package DomainDefinitions {

  item def Torque;

  port def DrivePwrPort {
    out engineTorque : Torque;
  }

  port def ClutchPort;

  interface def EngineToTransmissionInterface {
    end p1 : DrivePwrPort;
    end p2 : ClutchPort;
  }

  part def Engine {
    port drivePwrPort : DrivePwrPort;
  }

  part def Transmission {
    port clutchPort : ~ClutchPort;
  }

  part def Vehicle {
    attribute mass : ScalarValues::Real;
    part engine : Engine;
    part transmission : Transmission;
  }
}

package RequirementDefinitions {

  requirement def MassRequirement {
    subject vehicle : DomainDefinitions::Vehicle;
    attribute actualMass : ScalarValues::Real;
    attribute requiredMass : ScalarValues::Real;
    require constraint { actualMass <= requiredMass }
  }

  requirement def FuelEconomyRequirement {
    subject vehicle : DomainDefinitions::Vehicle;
    attribute actualFuelEconomy : ScalarValues::Real;
    attribute requiredFuelEconomy : ScalarValues::Real;
    require constraint { actualFuelEconomy >= requiredFuelEconomy }
  }

  requirement def DrivePowerInterfaceRequirement {
    subject engine : DomainDefinitions::Engine;
    doc /* The engine shall transfer generated torque to the transmission through the clutch interface. */
  }
}

package Requirements {

  requirement vehicleSpecification {
    subject vehicle : DomainDefinitions::Vehicle;

    requirement vehicleMassRequirement : RequirementDefinitions::MassRequirement {
      redefines requiredMass = 2000;
    }

    requirement cityFuelEconomyRequirement : RequirementDefinitions::FuelEconomyRequirement {
      redefines requiredFuelEconomy = 25;
      attribute assumedCargoMass : ScalarValues::Real;
      assume constraint { assumedCargoMass >= 500 }
    }

    requirement highwayFuelEconomyRequirement : RequirementDefinitions::FuelEconomyRequirement {
      redefines requiredFuelEconomy = 30;
      attribute assumedCargoMass : ScalarValues::Real;
      assume constraint { assumedCargoMass >= 500 }
    }
  }

  requirement engineSpecification {
    subject engine : DomainDefinitions::Engine;
    requirement drivePowerInterface : RequirementDefinitions::DrivePowerInterfaceRequirement;
  }
}

package Structure {

  part vehicle_b : DomainDefinitions::Vehicle {
    attribute mass = 1950;
    part engine : DomainDefinitions::Engine;
    part transmission : DomainDefinitions::Transmission;

    interface engineToTransmissionInterface : DomainDefinitions::EngineToTransmissionInterface
      connect engine::drivePwrPort to transmission::clutchPort;
  }
}

package SatisfactionManifest {
  doc /* [satisfy] Requirements::vehicleSpecification::vehicleMassRequirement by Structure::vehicle_b
         [satisfy] Requirements::vehicleSpecification::cityFuelEconomyRequirement by Structure::vehicle_b
         [satisfy] Requirements::vehicleSpecification::highwayFuelEconomyRequirement by Structure::vehicle_b
         [satisfy] Requirements::engineSpecification::drivePowerInterface by Structure::vehicle_b::engine */
}

package AllocationManifest {
  doc /* [allocation] C-VEH-001 allocated_to Structure::vehicle_b
         [allocation] C-VEH-002 allocated_to Structure::vehicle_b
         [allocation] C-VEH-003 allocated_to Structure::vehicle_b
         [allocation] C-VEH-004 allocated_to Structure::vehicle_b::engine */
}

package ViewTargets {
  doc /* render target: Structure::vehicle_b as structural context view */
}

}
