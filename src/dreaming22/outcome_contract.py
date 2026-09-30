"""Outcome-blind metadata gates for a prospective clinical-CI analysis.

This checks metadata, not EEG quality, license eligibility, or clinical truth.
A false label without documented follow-up is not a valid negative control.
"""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class ProspectiveMetadata:
    source: str
    person: str
    bids_folder: str
    session: str
    age: float
    event_days: float | None
    followup_days: float
    label: bool

    def validate(self, *, min_event_days: float, max_event_days: float,
                 min_negative_followup_days: float) -> None:
        """Thresholds must come from a frozen source-specific endpoint contract.

        Boundaries are in elapsed days, never guessed from shifted dates. A caller
        must explicitly choose how the source's year definition maps to days.
        """
        for value in (self.source, self.person, self.bids_folder, self.session):
            if not isinstance(value, str) or not value.strip():
                raise ValueError('Missing linkage identifier')
        for value in (min_event_days, max_event_days, min_negative_followup_days):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
                raise ValueError('Invalid endpoint threshold')
        if min_event_days > max_event_days:
            raise ValueError('Reversed endpoint interval')
        for value in (self.age, self.followup_days):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError('Invalid age or follow-up')
        if type(self.label) is not bool:
            raise ValueError('Label must be explicitly parsed; strings are not booleans')
        if self.label:
            t = self.event_days
            if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t):
                raise ValueError('Positive needs an observed event interval')
            if not min_event_days <= t <= max_event_days:
                raise ValueError('Positive event outside prospective interval')
            if t > self.followup_days:
                raise ValueError('Event after last follow-up')
        else:
            if self.event_days is not None:
                raise ValueError('Negative has conflicting event time')
            if self.followup_days < min_negative_followup_days:
                raise ValueError('Negative has insufficient follow-up')


def audit_linkage(rows: list[ProspectiveMetadata]) -> dict[str, int]:
    """Refuse duplicate visits/people for a baseline-only design.

    Source-local keys cannot prove cross-source patient independence. This gate
    requires a separate cross-source overlap policy before any external claim.
    """
    if not rows:
        raise ValueError('Empty metadata cohort')
    if any(not isinstance(r, ProspectiveMetadata) for r in rows):
        raise ValueError('Malformed metadata row')
    people = [(r.source, r.person) for r in rows]
    files = [(r.source, r.bids_folder, r.session) for r in rows]
    if len(set(people)) != len(people):
        raise ValueError('Multiple baseline rows for a participant')
    if len(set(files)) != len(files):
        raise ValueError('Multiple metadata rows for a PSG link')
    for r in rows:
        if any(not isinstance(x, str) or not x.strip() for x in (r.source,r.person,r.bids_folder,r.session)):
            raise ValueError('Missing linkage identifier')
    return {'participants': len(people), 'sources': len({r.source for r in rows})}
