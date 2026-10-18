// Original instructional fixture: two actors compete for one available slot.
// Current observes permission before commit; Rechecked checks again at commit.
// Neither module models an actual repository implementation.
module checkThenAct {
  const RECHECK: bool
  pure val ACTORS = Set(1, 2)
  type Phase = Idle | Ready | Done
  var phase: int -> Phase
  var available: int
  var holders: Set[int]

  action init = all {
    phase' = ACTORS.mapBy(_ => Idle),
    available' = 1,
    holders' = Set(),
  }

  action observe(actor: int): bool = all {
    phase.get(actor) == Idle,
    available > 0,
    phase' = phase.set(actor, Ready),
    available' = available,
    holders' = holders,
  }

  action commit(actor: int): bool = all {
    phase.get(actor) == Ready,
    (not(RECHECK) or available > 0),
    phase' = phase.set(actor, Done),
    available' = available - 1,
    holders' = holders.union(Set(actor)),
  }

  // Environment idling intentionally admits stuttering. This safety fixture
  // does not demonstrate deadlock detection or liveness.
  action idle = all {
    phase' = phase,
    available' = available,
    holders' = holders,
  }

  action step = {
    nondet actor = ACTORS.oneOf()
    any { observe(actor), commit(actor), idle }
  }

  val safety = available >= 0 and holders.size() <= 1
  val bothObserved = ACTORS.forall(actor => phase.get(actor) == Ready)
  val committed = holders.size() == 1
}

module Current {
  import checkThenAct(RECHECK = false).*
}

module Rechecked {
  import checkThenAct(RECHECK = true).*
}

module checkThenActTest {
  import checkThenAct(RECHECK = false).*
  run staleCheckTest = init
    .then(observe(1)).then(observe(2))
    .then(commit(1)).then(commit(2))
    .expect(not(safety))
}

module recheckedTest {
  import checkThenAct(RECHECK = true).*
  run oneCommitTest = init
    .then(observe(1)).then(observe(2))
    .then(commit(1))
    .expect(safety and committed and available == 0)
}
