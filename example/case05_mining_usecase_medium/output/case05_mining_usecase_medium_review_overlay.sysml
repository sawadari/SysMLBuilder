package Case05MiningUseCaseMediumExpectedReview {

package DomainDefinitions {
  part def MiningFrigate;
}

package DraftRequirementContracts {

  requirement def DraftMineAsteroidsCompletionCriteria {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* [proposal-id] P-UC-001
           [source-contract] C-UC-001
           [source-requirement] UC-MF-001
           [missing-slot] success_thresholds
           [proposed-value] define ore extraction completion criteria and cargo-full threshold
           [rationale] The use case contains main and exception flows but does not define measurable success limits.
           [trace-quality] direct_file_grounded
           [confidence] 0.61
           [review-action] accept / modify / reject / defer */
  }

  requirement def DraftOffloadCompletionCriteria {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* [proposal-id] P-UC-002
           [source-contract] C-UC-002
           [source-requirement] UC-MF-002
           [missing-slot] completion_conditions
           [proposed-value] define successful docking, cargo transfer completion, and resupply completion criteria
           [rationale] The narrative preserves flow but not completion metrics.
           [trace-quality] direct_file_grounded
           [confidence] 0.60
           [review-action] accept / modify / reject / defer */
  }
}

package MissingSlots {
  doc /* UC-MF-001 missing: success_thresholds, time_limits, trigger_conditions
         UC-MF-002 missing: success_thresholds, completion_conditions */
}

package OpenQuestions {
  doc /* Should mining completion be measured by ore quantity, time, or cargo fill percentage?
         Should offload success be measured by all cargo transferred, minimum cargo transferred, or docking completion? */
}

package BehaviorCandidates {
  doc /* Candidate behavior decomposition:
         MineAsteroids -> target selection / mining activation / ore transfer / suspend on full cargo
         OffloadOreAndResupply -> docking / cargo transfer / resupply / abort on failure */
}

package ReviewGuide {
  doc /* [review-action] accept / modify / reject / defer
         Canonical use cases are acceptable, but quantitative success criteria remain unresolved. */
}

}
