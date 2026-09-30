# Round 3 matched negative-control contract

Date: September 30, 2026. Engineering method addition, not a disease finding.
Judge session: https://chatgpt.com/c/6abc7ad3-47b0-83ee-9203-752c684e281a

## Adopted

For one prespecified EEG band, create adjacent epoch log-power changes for every stage-pair type meeting support. Thin event pairs chronologically to avoid sharing epochs. For each stage-pair type, choose stable same-starting-stage pairs within the same fixed time bin and with exactly the same surrounding-stage count vector. Exclude central two epochs from that vector because a stable pair cannot have the same central labels as a transition. Require full context without unknown labels. Choose nearest control in time with index tie-break, without reuse within the stage-pair comparison. Matching never inspects EEG values. Require at least three matched nonoverlapping events and complete matching of the thinned eligible set; otherwise return missing.

D(r,p) = MAD(transition changes) - MAD(matched stable changes).
Recording statistic = median of supported D(r,p).
Descriptive cohort statistic = median of recording statistics, not a pooled recording/pair median. Repeated nights require verified participant grouping before inference. Controls may be reused between different stage-pair analyses; those analyses are dependent and not independent observations.

Defaults are 60 epochs per time bin (30 minutes only on a 30-second grid), context radius 10 epochs, support 3. The caller must freeze units, band, bin origin, epoch size, support, exclusions and cohort eligibility before real evaluation. A per-band output does not license selecting the most favorable band after inspection. Source-stage spectral differences remain inherent in transitions; the control estimates surrounding-context specificity, not a causal transition effect or central-stage equality.

## Not adopted

The judge contradicts itself between recording-level medians and pooled (recording,pair) cells. Use equal-recording medians only. No p-value or 95% interval is returned. Whole-night circular label shifts can change time-of-night/stage compatibility and do not prove exchangeability. Shuffling labels also disrupts the EEG-based scoring relation. Neither a displaced placebo nor a block permutation is automatically a valid null. An inferential extension needs a defensible model, participant-level sampling and a separate preregistration.

## Synthetic checks and limits

Eight new tests cover zero-change matched output, a known injected difference of 1 in log-power-change MAD, matching independent of power, time-bin restriction, unknown context, no common support, unique epochs within each matched comparison and equal-recording aggregation. These are unit tests, not a false-positive-rate study or physiology result. Temporal autocorrelation remains. No real-data matched result has been computed yet. Strict matching can make most pairs unavailable; report that missingness rather than relaxing criteria after inspecting effects. No cognition labels acquired, no biological insight demonstrated, no benchmark win and no independent clinical replication.
