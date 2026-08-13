# Topology-aware root-cause localization

Three deterministic fault scenarios exercise different hierarchy levels:
`access-07`, `aggregation-03`, and `core-02`. An affected set contains the root
and all of its downstream descendants. Seeded observation noise removes some
downstream alarms and adds zero, one, or two false alarms by scenario.

Every node is ranked as a possible cause. The score combines the fraction of
observed alarms explained by its downstream impact, precision of the predicted
impact set, and a small bonus when the candidate itself is observed. This is a
transparent heuristic, not a trained model.

The true root is ranked first in all three included cases. The evaluation is
deliberately small and synthetic; future work should add simultaneous faults,
time ordering, recovery behavior, and larger randomized scenario sets.
