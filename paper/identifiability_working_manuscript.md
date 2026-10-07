# When exact sleep-transition controls lack support

Working manuscript, October 7, 2026. Not a finished paper. No clinical biomarker claim.

## Abstract

Exact controls can improve comparability while making a proposed sleep-EEG comparison unmeasurable. We audited an signal-outcome-blind, frozen matching contract using open sleep-stage annotations. Controls had to share starting stage, a fixed 60-epoch time bin and the exact surrounding-stage histogram at radius 10, with no shared central epochs and complete matching. A disjoint-control capacity bound established impossibility of full matching of the chronologically retained events under this contract, without examining EEG effects. Across 153 Sleep-EDF cassette recordings from 78 participants, 1,415 of 1,417 cells with at least three events had capacity deficits. Two first-night N2-to-N3 cells admitted full stage-only assignments; neither retained support on the paired second night. All 77 eligible cells in 16 healthy CAP recordings also had deficits under conservative annotation parsing. These findings establish a feasibility boundary of this particular estimand, not an absence of transition physiology. They do not test cognition, neurodegeneration or signal-derived biomarkers. Annotation conventions, time-grid origin and missingness limit cross-source comparability.

## Research question and scope

Can the frozen exact transition-control comparison obtain full stage-only support on openly accessible sleep annotations? The original program sought prospective neurodegenerative signatures from sleep EEG. Compatible open clinical outcome data were not verified, and privileged access was excluded. The deliverable explicitly pivoted to sleep-physiology/identifiability. Neurodegeneration remains untested motivation only. No deficit is counted as a disease discovery, benchmark win or positive biomarker result.

## Methods

The audit is signal-outcome-blind, not independent of EEG provenance: stage labels were scored from the source recordings. Signal amplitudes, observed power effects and cognitive labels are not used in expanded support selection.

The boundary index denotes epochs i-1 and i. Transitions are grouped by directed source/target stage. For each directed stage pair separately, eligible event boundaries are traversed in increasing index order. Keep the earliest boundary; keep each later boundary only if neither of its epochs is already used by a retained event. Drop an overlapping later event without replacement. This deterministic thinning depends on stage/time eligibility, not signal magnitude. Controls are stable adjacent epochs with the same starting stage, time bin and surrounding histogram, excluding the central pair from that histogram. The context must be complete and contain only recognized stages. Let U be the union of both epochs {i-1,i} of every retained event in that directed-pair analysis. Exclude every candidate control boundary j if {j-1,j} intersects U. This excludes overlap with all retained events, not merely the event it might match. Controls assigned to different events within the same directed stage-pair analysis must also be pairwise nonoverlapping, so no two selected control intervals share an EEG epoch. This clause is enforced by `used_control_epochs` in `src/dreaming22/matched_controls.py`; `src/dreaming22/support_audit.py` bounds disjoint controls within strata. Surrounding context windows need not be disjoint: only central two-epoch event/control intervals obey these exclusions. Context windows may overlap each other or other central intervals. No across-stage-pair disjointness is asserted. The original matching rule selects the closest available control chronologically, with earliest index breaking ties. It requires every retained event to be matched and at least three events before returning an EEG statistic. Temporal autocorrelation is not claimed removed.

For each exact stratum, let demand be the number of retained events and capacity the maximum number of pairwise-disjoint adjacent control intervals in that stratum. Equal-length intervals are optimally scheduled by taking the earliest available boundary and skipping overlapping boundaries. The positive part of demand minus capacity gives unavoidable unmatched events in that stratum. Summing these deficits remains a lower bound on global unmatched events. Controls across different strata can overlap, so adequate stratum capacity does not establish a global assignment. A positive deficit does prove that complete matching is impossible under this fixed contract. The proof concerns the selected chronologically thinned events, not every conceivable alternative event-selection design.

The bound was tested against exhaustive global control-subset enumeration on 712 small synthetic sequences under three fixed configurations, yielding 3,093 pair comparisons. This checks implementation on finite cases; it is not a general formal verification or real EEG experiment.

