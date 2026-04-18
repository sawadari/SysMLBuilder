package Case02VehicleAmbiguousLowExpectedReview {

package DomainDefinitions {
  part def Vehicle;
  part def Engine;
}

package DraftRequirementContracts {

  requirement def DraftVehicleMassRequirement {
    subject vehicle : DomainDefinitions::Vehicle;
    doc /* [proposal-id] P-VEH-L-001
           [source-contract] C-VEH-L-001
           [source-requirement] REQ-VEH-L-001
           [missing-slot] threshold_value
           [proposed-value] 2000
           [rationale] VehicleModel uses explicit quantitative mass requirements.
           [trace-quality] direct_file_grounded
           [confidence] 0.56
           [review-action] accept / modify / reject / defer */
  }

  requirement def DraftVehicleFuelEconomyContext {
    subject vehicle : DomainDefinitions::Vehicle;
    doc /* [proposal-id] P-VEH-L-003
           [source-contract] C-VEH-L-002
           [source-requirement] REQ-VEH-L-002
           [missing-slot] operating_contexts
           [proposed-value] CityNominal and HighwayNominal
           [rationale] VehicleModel separates city and highway fuel economy requirements.
           [trace-quality] direct_file_grounded
           [confidence] 0.58
           [review-action] accept / modify / reject / defer */
  }

  requirement def DraftVehicleDrivePowerInterface {
    subject engine : DomainDefinitions::Engine;
    doc /* [proposal-id] P-VEH-L-004
           [source-contract] C-VEH-L-003
           [source-requirement] REQ-VEH-L-003
           [missing-slot] interface_name
           [proposed-value] EngineToTransmissionInterface
           [rationale] VehicleModel defines an EngineToTransmissionInterface between engine and transmission.
           [trace-quality] direct_file_grounded
           [confidence] 0.68
           [review-action] accept / modify / reject / defer */
  }
}

package MissingSlots {
  doc /* REQ-VEH-L-001 missing: measured_property, threshold_value, threshold_unit
         REQ-VEH-L-002 missing: operating_contexts, threshold_value, threshold_unit
         REQ-VEH-L-003 missing: interface_name, interface_ends, flows */
}

package OpenQuestions {
  doc /* Is lightweight a mass threshold or an acceleration/performance surrogate?
         Should fuel efficiency be split into city and highway contexts?
         Does reliable drive power imply an interface requirement, a performance requirement, or both? */
}

package Assumptions {
  doc /* Assumption A1: lightweight most likely maps to mass.
         Assumption A2: fuel efficient most likely maps to city/highway fuel economy.
         Assumption A3: drive power transfer most likely maps to a named interface. */
}

package TraceWeaknesses {
  doc /* The input is intentionally ambiguous.
         The review overlay should remain the source of truth until the missing quantitative slots are accepted. */
}

package ReviewGuide {
  doc /* [review-action] accept / modify / reject / defer
         Do not promote any draft to canonical until all missing quantitative slots are resolved. */
}

}
