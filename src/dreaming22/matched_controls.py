"""Descriptive, outcome-blind within-recording matched controls.

No permutation p-value: whole-night shifts do not establish exchangeability.
Exact common support is required; unmatched pairs produce missing estimates.
"""
import numpy as np
from .features import STAGES, stage_transitions
from .transition_instability import robust_mad


def matched_transition_control(log_power, stages, *, bin_epochs=60,
                               context_radius=10, min_events=3):
    """Match adjacent changes without replacement on labels and night time.

    Index i denotes the boundary between epochs i-1 and i. Match starting
    stage, fixed time bin, and exact surrounding-stage histogram. Exclude the
    central pair from that histogram to avoid requiring stable windows to have
    a transition's central labels. This changes the estimand to context-matched
    transitions on observed common support, not equal central stage pairs.
    Matching uses labels/time only, never power or observed effect direction.
    Nonoverlapping event/control pairs avoid sharing individual EEG epochs;
    temporal autocorrelation still remains and is not claimed removed.
    """
    for value, lower in ((bin_epochs,1),(context_radius,1),(min_events,3)):
        if type(value) is not int or value < lower:
            raise ValueError('Invalid matching/support parameter')
    stage_transitions(stages)
    x=np.asarray(log_power,dtype=float)
    if x.ndim != 1 or len(x) != len(stages) or not np.isfinite(x).all():
        raise ValueError('Finite aligned log-power vector required')
    names=tuple(sorted(STAGES))
    def key(i):
        # Strict full context; no padding across edges or UNKNOWN gaps.
        lo=i-1-context_radius; hi=i+1+context_radius
        if lo<0 or hi>len(stages): return None
        surrounding=list(stages[lo:i-1])+list(stages[i+1:hi])
        if any(s not in STAGES for s in surrounding): return None
        return (stages[i-1],i//bin_epochs,tuple(surrounding.count(s) for s in names))
    events={}; stable=[]
    for i in range(1,len(stages)):
        if stages[i-1] not in STAGES or stages[i] not in STAGES: continue
        k=key(i)
        if k is None: continue
        if stages[i-1]==stages[i]: stable.append((i,k))
        else: events.setdefault(f'{stages[i-1]}>{stages[i]}',[]).append((i,k))
    results={}
    for pair,items in sorted(events.items()):
        # Freeze thinning chronologically, not by largest signal change.
        thinned=[]; used_event_epochs=set()
        for i,k in items:
            if {i-1,i}&used_event_epochs: continue
            thinned.append((i,k)); used_event_epochs.update((i-1,i))
        available=[(i,k) for i,k in stable if not {i-1,i}&used_event_epochs]
        matches=[]; used_control_epochs=set()
        for i,k in thinned:
            candidates=[j for j,q in available if q==k and not {j-1,j}&used_control_epochs]
            if not candidates: continue
            # Nearest time, then earliest index. No EEG-dependent selection.
            j=min(candidates,key=lambda j:(abs(j-i),j))
            matches.append((i,j)); used_control_epochs.update((j-1,j))
        # Do not drop unmatched events and silently claim complete matching.
        complete=len(matches)==len(thinned) and len(matches)>=min_events
        d=None
        if complete:
            transition=[x[i]-x[i-1] for i,j in matches]
            control=[x[j]-x[j-1] for i,j in matches]
            d=robust_mad(transition)-robust_mad(control)
        results[pair]={'eligible_events':len(items),'nonoverlapping_events':len(thinned),
                       'matched_events':len(matches),'complete_support':complete,
                       'mad_difference':d,'indices':matches}
    ds=[r['mad_difference'] for r in results.values() if r['mad_difference'] is not None]
    return {'pairs':results,'recording_median_difference':float(np.median(ds)) if ds else None,
            'eligible_pairs':len(ds),'inference':'descriptive only; no exchangeable null established'}


def equal_recording_summary(recording_results):
    """Median of recording medians, not pooled (recording,pair) cells.

    For repeated nights this is not an independent-participant estimate; group
    by verified participant before inference. This function gives no interval.
    """
    values=[r['recording_median_difference'] for r in recording_results
            if r['recording_median_difference'] is not None]
    if not values: return None
    if not np.isfinite(values).all(): raise ValueError('Nonfinite recording result')
    return float(np.median(values))
