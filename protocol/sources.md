- PhysioNet Challenge 2026, official, https://moody-challenge.physionet.org/2026/ : PSG with future ICD-coded impairment, training cohorts and hidden other-site validation/test, challenge conditions. High for page-described design, no dataset use established.
- Human Sleep Project 3.0, official, https://bdsp.io/content/hsp/3.0/ : multi-center PSG, EHR linkage, credentialed data agreement and training requirement. High.
- BDSP access guide, official, https://bdsp.io/about/howto_accessdata/ : credentialing via AWS account and CITI training. High.
- NSRR data security, official, https://sleepdata.org/about/data-security : cost-free reviewed dataset-specific request, DAUA. High.
- MrOS NSRR, official, https://sleepdata.org/datasets/mros : two sleep study cycles in older men; confirm paired future cognitive outcomes. Medium for fit.
- SHHS NSRR, official, https://sleepdata.org/datasets/shhs : two PSG cycles, public description CVD outcome; cognition linkage not verified. Low fit.
- BDSP sleep EEG brain age/dementia, official, https://bdsp.io/content/v83ha57g3u22jz0eznrf/1.0.0/ : credentialed derived BAI/cognitive table, not raw PSG in release; needs verify linking with HSP. High.
- BDSP dementia detection, official, https://bdsp.io/content/vbredhzkdixefl465gzg/1.0.0/ : credentialed derived data/research; raw EEG linkage not established. Medium.
- Sleep-EDF Expanded, official, https://www.physionet.org/content/sleep-edfx/1.0.0/ : open ODC Attribution PSG+manual stages, no neurodegeneration diagnosis on page. High for staging pretraining only.
- NACC, official, https://www.naccdata.org/about-nacc-data/longitudinal-neurocognitive-and-clinical-phenotype-data : longitudinal cognition but paired PSG absent from description. High for cognition only.

## Search exclusions and access nuance (2026-09-26)

- PhysioNet's small Challenge training set is also listed on Kaggle: https://www.kaggle.com/datasets/physionet/physionetchallenge2026data . This is a distribution mirror, not an independent source, and its page confirms three training hospitals with distinct hidden evaluation sites. Access/download and terms must still be checked; do not imply it can be used as an independent validation dataset.
- RESILIENT Zenodo, https://zenodo.org/records/16755408 , has baseline and six-month cognitive assessments plus sleep-mat/watch streams but **no scalp sleep EEG** in its listed files. Reject for an EEG-derived biomarker even though cognition is longitudinal.
- PEARL-Neuro, https://www.nature.com/articles/s41597-024-03106-5 , has non-invasive high-density **wake** EEG in generally healthy adults with risk genotypes and cognitive tasks, **not sleep PSG** or neurodegenerative disease follow-up. Reject as independent sleep-EEG validation.
- NACC cognitive trajectories alone cannot be independently joined to PSG without an approved, demonstrated participant linkage; never infer one from cohort names.
- MrOS longitudinal BAI publication, https://pmc.ncbi.nlm.nih.gov/articles/PMC11714716/ : a published analysis confirms baseline PSG in 2003-05 and incident cognitive impairment followed until 2016, with 2,609 eligible men and 416 events per its reported cohort. This validates scientific *feasibility* in the parent cohort; it does not prove that the required participant-linked outcome table and raw PSG are both in the freely requestable NSRR package. It is prior art, so BAI alone is not a novel biomarker discovery.
