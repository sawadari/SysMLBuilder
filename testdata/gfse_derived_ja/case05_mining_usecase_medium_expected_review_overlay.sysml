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
           [proposed-value] 鉱石採取の完了基準と貨物満杯閾値を定義する
           [rationale] このユースケースはメインフローと例外フローを含むが、測定可能な成功限界を定義していない。
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
           [proposed-value] 成功したドッキング、貨物移送完了、補給完了の基準を定義する
           [rationale] この記述はフローを保持しているが完了指標は保持していない。
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
  doc /* 採掘完了は鉱石量、時間、貨物充填率のどれで測るべきか。
         荷下ろし成功は全貨物移送、最小貨物移送、ドッキング完了のどれで測るべきか。 */
}

package BehaviorCandidates {
  doc /* 候補となる振る舞い分解:
         MineAsteroids -> target selection / mining activation / ore transfer / suspend on full cargo
         OffloadOreAndResupply -> docking / cargo transfer / resupply / abort on failure */
}

package ReviewGuide {
  doc /* [review-action] accept / modify / reject / defer
         canonical なユースケース自体は受容可能だが、定量的な成功基準は未解決のままである。 */
}

}
