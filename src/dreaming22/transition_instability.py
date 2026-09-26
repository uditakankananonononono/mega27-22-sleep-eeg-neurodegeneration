"""Outcome-blind staged EEG transition variability analysis.

Experimental method, not a cognitive biomarker. Define each stage-pair type in
advance and take per-type robust dispersion across repeated transitions. The
report exposes event counts: low support is missing, not zero. Null control
uses same-length adjacent stable-stage epoch pairs, avoiding label shuffles
that would destroy architecture but not necessarily spectral trajectories.
"""
from collections import defaultdict
import numpy as np
from .features import BANDS, STAGES, epoch_bandpower, stage_transitions


def robust_mad(values):
    x=np.asarray(values,dtype=float)
    if x.ndim!=1 or x.size<3 or not np.isfinite(x).all():
        return None
    return float(np.median(np.abs(x-np.median(x))))


def transition_instability(signal_uv, sfreq, stages, *, epoch_seconds=30., min_events=3):
    if min_events<3: raise ValueError('Minimum support is three independent transitions')
    nfloat=sfreq*epoch_seconds
    if not np.isfinite(nfloat) or nfloat<2 or not float(nfloat).is_integer():
        raise ValueError('Epoch grid invalid')
    n=int(nfloat); x=np.asarray(signal_uv,dtype=float)
    if x.ndim!=1 or len(x)!=n*len(stages): raise ValueError('EEG/stage grid mismatch')
    stage_transitions(stages)
    cache={}
    def power(i):
        if i not in cache: cache[i]=epoch_bandpower(x[i*n:(i+1)*n],sfreq)
        return cache[i]
    changes=defaultdict(lambda:defaultdict(list))
    stable=defaultdict(lambda:defaultdict(list))
    for i in range(1,len(stages)):
        a,b=stages[i-1],stages[i]
        if a not in STAGES or b not in STAGES: continue
        p,q=power(i-1),power(i)
        dest=stable[a] if a==b else changes[f'{a}>{b}']
        for band in BANDS:
            if all(np.isfinite(z) and z>0 for z in (p[band],q[band])):
                dest[band].append(float(np.log(q[band]/p[band])))
    def summary(data):
        return {kind:{band:{'events':len(v),'mad_log_change':robust_mad(v) if len(v)>=min_events else None}
                      for band,v in bands.items()}
                for kind,bands in sorted(data.items())}
    return {'transitions':summary(changes),'stable_stage_control':summary(stable),
            'minimum_events':min_events,'note':'Within-recording method feasibility only; no cognitive/disease label.'}
