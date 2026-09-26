# DREAMING 22: sleep EEG and early neurodegenerative signatures

Status, 2026-09-26: protocol/engineering scaffold only. No participant PSG/outcome data acquired, no model fit, no measured biomarker, and no independent validation. Not a diagnostic device or Alzheimer's classifier.

Goal: discover a non-invasive sleep-EEG-derived *candidate biomarker* for early neurodegeneration and test whether it generalizes across genuinely independent datasets. A candidate is not a clinically validated biomarker, early-disease diagnosis, causal mechanism, or confirmed Alzheimer-specific signal. Question: Which stage-specific changes in sleep-brain dynamics associate with current cognitive impairment or future decline, beyond age and sleep/clinical confounders? Start with spectral power, complexity, sleep-stage transitions, and a REM-focused hypothesis. Connectivity and cross-frequency coupling are conditional on sufficient comparable EEG electrodes, viable signal quality, and predeclared methods. A two-lead PSG is not a high-density brain network.

Data leads and access: see protocol/sources.md. Source page descriptions do not prove a linked, usable participant-level dataset. No clinical claim is licensed by a cohort title. Only de-identified data and approved terms may be used.

## Non-negotiable analysis gates

1. Record dataset version, license/DAUA, subject and visit keys, EEG/staging channels, outcome definition, and time gap. Clinical code-derived diagnosis is not biomarker-confirmed preclinical disease.
2. Freeze exclusion, signal filters, stage harmonization, one-person-one-fold splits, covariates, comparators, endpoints, and external validation source *before* any labels are examined.
3. QC units, reference montage, sampling, saturation, motion and stage annotation; keep processing blind to outcomes. Do not compute network connectivity from a single lead or incomparable channel pairs.
4. Fit age-only/clinical and stage-specific feature baselines on training subjects only. All imputation/standardization/hyperparameter choices stay inside train folds. No recordings of the same person across train and test. For the longitudinal target, PSG precedes outcome by the prespecified interval.
5. Freeze a feature/signature definition before external testing. Report effect size/direction, age- and confound-adjusted associations, uncertainty, stage specificity, and individual-level reproducibility. A high classifier AUC alone is not a biological biomarker.
6. Independent-site/source validation must retain the direction and useful magnitude, with calibration, subgroup, missingness and negative results reported. An internal split or challenge submission without accessible independent-source results cannot pass this gate.
7. Call it a *candidate non-invasive biomarker* only if the independent data and prespecified evidence gates pass; never call it clinically validated or suitable for screening without prospective replication and appropriate clinical testing.

## Engineering prototype

`src/dreaming22/features.py` accepts a uniformly sampled, pre-QC'd EEG array in microvolts and stage labels per fixed epoch, computes Welch bandpower and stage transitions. It does not do EDF ingestion, clinical outcome linkage, age adjustment, connectivity, or validation. These remain open tasks. Run `python3 -m unittest discover -s tests` with numpy and scipy installed.
