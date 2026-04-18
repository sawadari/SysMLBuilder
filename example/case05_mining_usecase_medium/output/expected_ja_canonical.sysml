package Case05MiningUseCaseMediumExpected {

package DomainDefinitions {
  part def MiningFrigate;
  part def PilotPod;
  part def AsteroidBelt;
  part def Station;
}

package UseCases {

  use case def MineAsteroids {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    actor pilotPod : DomainDefinitions::PilotPod;
    actor asteroidBelt : DomainDefinitions::AsteroidBelt;
    objective {
      doc /* メインフロー:
             1. 小惑星ターゲットを特定する。
             2. 採掘レーザーを起動する。
             3. 鉱石を採取し貨物倉へ格納する。
             4. 貨物倉が満杯になったら採掘を中断する。
             例外フロー:
             - 採掘レーザーが故障した場合、採掘を停止してパイロットへ通知する。
             - 対象小惑星が枯渇した場合、ターゲットを再取得する。 */
    }
  }

  use case def OffloadOreAndResupply {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    actor station : DomainDefinitions::Station;
    objective {
      doc /* メインフロー:
             1. ステーションとのドッキング接続を確立する。
             2. 鉱石をステーションへ移送する。
             3. 重要システムを補給する。
             例外フロー:
             - ドッキングに失敗した場合、パイロットへ通知して荷下ろし手順を中止する。
             - 貨物移送に失敗した場合、運用を中断して鉱石を船内に保持する。 */
    }
  }
}

package Requirements {
  requirement operationalObjectives {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* 運用ユースケースの目的から導出した。定量的な完了閾値は意図的に未解決のままとしている。 */
  }
}

package ViewDefinitions {
  private import Views::*;
  private import DS_Views::*;

  view mineAsteroidsObjectiveView : DS_Views::SymbolicViews::gv {
    expose UseCases::MineAsteroids;
  }

  view offloadOreAndResupplyObjectiveView : DS_Views::SymbolicViews::gv {
    expose UseCases::OffloadOreAndResupply;
  }
}

}

package Case05MiningUseCaseMediumExpectedStandardViews {
    private import DS_Views::*;

    // Replace RequirementsTreeView with RequirementTreeView if your Cameo build requires the singular form.
    view 'Requirements View' : DS_Views::SymbolicViewsByExpression::RequirementsTreeView {
        expose Case05MiningUseCaseMediumExpected::**;
    }

    view 'Structural Context View' : DS_Views::SymbolicViewsByExpression::PartsTreeView {
        expose Case05MiningUseCaseMediumExpected::**;
    }

    view 'Internal Structure View' : DS_Views::SymbolicViewsByExpression::'Parts&PortsNestedView' {
        expose Case05MiningUseCaseMediumExpected::**;
    }

    view 'Behavior Activity View' : DS_Views::SymbolicViewsByExpression::ActionsNestedView {
        expose Case05MiningUseCaseMediumExpected::**;
    }

    view 'Behavior State View' : DS_Views::SymbolicViewsByExpression::StatesNestedView {
        expose Case05MiningUseCaseMediumExpected::**;
    }
}
