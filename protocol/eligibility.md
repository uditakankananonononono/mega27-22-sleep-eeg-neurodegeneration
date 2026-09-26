# Source eligibility register

The unit is a real participant, not an EDF file, visit or PSG segment. Status is not an endorsement. Record source version and the actual permitted data-use agreement before downloading, linking or publishing.

| Candidate | EEG during sleep | Outcome | Timing | Access | Status |
|---|---|---|---|---|---|
| PhysioNet 2026 Challenge training | Described raw PSG and stages | Future ICD-coded cognitive impairment, MCI/AD/dementia pooled | 1-6 years post-PSG, per official rules | Training data linked from official page; exact access/terms to verify | Lead only; hidden sites' labels not available; cannot independently inspect signature replication |
| BDSP HSP v3.0 | Described raw multi-site PSG | EHR diagnoses across systems | Participant-specific cognitive outcome needs confirmation | Credentialed DUA, AWS account and CITI | Not acquired |
| NSRR MrOS | Two older-men PSG cycles | Published longitudinal incident CI analysis (2,609 men; 416 incident events), but individual-level outcome table in accessible package not verified | PSG 2003-05, follow-up to 2016 in paper; downloadable row-level linkage unverified | Cost-free reviewed per-dataset DAUA | Feasible in published parent cohort; eligibility/access unverified |
| NSRR SHHS | Two PSG cycles | Cardiovascular endpoints described | Cognitive endpoint linkage unverified | Cost-free reviewed per-dataset DAUA | Candidate; not eligible yet |
| Sleep-EDF Expanded | Open staged PSG | No suitable neurodegeneration endpoint | None | Open ODC Attribution 1.0 | Signal engineering only |
| RESILIENT | No scalp EEG in documented files | Baseline/six-month cognitive tests | Longitudinal | Zenodo CC BY 4.0 | Excluded (wrong modality) |
| PEARL-Neuro | Wake resting/task EEG, not sleep | Risk genotype/cognitive tests | Not disease trajectory | OpenNeuro via associated paper | Excluded (wrong modality) |

**MrOS catalog warning:** The NSRR Visit-2 `mhalzh` self-report ('doctor ever told you dementia or Alzheimer's') has 1,885 UNKNOWN of 2,911 records, only 17 YES, 1,008 NO and 1 missing; https://sleepdata.org/datasets/mros/variables/mhalzh . It cannot stand in for the published 416 incident composite endpoint. Need actual cognitive scores and follow-up/visit-to-PSG linkage before eligibility. Never replace UNKNOWN with NO.
