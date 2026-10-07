# Isolated engineering reproduction, October 7, 2026

A new Python 3.10 virtual environment, without inherited site packages, installed the four exact direct dependency versions in `requirements-reproduce.txt`. `pip check` found no broken requirements. The 48-test suite passed in 0.124 seconds on source commit daa08fe8a9357c15235b7ec51c846346a2379f20. This includes the exhaustive synthetic matching-oracle regression, not a raw-data rerun or independent biological validation.

Reproduce from repository root:

```sh
python3 -m venv /tmp/dreaming22-env
/tmp/dreaming22-env/bin/python -m pip install -r requirements-reproduce.txt
/tmp/dreaming22-env/bin/python -m pip check
/tmp/dreaming22-env/bin/python -m unittest discover -s tests
```

These are direct version pins, not a platform-independent artifact lock or supply-chain checksum guarantee. Python/platform variants were not tested. The suite does not download data. Raw Sleep-EDF recordings and metadata remain outside the repository; archived raw/annotation outputs were not regenerated in this environment. Clinical cohort access and all biomarker, benchmark and independent clinical replication gates remain open.

## Annotation-only data reproduction

At source commit 78b34ba43661fdaae7b16d67e1357623cb045cb0, the isolated environment downloaded the ten frozen hypnograms plus operator checksums and metadata (104,717 bytes total). The script checked all annotation bytes against the operator SHA256 list and the metadata against its frozen hash. Reproducing `results/ten_subject_annotation_support.json` gave a byte-identical file, SHA256 `46a8bb2c046994d9b37d24f2957c7fc313df0d5f0f48d3eb09c06e0556098093`.

```sh
python scripts/batch_annotation_support.py \
  --manifest protocol/open_annotation_sample_manifest.json \
  --data-dir local_data --checksum local_data/SHA256SUMS.txt \
  --metadata local_data/SC-subjects.xls --out /tmp/reproduced.json
cmp /tmp/reproduced.json results/ten_subject_annotation_support.json
```

This reproduces the same selected young sample's annotation-only feasibility failure: all 88 cells with at least three events have capacity deficits. It is not a new cohort, EEG effect, disease test or independent scientific replication. No raw PSG was downloaded for this check. Sleep-EDF attribution and source: https://www.physionet.org/content/sleep-edfx/1.0.0/ . Exact annotation URLs are in the frozen manifest. Metadata: https://www.physionet.org/files/sleep-edfx/1.0.0/SC-subjects.xls?download . Checksums: https://www.physionet.org/files/sleep-edfx/1.0.0/SHA256SUMS.txt?download .
