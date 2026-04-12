package Case06MiningUseCaseAmbiguousLowExpectedReview {

package DomainDefinitions {
  part def MiningFrigate;
}

package DraftRequirementContracts {

  requirement def DraftMineAsteroidsUseCase {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* [proposal-id] P-UCL-001
           [source-contract] C-UCL-001
           [source-requirement] REQ-UC-L-001
           [missing-slot] actors
           [proposed-value] PilotPod and AsteroidBelt
           [rationale] Mining use cases in the reference model use a pilot and an asteroid belt.
           [trace-quality] direct_file_grounded
           [confidence] 0.72
           [review-action] accept / modify / reject / defer */
  }

  requirement def DraftDefenseUseCase {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* [proposal-id] P-UCL-002
           [source-contract] C-UCL-002
           [source-requirement] REQ-UC-L-002
           [missing-slot] actors
           [proposed-value] HostileShip and PilotPod
           [rationale] Threat engagement use cases in the reference model use hostile ships and the pilot.
           [trace-quality] direct_file_grounded
           [confidence] 0.71
           [review-action] accept / modify / reject / defer */
  }

  requirement def DraftResupplyUseCase {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* [proposal-id] P-UCL-003
           [source-contract] C-UCL-003
           [source-requirement] REQ-UC-L-003
           [missing-slot] actors
           [proposed-value] Station
           [rationale] Resupply use cases in the reference model involve a station actor.
           [trace-quality] direct_file_grounded
           [confidence] 0.70
           [review-action] accept / modify / reject / defer */
  }
}

package MissingSlots {
  doc /* REQ-UC-L-001 missing: objective_text, actors, main_flow_steps, success_thresholds
         REQ-UC-L-002 missing: objective_text, actors, trigger_conditions, exception_flow_steps
         REQ-UC-L-003 missing: objective_text, actors, trigger_conditions, completion_conditions */
}

package OpenQuestions {
  doc /* What is the concrete success definition for efficient mining?
         What specific trigger makes a threat actionable?
         When exactly is resupply considered necessary and complete? */
}

package TraceWeaknesses {
  doc /* This case is intentionally vague.
         It is grounded in the same source file as case05, but the input narrative omits most operational structure. */
}

package ReviewGuide {
  doc /* [review-action] accept / modify / reject / defer
         Do not emit canonical use cases until actors, objective text, and flow structure are accepted. */
}

}
