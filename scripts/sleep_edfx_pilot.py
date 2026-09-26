"""Reproducible staged sleep-EEG *method pilot*, NOT cognitive-disease research.

Uses one openly licensed Sleep-EDF recording; never reads cognitive outcomes.
Stage annotation time is assigned per 30-s epoch midpoint. Excludes movement,
unknown and any epoch containing annotation boundary. Blind QC here is minimal
and intentionally does not certify a biomarker.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import pyedflib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dreaming22.features import epoch_bandpower, transition_context_bandpower, stage_transitions
from dreaming22.transition_instability import transition_instability

LABELS={'Sleep stage W':'W','Sleep stage 1':'N1','Sleep stage 2':'N2',
        'Sleep stage 3':'N3','Sleep stage 4':'N3','Sleep stage R':'REM'}

def stages_from_annotations(onsets,durations,descriptions,n_epochs,epoch_s=30):
    stages=[]
    for i in range(n_epochs):
        start=i*epoch_s; end=start+epoch_s
        matching=[LABELS.get(str(label),'UNKNOWN') for onset,duration,label in zip(onsets,durations,descriptions)
                  if float(onset)<=start and float(onset)+float(duration)>=end]
        stages.append(matching[0] if len(matching)==1 else 'UNKNOWN')
    return stages

def run(psg,hyp,subject):
    with pyedflib.EdfReader(str(psg)) as r:
        names=r.getSignalLabels()
        idx=names.index('EEG Fpz-Cz')
        fs=float(r.getSampleFrequency(idx)); length=int(r.getNSamples()[idx]); duration=float(r.getFileDuration())
        x=r.readSignal(idx)
    with pyedflib.EdfReader(str(hyp)) as h:
        onsets,durations,descriptions=h.readAnnotations()
    n_epochs=int(duration//30)
    if length < int(fs*30*n_epochs): raise ValueError('Signal shorter than stage grid')
    stages=stages_from_annotations(onsets,durations,descriptions,n_epochs)
    ns=int(fs*30)
    first=x[:ns*n_epochs].reshape((n_epochs,ns))
    # Conservative but crude per-epoch guards; calibrate signal QC before biological use.
    finite=np.isfinite(first).all(axis=1)
    dynamic=np.ptp(first,axis=1)
    keep=finite&(dynamic>0)&(dynamic<1000)
    cleaned=[stage if keep[i] else 'UNKNOWN' for i,stage in enumerate(stages)]
    transition=transition_context_bandpower(x[:ns*n_epochs],fs,cleaned,
                                           source='N2',target='REM',min_events=1)
    pairs=[i for i in range(1,len(cleaned)) if cleaned[i-1]=='N2' and cleaned[i]=='REM']
    # Also N2->N3 baseline for context (no disease labels).
    n3_pairs=[i for i in range(1,len(cleaned)) if cleaned[i-1]=='N2' and cleaned[i]=='N3']
    return {'source':'Sleep-EDF Expanded v1.0.0', 'recording_id':psg.name,
            'subject_key':subject,'sampling_hz':fs,'duration_sec':duration,
            'stage_counts':{s:cleaned.count(s) for s in ['W','N1','N2','N3','REM','UNKNOWN']},
            'n2_to_rem_event_count':len(pairs),'n2_to_n3_event_count':len(n3_pairs),
            'n2_to_rem_median_log_bandpower_change':transition,
            'stage_pair_transition_instability':transition_instability(x[:ns*n_epochs],fs,cleaned),
            'qc_dropped_epochs':int((~keep).sum()),
            'interpretation':'Engineering feasibility only; no cognitive outcomes, statistics or biomarker validation'}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--psg',type=Path,required=True);a.add_argument('--hyp',type=Path,required=True);a.add_argument('--subject',required=True);a.add_argument('--out',type=Path,required=True)
    args=a.parse_args()
    result=run(args.psg,args.hyp,args.subject)
    result['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [args.psg,args.hyp]}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
