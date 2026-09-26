# Biomarker claim ladder (no rung yet passed)

**Measurement**: non-invasive overnight EEG signal, recorded with an explicit montage, reference, stage and QC protocol. Spectral/entropy/REM/transition features are candidates; connectivity only when enough simultaneous comparable channels exist. These are measurements, not neurodegeneration diagnoses.

**Association**: frozen feature contrasts with age-adjusted, sex/OSA/medication/site-aware sensitivity analyses when covariates are available. Report missing covariates explicitly; age matching or age-conditioned testing does not erase confounding. Stratify by stage and compare REM-specific versus NREM and whole-night effects. Do not infer a direction before seeing data.

**Prediction**: baseline EEG precedes future decline; source defines diagnosis or cognitive-score trajectory; negative subjects require appropriate follow-up; evaluate age-only, sleep architecture, clinical covariate and feature-added models without tuning on the test set. Avoid selection and immortal-time biases.

**Generalization**: truly independent site/source with compatible outcome and acquisition, person-level deduplication, frozen feature and preprocessing, no cross-source individual overlap or leakage. A hidden site's aggregate score is helpful but does not replace inspectable validation of the claimed biological signature. If validation fails, report a dataset-specific association, not a biomarker.

**Clinical utility**: a candidate sleep-derived association is not an approved diagnostic test. Independent prospective replication, calibration and subgroup equity, reproducibility across recording devices and clinical adjudication would be needed before any screening claim. No individual diagnosis or medical recommendation.

Evidence tally as of 2026-09-26: 0 verified participant datasets acquired; 0 models fit; 0 biomarker associations tested; 0 external replications.
