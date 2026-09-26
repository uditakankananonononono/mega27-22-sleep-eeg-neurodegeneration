"""Fail-closed participant grouping and external-site split audits.

The caller provides a de-identified subject key scoped by source. No random
recording-level split is allowed. The source/site can be a hospital or study,
not the user-controlled file path. This module does not read disease labels.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Record:
    recording_id: str
    source_id: str
    person_id: str
    visit_id: str

    def __post_init__(self):
        for field in ("recording_id", "source_id", "person_id", "visit_id"):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Missing {field}; cannot certify split")

    @property
    def person_key(self):
        return (self.source_id, self.person_id)


def audit_partitions(train: list[Record], val: list[Record], test: list[Record],
                     require_external_test: bool = False) -> dict[str, int]:
    """Reject duplicate recording IDs, person overlap and optional site overlap.

    Shared identifiers across institutions are not globally matchable: verify
    cross-source identity linkage or exclusion separately. Refuse train-only
    or empty partitions rather than reporting spurious test success.
    """
    partitions = (train, val, test)
    if not all(partitions):
        raise ValueError("All train/validation/test partitions must be nonempty")
    for label, records in zip(("train", "validation", "test"), partitions):
        if any(not isinstance(record, Record) for record in records):
            raise ValueError(f"Malformed {label} record")
    ids = [row.recording_id for part in partitions for row in part]
    if len(ids) != len(set(ids)):
        raise ValueError("Repeated recording ID across or within partitions")
    people = [{row.person_key for row in part} for part in partitions]
    if any(people[i] & people[j] for i, j in ((0, 1), (0, 2), (1, 2))):
        raise ValueError("A participant appears in multiple partitions")
    sources = [{row.source_id for row in part} for part in partitions]
    if require_external_test and (sources[0] | sources[1]) & sources[2]:
        raise ValueError("External test source overlaps training/validation")
    return {label: len(records) for label, records in zip(("train", "validation", "test"), partitions)}
