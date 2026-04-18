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
           [rationale] VehicleModel では明示的な定量質量要求が使われている。
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
           [rationale] VehicleModel では市街地と高速の燃費要求が分離されている。
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
           [rationale] VehicleModel ではエンジンとトランスミッションの間に EngineToTransmissionInterface が定義されている。
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
  doc /* 軽量とは質量閾値なのか、それとも加速性能の代用なのか。
         燃費は市街地と高速の文脈に分割すべきか。
         確実な駆動力供給はインタフェース要求を意味するのか、性能要求を意味するのか、それとも両方か。 */
}

package Assumptions {
  doc /* Assumption A1: 軽量は質量を指す可能性が高い。
         Assumption A2: 燃費が良いとは市街地/高速燃費を指す可能性が高い。
         Assumption A3: 駆動力伝達は名前付きインタフェースを指す可能性が高い。 */
}

package TraceWeaknesses {
  doc /* この入力は意図的に曖昧にしてある。
         不足している定量スロットが受理されるまでは、レビューオーバーレイを正とすべきである。 */
}

package ReviewGuide {
  doc /* [review-action] accept / modify / reject / defer
         不足している定量スロットがすべて解決するまで、いかなるドラフトも canonical へ昇格させてはならない。 */
}

}