Sleep-EDF cassette coverage includes every participant's earliest available night, plus all available second nights. Selection and parameters were frozen before expanded outputs, but the first ten participants and one second night had previously been inspected. Thus the expansion is descriptive, not a clean confirmatory holdout. Metadata and annotation bytes were verified against operator hashes. R&K stages 3/4 map to N3; movement/unknown and incomplete epochs are UNKNOWN. No raw PSG was read in the expanded census. Ages span 25-101. Repeated nights are not independent people.

CAP coverage includes healthy records n1-n16, frozen before support outputs. Explicit header columns allow optional Position and alternate Duration spelling. Only full epochs contained within explicit stage-duration intervals receive labels. Gaps are not carried forward. This differs from the operator Matlab reader and leaves 125 unknown epochs. Epoch zero is the first stage annotation, not a verified raw recording or lights-off time. CAP is an independent repository/source, not proof of cross-source participant independence.

## Results

The 1,415/1,417 denominator consists of eligible recording-by-directed-stage-pair cells with at least three chronologically retained events under this contract. It is not a percentage of all sleep transitions, epochs or people.

| Source/subset | Recordings | Cells with >=3 events | Proven deficits | Fully assigned cells checked |
|---|---:|---:|---:|---:|
| Sleep-EDF earliest available nights | 78 | 707 | 705 | 2 |
| Sleep-EDF second nights | 77 | 726 | 726 | 0 |
| Healthy CAP | 16 | 77 | 77 | 0 |

The CAP 77/77 result is conditional on the conservative parser: 125 partial, missing or unscored epochs remain UNKNOWN, with no gap carry-forward. Its grid starts at the first stage event, not verified recording/lights-off onset. This is annotation feasibility under that parser, not raw EEG QC.

The earliest-available subset includes two participants whose first nights were unavailable. Consequently, adding its 78 rows to the 77 second-night rows would duplicate those two recordings. The all-recordings total must instead include 76 true first nights and 77 second nights, totaling 153 unique recordings. Reconciliation by unique filename yields 1,417 eligible cells and 1,415 deficits. The initial pooled 1,433/1,431 counts double-counted the two shared files and are withdrawn.

Two first-night N2-to-N3 cells, subjects 10 and 40, admit complete assignments of six and three events. Archived boundary indices demonstrate feasible stage-only control selection. A zero placeholder vector was used only to exercise the matching routine; no resulting signal statistic is retained or interpreted. Both participants have second nights without a support-feasible >=3-event cell. The conservative audit cannot conclude that EEG features fail to repeat, only that this same exact matched comparison cannot be evaluated on both nights.

## Relation to existing work

Lack of common support is an established statistical problem, not a newly discovered principle. The reviewed overlap-weighting literature explains that restricting or reweighting the available comparison population can change the estimand [4]. That causal treatment framework does not establish causality for sleep transitions. Our before/after context contains post-transition labels, so treating its histogram as a causal adjustment set would require additional justification. We make no such claim.

Sleep-transition physiology and brain dynamics also have substantial prior art. Whole-brain transition work [5], slow-wave synchronization models [6] and proof-of-principle attractor-state analyses [7] already address these subjects. Our annotation audit measures none of their signal-level mechanisms. Its narrow contribution is the documented empirical support boundary of this exact frozen contract, together with an signal-outcome-blind implementation and reproducible records. Priority over equivalent support audits has not been established.

## Stage-pair support breakdown

Machine-generated tables in `verified_tables.md` reconcile filenames before aggregation and check the reported totals against archived outputs. Among 129 unique-recording N2-to-N3 cells with at least three retained events, 127 have deficits and two admit complete stage-only assignments. The opposite N3-to-N2 direction has 129 eligible cells, all with deficits. N1-to-N2 has 151 eligible cells, all deficient; N2-to-REM has 138, all deficient. These are cell-level feasibility counts, not estimates of transition frequency, participant prevalence, direction-specific EEG power or biological asymmetry. Cells within a recording and repeated nights within a person are dependent.

