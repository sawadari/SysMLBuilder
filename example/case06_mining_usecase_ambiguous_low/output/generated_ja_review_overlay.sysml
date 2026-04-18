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
           [rationale] 参照モデルの採掘ユースケースではパイロットと小惑星帯を用いている。
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
           [rationale] 参照モデルの脅威対処ユースケースでは敵対艦船とパイロットを用いている。
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
           [rationale] 参照モデルの補給ユースケースにはステーションアクターが含まれる。
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
  doc /* 効率的な採掘の具体的な成功定義は何か。
         どの具体的なトリガが脅威を対処対象にするのか。
         補給はどの時点で必要かつ完了と見なされるのか。 */
}

package TraceWeaknesses {
  doc /* このケースは意図的に曖昧である。
         case05 と同じソースファイルを根拠にしているが、入力記述では運用構造の大半を省略している。 */
}

package ReviewGuide {
  doc /* [review-action] accept / modify / reject / defer
         アクター、目的テキスト、フロー構造が受理されるまで canonical なユースケースを出力してはならない。 */
}

}
