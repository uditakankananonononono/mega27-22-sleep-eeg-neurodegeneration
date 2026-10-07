# When exact sleep-transition controls lack support

Working manuscript, October 7, 2026. Not a finished paper. No clinical biomarker claim.

## Abstract

Exact controls can improve comparability while making a proposed sleep-EEG comparison unmeasurable. We audited an outcome-blind, frozen matching contract using open sleep-stage annotations. Controls had to share starting stage, a fixed 60-epoch time bin and the exact surrounding-stage histogram at radius 10, with no shared central epochs and complete matching. A disjoint-control capacity bound established impossibility without examining EEG effects. Across 153 Sleep-EDF cassette recordings from 78 participants, 1,415 of 1,417 cells with at least three events had capacity deficits. Two first-night N2-to-N3 cells admitted full stage-only assignments; neither retained support on the paired second night. All 77 eligible cells in 16 healthy CAP recordings also had deficits under conservative annotation parsing. These findings establish a feasibility boundary of this particular estimand, not an absence of transition physiology. They do not test cognition, neurodegeneration or signal-derived biomarkers. Annotation conventions, time-grid origin and missingness limit cross-source comparability.

## Research question and scope

Can the frozen exact transition-control comparison obtain full stage-only support on openly accessible sleep annotations? The original program sought prospective neurodegenerative signatures from sleep EEG. Compatible open clinical outcome data were not verified, and privileged access was excluded. The deliverable explicitly pivoted to sleep-physiology/identifiability. Neurodegeneration remains untested motivation only. No deficit is counted as a disease discovery, benchmark win or positive biomarker result.

## Methods

The boundary index denotes epochs i-1 and i. Transitions are grouped by directed source/target stage. Events are thinned chronologically to avoid sharing central epochs within a stage-pair analysis. Controls are stable adjacent epochs with the same starting stage, time bin and surrounding histogram, excluding the central pair from that histogram. The context must be complete and contain only recognized stages. Controls cannot use any retained event epoch. The original matching rule selects the closest available control chronologically, with earliest index breaking ties. It requires every retained event to be matched and at least three events before returning an EEG statistic. Temporal autocorrelation is not claimed removed.

For each exact stratum, let demand be the number of retained events and capacity the maximum number of pairwise-disjoint adjacent control intervals in that stratum. Equal-length intervals are optimally scheduled by taking the earliest available boundary and skipping overlapping boundaries. The positive part of demand minus capacity gives unavoidable unmatched events in that stratum. Summing these deficits remains a lower bound on global unmatched events. Controls across different strata can overlap, so adequate stratum capacity does not establish a global assignment. A positive deficit does prove that complete matching is impossible under this fixed contract. The proof concerns the selected chronologically thinned events, not every conceivable alternative event-selection design.

The bound was tested against exhaustive global control-subset enumeration on 712 small synthetic sequences under three fixed configurations, yielding 3,093 pair comparisons. This checks implementation on finite cases; it is not a general formal verification or real EEG experiment.

Sleep-EDF cassette coverage includes every participant's earliest available night, plus all available second nights. Selection and parameters were frozen before expanded outputs, but the first ten participants and one second night had previously been inspected. Thus the expansion is descriptive, not a clean confirmatory holdout. Metadata and annotation bytes were verified against operator hashes. R&K stages 3/4 map to N3; movement/unknown and incomplete epochs are UNKNOWN. No raw PSG was read in the expanded census. Ages span 25-101. Repeated nights are not independent people.

CAP coverage includes healthy records n1-n16, frozen before support outputs. Explicit header columns allow optional Position and alternate Duration spelling. Only full epochs contained within explicit stage-duration intervals receive labels. Gaps are not carried forward. This differs from the operator Matlab reader and leaves 125 unknown epochs. Epoch zero is the first stage annotation, not a verified raw recording or lights-off time. CAP is an independent repository/source, not proof of cross-source participant independence.

## Results

| Source/subset | Recordings | Cells with >=3 events | Proven deficits | Fully assigned cells checked |
|---|---:|---:|---:|---:|
| Sleep-EDF earliest available nights | 78 | 707 | 705 | 2 |
| Sleep-EDF second nights | 77 | 726 | 726 | 0 |
| Healthy CAP | 16 | 77 | 77 | 0 |

The earliest-available subset includes two participants whose first nights were unavailable. Consequently, adding its 78 rows to the 77 second-night rows would duplicate those two recordings. The all-recordings total must instead include 76 true first nights and 77 second nights, totaling 153 unique recordings. Reconciliation by unique filename yields 1,417 eligible cells and 1,415 deficits. The initial pooled 1,433/1,431 counts double-counted the two shared files and are withdrawn.