The tables also report retained event counts and summed unmatched lower bounds. Those totals describe the frozen thinning/control design, not independent trials. They are not used to compute significance or confidence intervals. A direction having more unsupported cells need not have a stronger physiologic disruption; event availability, context composition and stable-control scarcity all contribute. Reported support is conditional on the stage grid and source-specific annotation handling.

## Why capacity fails

The audit distinguishes absent exact control pools from competition for disjoint controls. Across eligible unique cassette cells, 15,489 of 18,989 retained events have no exact control pool. The disjoint-capacity lower bound rises to 15,799 unmatched events, an additional 310 beyond empty-pool failures. Healthy CAP has 375 empty-pool events among 445 retained events and a bound of 378 unmatched, three more than the empty-pool count. These sums are descriptive accounting for retained directed-pair events, not independent observations or a causal decomposition. Cross-stratum overlap could force still more unmatched events.

Thus control absence is the main counted source of infeasibility under this contract; enforcing nonoverlap introduces additional deficits. This does not show which individual exact-key component causes scarcity. Testing weaker keys after seeing these outputs would be a new design, not validation of the failed one. A capacity defect is distinct from an algorithmic failure: no search procedure can supply a control that is absent from the eligible pool.

## Interpretation

The frozen comparison is supported rarely, not universally impossible. Replacing greedy matching alone cannot overcome a positive capacity deficit. The failure concerns exact context/time controls and full matching, not a general inability to study transitions. A different estimand could be evaluated in a separately frozen study, but changing it after these outputs would not rescue or confirm the original test. No causal or neurodegenerative mechanism is inferred.

## Limits and work remaining

Annotations rather than EEG effects drive the expanded results. Missing stage intervals, recording-origin differences and scoring conventions affect support. The study does not establish optimal matching for arbitrary contexts, clinical independence, cognitive outcomes, age-adjusted disease contrasts, signal QC or independent biomarker validation. Unique-recording reconciliation corrected an initial double-count; subset totals must not be summed without deduplication. A preliminary literature and internal mathematical scope review are archived. A complete paper still needs fuller priority screening, independent mathematical review, verified figures, and format inspection. This working source does not satisfy the 50-page text-body floor.

## Primary sources and reproducibility

Sleep-EDF: https://www.physionet.org/content/sleep-edfx/1.0.0/ . CAP: https://physionet.org/content/capslpdb/1.0.0/ . CAP reader: https://physionet.org/files/capslpdb/1.0.0/ScoringReader.m?download . Frozen manifests, complete stratum outputs, checksums and reproduction scripts are in the repository. The engineering suite has 59 passing tests; that number is software evidence only.


## Reviewed references

[4] Overlap, matching, or entropy weights: what are we weighting for? https://arxiv.org/html/2210.12968 . Supports the established common-support and estimand distinction, not our sleep findings.

[5] Discovery of key whole-brain transitions and dynamics during human wakefulness and non-REM sleep. https://www.nature.com/articles/s41467-019-08934-3 . Prior sleep-transition dynamics work.

[6] Slow wave synchronization and sleep state transitions. https://www.nature.com/articles/s41598-022-11513-0 . Prior slow-wave/state-transition physiology.

[7] Dynamics of sleep: Exploring critical transitions and early warning signals. https://pubmed.ncbi.nlm.nih.gov/32304989/ . Prior proof-of-principle attractor-state work, not clinical early-neurodegeneration validation.

## Reporting and reproducibility safeguards

Each result remains tied to a frozen manifest, filename and source hash. The complete stratum output is retained rather than only summary deficits, allowing readers to see event demand, raw control counts and disjoint capacity. The absence of a returned statistic is explicitly missing, not zero. Neither an empty comparison nor a zero placeholder is evidence against transition physiology. The two assignment-feasible cells are disclosed to avoid turning broad failure into a universal impossibility claim.

Identity reconciliation occurs before summing overlapping recording subsets. A regression rejects inconsistent duplicates, and archived expected totals check 153 unique cassette files rather than 155 subset rows. Repeated-night pairs are linked by source-specific participant metadata. Cross-source participant independence is not inferred from different repository names. These safeguards improve the reliability of this analysis but do not certify every possible future use of the scripts.

