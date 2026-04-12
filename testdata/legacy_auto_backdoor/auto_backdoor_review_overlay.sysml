package AutoBackDoorReviewOverlay {

package DraftRequirementContracts {

  requirement def Draft_RCI_ABD_101_SpeedThreshold {
    subject subjectSystem : AutoBackDoorCanonicalModel::Structure::PowerBackDoorSystem;
    doc /* [proposal-id] ABD-PROP-001
           [source-contract] RCI-ABD-101
           [source-requirement] ABD-REQ-101
           [missing-slot] VehSpd threshold
           [proposed-value] VehSpd < 3 km/h
           [rationale] 低速時のみという表現を停車近傍条件へ正規化した仮案。
           [confidence] 0.83
           [review-action] accept / modify / reject / defer */
  }

  requirement def Draft_RCI_ABD_103_ResponseLimit {
    subject subjectController : AutoBackDoorCanonicalModel::Structure::BackDoorController;
    doc /* [proposal-id] ABD-PROP-002
           [source-contract] RCI-ABD-103
           [source-requirement] ABD-REQ-103
           [missing-slot] response limit
           [proposed-value] 100 ms
           [rationale] 制御応答時間として既存サンプルで使いやすい初期仮案。
           [confidence] 0.86
           [review-action] accept / modify / reject / defer */
  }

  requirement def Draft_RCI_ABD_104_FullOpenThreshold {
    subject subjectController : AutoBackDoorCanonicalModel::Structure::BackDoorController;
    doc /* [proposal-id] ABD-PROP-003
           [source-contract] RCI-ABD-104
           [source-requirement] ABD-REQ-104
           [missing-slot] full open threshold
           [proposed-value] BackDoorPos >= 95 %
           [rationale] 「ほぼ全開」をテスト可能な閾値へ正規化した仮案。
           [confidence] 0.81
           [review-action] accept / modify / reject / defer */
  }

  requirement def Draft_RCI_ABD_105_StopLimit {
    subject subjectController : AutoBackDoorCanonicalModel::Structure::BackDoorController;
    doc /* [proposal-id] ABD-PROP-004
           [source-contract] RCI-ABD-105
           [source-requirement] ABD-REQ-105
           [missing-slot] stop limit
           [proposed-value] 50 ms
           [rationale] 安全反応時間の初期仮案。
           [confidence] 0.79
           [review-action] accept / modify / reject / defer */
  }

  requirement def Draft_RCI_ABD_105_ReverseLimit {
    subject subjectController : AutoBackDoorCanonicalModel::Structure::BackDoorController;
    doc /* [proposal-id] ABD-PROP-005
           [source-contract] RCI-ABD-105
           [source-requirement] ABD-REQ-105
           [missing-slot] reverse limit
           [proposed-value] 200 ms
           [rationale] 停止後の反転開始時間の初期仮案。
           [confidence] 0.79
           [review-action] accept / modify / reject / defer */
  }

  requirement def Draft_RCI_ABD_106_FaultDefinition {
    subject subjectController : AutoBackDoorCanonicalModel::Structure::BackDoorController;
    doc /* [proposal-id] ABD-PROP-006
           [source-contract] RCI-ABD-106
           [source-requirement] ABD-REQ-106
           [missing-slot] fault definition
           [proposed-value] 開度センサ更新停止 500 ms
           [rationale] センサ異常を最小限でテスト可能な形へ落とす仮案。
           [confidence] 0.74
           [review-action] accept / modify / reject / defer */
  }
}

package MissingSlots {
  doc /* [missing-slot-summary]
         RCI-ABD-101 : VehSpd threshold
         RCI-ABD-103 : response limit
         RCI-ABD-104 : full open threshold
         RCI-ABD-105 : stop limit, reverse limit
         RCI-ABD-106 : fault definition */
}

package OpenQuestions {
  requirement def Question_RCI_ABD_106_Scope {
    subject subjectController : AutoBackDoorCanonicalModel::Structure::BackDoorController;
    doc /* [open-question] 「センサ異常」は開度センサのみか、挟み込みセンサやラッチ異常も含むか。
           [review-action] accept / modify / reject / defer */
  }
}

package Assumptions {
  requirement def Assumption_LowSpeedMeansNearStandstill {
    subject subjectSystem : AutoBackDoorCanonicalModel::Structure::PowerBackDoorSystem;
    doc /* [assumption] 「低速時」は停車近傍条件を意味するものとして仮置きする。
           [review-action] accept / modify / reject / defer */
  }
}

package BehaviorCandidates {
  requirement def Candidate_ClosedToOpening {
    subject subjectController : AutoBackDoorCanonicalModel::Structure::BackDoorController;
    doc /* [candidate-type] transition
           [source-state] Closed
           [target-state] Opening
           [event] accepted_open_request
           [status] review_required
           [review-action] accept / modify / reject / defer */
  }

  requirement def Candidate_ClosingToReverseOpening {
    subject subjectController : AutoBackDoorCanonicalModel::Structure::BackDoorController;
    doc /* [candidate-type] transition
           [source-state] Closing
           [target-state] ReverseOpening
           [event] PinchDetected == true
           [status] review_required
           [review-action] accept / modify / reject / defer */
  }
}

package ReviewGuide {
  doc /* review overlay only.
         accepted proposals are written into review_decisions_template.yaml and promoted on the next run.
         deferred or rejected proposals must not be copied into the canonical model. */
}

}