Two first-night N2-to-N3 cells, subjects 10 and 40, admit complete assignments of six and three events. Archived boundary indices demonstrate feasible stage-only control selection. A zero placeholder vector was used only to exercise the matching routine; no resulting signal statistic is retained or interpreted. Both participants have second nights without a support-feasible >=3-event cell. The conservative audit cannot conclude that EEG features fail to repeat, only that this same exact matched comparison cannot be evaluated on both nights.

## Relation to existing work

Lack of common support is an established statistical problem, not a newly discovered principle. The reviewed overlap-weighting literature explains that restricting or reweighting the available comparison population can change the estimand [4]. That causal treatment framework does not establish causality for sleep transitions. Our before/after context contains post-transition labels, so treating its histogram as a causal adjustment set would require additional justification. We make no such claim.

Sleep-transition physiology and brain dynamics also have substantial prior art. Whole-brain transition work [5], slow-wave synchronization models [6] and proof-of-principle attractor-state analyses [7] already address these subjects. Our annotation audit measures none of their signal-level mechanisms. Its narrow contribution is the documented empirical support boundary of this exact frozen contract, together with an outcome-blind implementation and reproducible records. Priority over equivalent support audits has not been established.

## Stage-pair support breakdown

Machine-generated tables in `verified_tables.md` reconcile filenames before aggregation and check the reported totals against archived outputs. Among 129 unique-recording N2-to-N3 cells with at least three retained events, 127 have deficits and two admit complete stage-only assignments. The opposite N3-to-N2 direction has 129 eligible cells, all with deficits. N1-to-N2 has 151 eligible cells, all deficient; N2-to-REM has 138, all deficient. These are cell-level feasibility counts, not estimates of transition frequency, participant prevalence, direction-specific EEG power or biological asymmetry. Cells within a recording and repeated nights within a person are dependent.

The tables also report retained event counts and summed unmatched lower bounds. Those totals describe the frozen thinning/control design, not independent trials. They are not used to compute significance or confidence intervals. A direction having more unsupported cells need not have a stronger physiologic disruption; event availability, context composition and stable-control scarcity all contribute. Reported support is conditional on the stage grid and source-specific annotation handling.

## Interpretation

The frozen comparison is supported rarely, not universally impossible. Replacing greedy matching alone cannot overcome a positive capacity deficit. The failure concerns exact context/time controls and full matching, not a general inability to study transitions. A different estimand could be evaluated in a separately frozen study, but changing it after these outputs would not rescue or confirm the original test. No causal or neurodegenerative mechanism is inferred.

## Limits and work remaining

Annotations rather than EEG effects drive the expanded results. Missing stage intervals, recording-origin differences and scoring conventions affect support. The study does not establish optimal matching for arbitrary contexts, clinical independence, cognitive outcomes, age-adjusted disease contrasts, signal QC or independent biomarker validation. Unique-recording reconciliation corrected an initial double-count; subset totals must not be summed without deduplication. A preliminary literature and internal mathematical scope review are archived. A complete paper still needs fuller priority screening, independent mathematical review, verified figures, and format inspection. This working source does not satisfy the 50-page text-body floor.

## Primary sources and reproducibility

Sleep-EDF: https://www.physionet.org/content/sleep-edfx/1.0.0/ . CAP: https://physionet.org/content/capslpdb/1.0.0/ . CAP reader: https://physionet.org/files/capslpdb/1.0.0/ScoringReader.m?download . Frozen manifests, complete stratum outputs, checksums and reproduction scripts are in the repository. The engineering suite has 57 passing tests; that number is software evidence only.


## Reviewed references

[4] Overlap, matching, or entropy weights: what are we weighting for? https://arxiv.org/html/2210.12968 . Supports the established common-support and estimand distinction, not our sleep findings.

[5] Discovery of key whole-brain transitions and dynamics during human wakefulness and non-REM sleep. https://www.nature.com/articles/s41467-019-08934-3 . Prior sleep-transition dynamics work.

[6] Slow wave synchronization and sleep state transitions. https://www.nature.com/articles/s41598-022-11513-0 . Prior slow-wave/state-transition physiology.

[7] Dynamics of sleep: Exploring critical transitions and early warning signals. https://pubmed.ncbi.nlm.nih.gov/32304989/ . Prior proof-of-principle attractor-state work, not clinical early-neurodegeneration validation.
