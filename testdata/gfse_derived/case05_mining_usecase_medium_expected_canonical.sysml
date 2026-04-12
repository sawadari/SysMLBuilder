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
      doc /* Main Flow:
             1. Identify an asteroid target.
             2. Activate the mining laser.
             3. Extract ore and store it in the cargo hold.
             4. Suspend mining when the cargo hold becomes full.
             Exception Flows:
             - If the mining laser fails, halt mining and alert the pilot.
             - If the target asteroid is depleted, reacquire a target. */
    }
  }

  use case def OffloadOreAndResupply {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    actor station : DomainDefinitions::Station;
    objective {
      doc /* Main Flow:
             1. Establish a docking connection with a station.
             2. Transfer ore to the station.
             3. Resupply essential systems.
             Exception Flows:
             - If docking fails, notify the pilot and abort the offload sequence.
             - If cargo transfer fails, suspend operations and keep the ore on board. */
    }
  }
}

package Requirements {
  requirement operationalObjectives {
    subject miningFrigate : DomainDefinitions::MiningFrigate;
    doc /* Derived from operational use case objectives. Quantitative completion thresholds are intentionally left unresolved. */
  }
}

package ViewTargets {
  doc /* render target: UseCases::MineAsteroids as textual objective view
         render target: UseCases::OffloadOreAndResupply as textual objective view */
}

}
