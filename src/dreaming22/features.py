"""Outcome-blind elementary sleep-EEG features; not a diagnostic model.

Input is one participant/recording, one preprocessed EEG derivation in microvolts.
Do not use this module as an EDF reader, artifact cleaner, or network estimator.
"""
from __future__ import annotations

from collections import Counter
import numpy as np
from scipy.signal import welch

STAGES = frozenset({"W", "N1", "N2", "N3", "REM"})
BANDS = {"delta": (0.5, 4.0), "theta": (4.0, 8.0),
         "alpha": (8.0, 12.0), "sigma": (12.0, 16.0), "beta": (16.0, 30.0)}


def stage_transitions(stages: list[str]) -> dict[str, int]:
    """Counts adjacent recorded epochs, excluding UNKNOWN and stage gaps.

    Consumers must not collapse intervening invalid epochs before calling this.
    """
    bad = STAGES | {"UNKNOWN"}
    if any(stage not in bad for stage in stages):
        raise ValueError("Stage outside W/N1/N2/N3/REM/UNKNOWN")
    return dict(Counter(f"{a}>{b}" for a, b in zip(stages, stages[1:])
                        if a in STAGES and b in STAGES and a != b))


def epoch_bandpower(signal_uv: np.ndarray, sfreq: float) -> dict[str, float]:
    """Welch PSD integrated over named Hz bands, units microvolts squared.

    Returns NaN for a band above Nyquist. Caller must exclude bad signal first.
    """
    x = np.asarray(signal_uv, dtype=float)
    if x.ndim != 1 or x.size < 2 or not np.isfinite(x).all():
        raise ValueError("Finite one-dimensional epoch with >=2 samples required")
    if not np.isfinite(sfreq) or sfreq <= 0:
        raise ValueError("Positive finite sampling rate required")
    freqs, psd = welch(x, fs=sfreq, nperseg=min(x.size, max(2, int(sfreq * 4))))
    out = {}
    for name, (lo, hi) in BANDS.items():
        if hi > sfreq / 2:
            out[name] = float("nan")
            continue
        # Include edges only once in the trapezoidal integration. Near a
        # boundary, bin resolution may be coarse; log sampling rate and epoch.
        select = (freqs >= lo) & (freqs <= hi)
        out[name] = float(np.trapezoid(psd[select], freqs[select])) if select.sum() >= 2 else float("nan")
    return out


def recording_stage_bandpower(signal_uv: np.ndarray, sfreq: float,
                              stages: list[str], epoch_seconds: float = 30.) -> dict[str, dict[str, float]]:
    """Median per-stage bandpower, omitting UNKNOWN; no label or cohort access.

    Reject partial epochs and noninteger samples/epoch to avoid silent shift.
    """
    samples = sfreq * epoch_seconds
    if not np.isfinite(samples) or samples < 2 or not float(samples).is_integer():
        raise ValueError("Epoch length must resolve to an integer >=2 samples")
    x = np.asarray(signal_uv, dtype=float)
    n = int(samples)
    if x.ndim != 1 or x.size != n * len(stages):
        raise ValueError("Sample count must exactly match stage epoch count")
    stage_transitions(stages)  # Validate all labels.
    collected: dict[str, list[dict[str, float]]] = {stage: [] for stage in STAGES}
    for i, stage in enumerate(stages):
        if stage != "UNKNOWN":
            collected[stage].append(epoch_bandpower(x[i*n:(i+1)*n], sfreq))
    return {stage: {band: float(np.nanmedian([row[band] for row in rows]))
                    for band in BANDS}
            for stage, rows in collected.items() if rows}


def transition_context_bandpower(signal_uv: np.ndarray, sfreq: float,
                                 stages: list[str], source: str = "N2",
                                 target: str = "REM", epoch_seconds: float = 30.,
                                 min_events: int = 3) -> dict[str, float] | None:
    """Exploratory within-recording transition-conditioned signature.

    For each adjacent source->target transition, compare target-epoch power to
    the immediately preceding source epoch; report median log(target/source)
    across enough independent transitions. This is outcome-blind engineering,
    not a validated novel biomarker. Connectivity or cause is NOT inferred.
    """
    if source not in STAGES or target not in STAGES or source == target:
        raise ValueError("Source/target must be different known stages")
    if min_events < 1:
        raise ValueError("At least one event required")
    samples = sfreq * epoch_seconds
    if not np.isfinite(samples) or samples < 2 or not float(samples).is_integer():
        raise ValueError("Epoch length must resolve to integer >=2 samples")
    x = np.asarray(signal_uv, dtype=float)
    n = int(samples)
    if x.ndim != 1 or x.size != n * len(stages):
        raise ValueError("Signal/stages misaligned")
    stage_transitions(stages)
    pairs = [(i-1, i) for i in range(1, len(stages))
             if stages[i-1] == source and stages[i] == target]
    if len(pairs) < min_events:
        return None
    changes = {band: [] for band in BANDS}
    for before, after in pairs:
        base = epoch_bandpower(x[before*n:(before+1)*n], sfreq)
        follow = epoch_bandpower(x[after*n:(after+1)*n], sfreq)
        for band in BANDS:
            if np.isfinite(base[band]) and np.isfinite(follow[band]) and base[band] > 0 and follow[band] > 0:
                changes[band].append(float(np.log(follow[band]/base[band])))
    return {band: float(np.median(values)) if len(values) >= min_events else float("nan")
            for band, values in changes.items()}
