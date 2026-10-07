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
