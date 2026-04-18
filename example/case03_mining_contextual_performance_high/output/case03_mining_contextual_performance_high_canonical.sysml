package Case03MiningContextualPerformanceHighExpected {

package DomainDefinitions {

  part def MiningFrigate {
    attribute cargoCapacity : ScalarValues::Real;
    attribute shieldStrengthHS : ScalarValues::Real;
    attribute shieldStrengthLS : ScalarValues::Real;
  }
}

package RequirementDefinitions {

  requirement def CargoCapacityRequirement {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    attribute cargoCapacity : ScalarValues::Real;
    require constraint { cargoCapacity >= 5000.0 }
  }

  requirement def SurvivabilityRequirement {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    attribute shieldStrengthHS : ScalarValues::Real;
    attribute shieldStrengthLS : ScalarValues::Real;
    require constraint { shieldStrengthHS >= 200.0 }
    require constraint { shieldStrengthLS >= 400.0 }
  }
}

package Requirements {

  requirement miningFrigateSpecification {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    requirement cargoCapacityRequirement : RequirementDefinitions::CargoCapacityRequirement;
    requirement survivabilityRequirement : RequirementDefinitions::SurvivabilityRequirement;
  }
}

package Structure {

  part miningFrigate_ref : DomainDefinitions::MiningFrigate {
    attribute cargoCapacity = 6200.0;
    attribute shieldStrengthHS = 250.0;
    attribute shieldStrengthLS = 450.0;
  }
}

package SatisfactionManifest {
  doc /* [satisfy] Requirements::miningFrigateSpecification::cargoCapacityRequirement by Structure::miningFrigate_ref
         [satisfy] Requirements::miningFrigateSpecification::survivabilityRequirement by Structure::miningFrigate_ref */
}

package AllocationManifest {
  doc /* [allocation] C-MF-001 allocated_to Structure::miningFrigate_ref
         [allocation] C-MF-002 allocated_to Structure::miningFrigate_ref
         [allocation] C-MF-003 allocated_to Structure::miningFrigate_ref */
}

package ViewDefinitions {
  private import Views::*;
  private import DS_Views::*;

  view miningFrigateStructureView : DS_Views::SymbolicViews::gv {
    expose Structure::miningFrigate_ref;
  }
}

}

package Case03MiningContextualPerformanceHighExpectedStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose Case03MiningContextualPerformanceHighExpected::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose Case03MiningContextualPerformanceHighExpected::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose Case03MiningContextualPerformanceHighExpected::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose Case03MiningContextualPerformanceHighExpected::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose Case03MiningContextualPerformanceHighExpected::**;
    }
}
