# Source and endpoint recheck, September 30, 2026

Official source: https://moody-challenge.physionet.org/2026/

The official competition phase concluded August 24, 2026. Do not describe hidden-test evaluation as a currently available route without new confirmation from organizers. No team registration or entry was submitted by this project. Training links remain listed. Official sizes are 214 GiB (small) and 1.2 TiB (large); these are not download authorizations.

Metadata linkage is explicitly BidsFolder + SessionID, with source and BDSPPatientID. Positive labels are future clinically coded cognitive impairment, not confirmed Alzheimer pathology. The endpoint requires qualifying codes separated by at least a week, at least one year after PSG and one no more than six years afterward. Negative labels need documented follow-up. These details require source-code verification before a definitive day-threshold implementation or outcome reconstruction. Date shifts preserve within-person differences but do not support cross-patient calendar comparisons. No metadata has been downloaded or examined.

The supplementary examples from two hidden sites lack outcomes. They can test file/montage compatibility, not external biological replication. A held-out training hospital is a useful domain check but does not automatically meet the independent-cohort gate. Small and large versions overlap in origin and are not two independent datasets.

## License/access

HSP v3.0 official license: https://bdsp.io/content/hsp/view-license/3.0/
Access guide: https://bdsp.io/about/howto_accessdata/
HSP resource: https://bdsp.io/content/hsp/3.0/
Kaggle training mirror: https://www.kaggle.com/datasets/physionet/physionetchallenge2026data

Official HSP License 1.5.0 prohibits sharing restricted-data access, prohibits commercial use, requires current research-subject/HIPAA certification, and requires publication-associated code to be accessible to the research community. HSP requires credentialing and DUA; the guide adds registered AWS account and CITI training. The Kaggle page displays older-looking license text without the official no-commercial-use clause. Do not assume equivalent terms or bypass credentialing because an archive is linked. Kaggle fetch displayed a GetCurrentUser rate-limit message; no further access attempt made this run.

Open gap: verify the user's current qualifications, approved access, applicable training-mirror terms and secure permitted execution environment before acquiring participant data. No license accepted, DUA signed, restricted data acquired, form submitted, or author contact made.

## Engineering repair

outcome_contract.py validates an explicit caller-supplied elapsed-day contract, not hard-coded approximations of source year rules. It rejects insufficient-follow-up negatives, ambiguous booleans, impossible dates, missing identifiers and duplicate baseline PSG links. Nine synthetic tests added; 34 total pass. It does not validate ICD code multiplicity, credentials, montage, cross-source identity overlap, biological claims, or clinical prediction. It is not a counted ChatGPT novelty round.