The initial dependency instructions were incomplete: the full suite imports pyedflib and annotation reproduction uses xlrd. A new Python 3.10 environment installed pinned numpy, scipy, pyedflib and xlrd versions, passed dependency checks and the then-current suite, and reproduced the original ten-subject output byte-for-byte. An intermediate 57-test revision passed in that isolated environment; the current 59-test revision was rerun there after adding the zero-bound counterexample and key-occupancy test, with no broken requirements reported. Direct dependency pins are not a cryptographic artifact lock, and other Python/platform combinations remain untested.

## What a future study would need

A broader sleep-physiology experiment would need a separately declared comparison that is support-feasible without using EEG outcome values to select it. It would need comparable signal units, montage, filtering, epoch origin, stage scoring, artifact exclusion and source-specific covariates. Signal-derived features would need their own uncertainty and repeated-night assessment. Merely weakening the exact key until more events match would not establish that the resulting comparison answers the original question or has less bias.

Returning to the neurodegenerative question would additionally require eligible participant-level baseline EEG linked to a valid future cognitive endpoint, a frozen elapsed-time contract, a fair comparator and a genuinely independent clinical cohort. None is supplied by the present annotation support audit. The present study can inform whether a proposed design is measurable; it cannot close those clinical evidence gaps. Its practical value is to prevent unsupported estimates from being presented as successful biomarkers, not to promise a diagnostic result.

## Capacity bound: assumptions and argument

Fix one recording and one directed stage pair. Let E be the chronologically retained event boundaries. Remove from the candidate stable-boundary set every interval sharing an epoch with E. This exclusion is applied before counting capacity: a stable pair cannot supply a control if it uses an event epoch, even when its key otherwise matches. Partition the remaining controls and the retained events by the exact key consisting of starting stage, time bin and context histogram. An event has precisely one key. A control can be assigned only to events with its own key.

For stratum k, let D_k denote the event count. Write each control boundary j as an interval using epochs j-1 and j. Let C_k be the greatest number of mutually nonoverlapping controls from that stratum. Any full or partial assignment under the contract uses mutually disjoint controls and assigns at most one control per event. Consequently it can match at most min(D_k,C_k) events in k. The number unmatched in k is at least D_k-min(D_k,C_k), equal to max(0,D_k-C_k). Summing across the disjoint event strata establishes the reported lower bound. This remains valid even when controls in different strata overlap, because allowing such overlaps while computing separate capacities can only enlarge available capacity relative to a global assignment.

The converse fails. Separate strata can each have enough controls yet demand incompatible intervals. Our implementation therefore reports capacity-not-disproven rather than globally feasible when the sum is zero. For the two actual census cells with zero bound, archived complete assignments separately establish feasibility under the selected design. No blanket converse theorem is inferred from those two examples.

Within one stratum, earliest-boundary scheduling maximizes the number of disjoint two-epoch intervals. Boundaries are sorted and duplicates removed. After selecting boundary j, any boundary j+1 is rejected because it shares epoch j; j+2 is eligible. Consider an optimal selection whose first boundary is later than the earliest available boundary. Replacing that first selection with the earliest one cannot move the finishing epoch later and cannot exclude an interval that previously followed it. Thus there is an optimal selection beginning with the greedy first choice. Applying the same argument recursively establishes maximum cardinality. This elementary equal-length interval argument is not claimed as new theory.

## Computation and limits of implementation evidence

The support audit reads stage labels rather than power values. Context keys are constructed from fixed-radius stage windows; no power threshold, observed effect direction or cognitive label contributes to key selection. Capacity is computed by sorting each eligible stratum's control boundaries and selecting nonoverlapping intervals. The current implementation nevertheless scans stable controls separately for every directed pair, and the production matching routine scans candidate lists for each event. The study has not benchmarked runtime scaling or memory use on very large collections. It should not be described as an optimized general matching solver.

