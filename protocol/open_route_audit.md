# Open sleep-EEG route audit, September 30, 2026

Open corpora permit method research now, but do not yet satisfy the requested prospective neurodegeneration endpoint. No modality or endpoint substitution is authorized by this audit.

## Sleep-EDF Expanded

https://www.physionet.org/content/sleep-edfx/1.0.0/

197 nights from two studies, not 197 independent datasets or necessarily 197 participants. Fpz-Cz and Pz-Oz EEG at 100 Hz; cassette aging subset described as 25-101 years, healthy Caucasian participants, repeated nights. Open ODC Attribution. Useful for outcome-blind extraction, event-support audit and repeated-night reproducibility. No appropriate cognition/conversion endpoint; low-density montage constrains connectivity and reference comparability. One recording analyzed so far.

## CAP Sleep Database

https://physionet.org/content/capslpdb/1.0.0/
https://physionet.org/content/capslpdb/view-license/1.0.0/

108 recordings with at least three EEG channels, staging and CAP annotations. Includes 16 healthy and 22 RBD recordings among other sleep disorders. Open ODC Attribution. Raw EEG not yet acquired in this audit.

Verified age workbook:
https://physionet.org/files/capslpdb/1.0.0/gender-age.xlsx?download
Official checksum:
https://physionet.org/files/capslpdb/1.0.0/SHA256SUMS.txt
SHA256: 9d7a4c54f352412e1b0a8793f6124d1aef7b318a13b027a2f88e497719654f36

RBD ages 58-82 (22 records); healthy ages 23-42 (16 records). Zero age overlap. RBD-vs-healthy prediction is not an age-adjustable clinical comparison without new data; regression cannot create support. Workbook contains spelling inconsistencies (RDB11 vs RBD11, SBD vs SDB), so linkage must use a reviewed alias map, not silent fuzzy matching. No longitudinal cognition or neurodegenerative conversion outcome verified. RBD diagnosis alone is not confirmed early neurodegeneration. Prefer extraction/negative-control portability only. CAP healthy controls cannot be used as matched controls for older RBD subjects.

## MASS

https://ceams-carsm.ca/mass/
https://borealisdata.ca/dataset.xhtml?persistentId=doi%3A10.5683%2FSP3%2F8ZEAWT

Although called open-access, official biosignal procedure requires an ethics-approved project and proof of ethical approval. SS1 has 53 participants aged 55-76, 15 MCI plus two borderline cases, with diagnosis available via restricted descriptors. Not an unrestricted clinical alternative; do not infer publicly displayed annotations authorize diagnosis access.

## Wake EEG

https://www.mdpi.com/2306-5729/8/6/95

The 88-person AD/FTD/control routine EEG dataset is eyes-closed resting-state, not staged sleep. It cannot validate sleep-transition features or prospective early disease. Excluded for this project's endpoint, regardless of open license.

## Decision

Proceed with open sleep EEG for extraction and reproducibility. Keep prospective clinical endpoint, independent outcome replication, biological insight and benchmark win open. Neither a disease-classifier pivot nor an RBD surrogate endpoint is silently substituted. Credential questions remain parked while seeking a genuinely open eligible cohort.
