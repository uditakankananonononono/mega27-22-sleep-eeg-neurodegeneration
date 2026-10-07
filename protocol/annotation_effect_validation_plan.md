# Annotation support versus EEG effect: prospective engineering plan

Status: proposed and frozen design only, not executed. No clinical endpoint.

## Question

Do the two already identified annotation-supported N2-to-N3 cells remain fully supported after a fixed, outcome-blind signal-quality screen? This is a selected two-recording engineering check. The cells were selected because support was observed; they are not a representative cohort, independent holdout, physiologic discovery or benchmark.

## Inputs and prerequisites

Subjects 10 and 40, first night, from the same Sleep-EDF version. Resolve exact PSG filenames from the source listing and verify operator checksums before reading. Use only EEG Fpz-Cz, verify the physical unit is microvolts and sampling is 100 Hz, and require a complete aligned 30-second grid. No alternative channel, night or subject may be substituted after seeing outputs. If linkage/unit/grid validation fails, record the obstacle without fitting an effect.

## Frozen screen

Reuse the pilot's intentionally crude engineering guard, not a clinical artifact classifier: every sample finite and per-epoch peak-to-peak range greater than zero and below 1,000 microvolts. Failed epochs become UNKNOWN in the stage vector. Do not tune this screen after seeing retained support. It does not establish absence of eye, muscle, electrode or reference artifacts. Artifact-resistant EEG interpretation would require a separate validated QC protocol.

## Outputs

Report counts and identities of failed epochs; retained events, exact control pools and capacity deficits; full-assignment indices under the unchanged matching contract. Preserve the pre-QC annotation indices and explain every changed assignment. If any event is removed, explicitly label the new retained-event population. Require the same 60-epoch bins, radius 10 and minimum three events. No p-values, cognitive labels or disease comparison.

Only if full support survives may a descriptive N2-to-N3 delta-band MAD difference be reported with the original Welch bandpower implementation, without uncertainty or inferential significance. That value is a selected-cell method demonstration, not evidence of a population EEG effect. Record the exact code revision, software versions and source hashes. A missing estimate stays missing, never zero. Selection of a supported cell prevents an unbiased claim about effect prevalence.

## Stop and interpretation rules

A failed hash/unit/linkage check stops that record. QC-induced support failure is an informative engineering boundary. Surviving support certifies only the selected inputs and contract, not causality, clinical validity or artifact-free physiology. No threshold relaxation, new channel search or favorable effect selection. Further signal-level study needs a separately frozen design and an eligible sample, not repeated selected demonstrations.