The exhaustive test enumerates all control subsets only for small synthetic sequences. Enumeration has exponential cost in the number of candidates, so it is a reference check rather than an intended full-night algorithm. Its 3,093 comparisons verify that the computed lower bound never exceeds the oracle's exact unmatched count on the tested cases. They do not establish a numerical confidence level, guarantee correctness for every input, or independently validate the clinical meaning of the contract. The analytical argument and finite test evidence answer different questions and are reported separately.

## Feasibility is not an effect estimate

A support-feasible cell supplies legal event/control indices, but does not supply artifact-free signals, matching clinical covariates or a meaningful spectral contrast. Before a signal-level analysis, the actual EEG epochs would need compatible physical units, sampling, reference montage and artifact handling. Exclusions applied after signal QC can remove events or controls and destroy annotation-only support. Therefore the two feasible annotation cells are upper-level opportunities for checking the design, not guaranteed analyzable EEG effects.

Conversely, a cell with a positive annotation capacity deficit cannot acquire full support merely by excluding additional unusable control epochs while keeping the same event demand. Signal QC can also remove events, which changes the retained-event comparison. Such a reduced comparison must be reported with its exclusions and population meaning rather than silently treated as the original full-support analysis. No signal-level result is supplied by this manuscript's expanded annotation census.


## Predeclared signal-check design

A proposed two-recording engineering check is archived in `protocol/annotation_effect_validation_plan.md`. It has not run. It would use only the two previously identified support-feasible first nights, verify source hashes and channel/grid metadata, apply the existing crude fixed epoch guard, then rerun the identical support contract. The output would distinguish event removal, control removal, altered assignments and a genuinely missing estimate. Choosing these cells because they were supported makes the experiment selected by feasibility; it cannot estimate how often EEG effects occur in a population. The pilot's peak-to-peak guard is not a validated artifact detector. A surviving descriptive value would therefore remain a method demonstration, without inferential significance or clinical interpretation.

A small explicit counterexample illustrates the bound's one-sided interpretation. The synthetic sequence N3,N2,N3,N3,N3,N3,N2,N3,N2,N3, with context radius 1 and a single 30-epoch bin, has two retained N3-to-N2 events and zero summed stratum deficit. Yet the two strata's control opportunities overlap, and exhaustive enumeration admits only one match. A regression preserves this example. It is below the real study's three-event reporting floor and uses different synthetic test parameters; it does not alter the census contract or add a physiologic result.


## Exact-key sparsity baseline

The reviewer-requested diagnostic was added after the census, so it is descriptive and not a new confirmatory hypothesis. A radius-10 context has 20 surrounding epochs and five stage categories. Stars-and-bars gives 10,626 nonnegative histograms summing to 20, or 53,130 possible starting-stage/histogram keys per time bin. These are theoretical possibilities, not uniformly likely states. Sleep labels are serially dependent, and many combinations are not occupied. Dividing available controls by the theoretical key-space size would not estimate the probability of a match.

A checksum-gated occupancy script therefore measures actual event-conditional candidate pools after the same event thinning and event-epoch exclusion. Before exact histogram matching, same-starting-stage/time-bin pools contain a median of 11 controls per cassette event (range 0-58), representing a median of seven distinct observed histograms (maximum 31). CAP has medians of 14 controls and ten observed histograms, with maxima 58 and 24. These are event-weighted summaries, not independent bins or participants.

Removing only the histogram requirement reduces empty-pool accounting from 15,489 to 2,616 of 18,989 cassette events, and from 375 to 45 of 445 CAP events. Thus exact context contributes substantial observed scarcity beyond starting-stage/time-bin scarcity. The relaxed pool is a diagnostic only: it does not establish disjoint assignment, comparable physiological context, a valid alternative effect estimand or less bias. No matching threshold was relaxed in the reported primary census.

The very low cell-level full-support rate is consequently unsurprising under this highly restrictive design. The finding should be framed as a quantitative design-feasibility warning, not a surprising new physiological phenomenon. The empty-pool event proportions are not 98 percent: they are 15,489/18,989 for cassette and 375/445 for CAP; near-total failure concerns full-support cells. The key-space calculation explains risk of sparsity, while the observed-pool baseline documents its magnitude in these selected sources.
