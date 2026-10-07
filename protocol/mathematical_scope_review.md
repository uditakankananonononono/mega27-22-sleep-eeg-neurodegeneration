# Mathematical scope review, October 7, 2026

The implemented bound applies only after the frozen chronological event thinning. Every retained event belongs to one exact key stratum. Let D_k be retained event demand and C_k the maximum disjoint control count within stratum k after excluding event epochs. Any globally feasible assignment uses at most C_k controls from that stratum. Therefore unmatched events in k are at least max(0,D_k-C_k), and summing those terms yields a valid global unmatched lower bound. Cross-stratum control overlaps can reduce attainable matching further; they cannot invalidate this lower bound.

For equal-length adjacent-epoch intervals, earliest-finish scheduling attains maximum cardinality within a stratum. An exchange argument replaces the first chosen interval of any optimal schedule with the earliest-finishing available interval without excluding more future intervals. Repeat on the remaining intervals. This is standard interval scheduling, not a new optimization theorem. The synthetic exhaustive oracle checks selected finite implementations, not a proof for malformed inputs or arbitrary generalized intervals.

Important scope limits:

- This is conditional feasibility of the retained-event design. Another event-thinning rule changes demand and exclusions; the bound is not a theorem covering all possible study designs.
- Insufficient support in finite records is not proof of structural population nonpositivity, no biological effect, or impossibility in every future recording.
- The histogram includes stages after the event. Those labels may reflect the transition itself; matching them is not automatically valid causal confound adjustment. No causal identification is claimed.
- No weighting, coarsening or dropping unmatched events is introduced here. Each changes the comparison or target population and would need its own explicit protocol.
- Two feasible cells do not establish signal QC, representative samples or an unbiased physiologic contrast.
- Fixed time bins use different source annotation origins. Rates should not be pooled as cross-source physiology without origin reconciliation.

## Explicit failure of the converse

A synthetic sequence N3,N2,N3,N3,N3,N3,N2,N3,N2,N3, with radius 1 and bin size 30, retains two N3->N2 events. Each of their exact context strata has one disjoint-control capacity, so the summed deficit is zero. The strata's candidate controls share an epoch, and exhaustive global enumeration matches at most one of the two events. This is a counterexample to interpreting zero deficit as global feasibility, not a real-data or minimum-three-event result. A dedicated regression checks the zero bound and the exact maximum. The study's census thresholds remain unchanged.
