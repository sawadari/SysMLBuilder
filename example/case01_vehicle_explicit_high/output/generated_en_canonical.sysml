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

package ViewDefinitions {
  private import Views::*;
  private import DS_Views::*;

  view vehicleStructureView : DS_Views::SymbolicViews::gv {
    expose Structure::vehicle_b;
    expose Structure::vehicle_b::engine;
    expose Structure::vehicle_b::transmission;
  }
}

}

package Case01VehicleExplicitHighExpectedStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose Case01VehicleExplicitHighExpected::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose Case01VehicleExplicitHighExpected::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose Case01VehicleExplicitHighExpected::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose Case01VehicleExplicitHighExpected::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose Case01VehicleExplicitHighExpected::**;
    }
}
