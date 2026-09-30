"""One-recording, delta-only matched-control feasibility pilot.

No clinical labels or inferential statistics. Parameters frozen in round-3
contract before this run. Whole-record start is time-bin origin, not lights-off.
"""
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np
import pyedflib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dreaming22.features import epoch_bandpower
from dreaming22.matched_controls import matched_transition_control
from sleep_edfx_pilot import stages_from_annotations

def run(psg,hyp):
    with pyedflib.EdfReader(str(psg)) as reader:
        idx=reader.getSignalLabels().index('EEG Fpz-Cz')
        unit=reader.getPhysicalDimension(idx).strip()
        if unit not in ('uV','µV'): raise ValueError('Unexpected units')
        fs=reader.getSampleFrequency(idx); x=reader.readSignal(idx)
        duration=reader.getFileDuration()
    n=int(fs*30); epochs=int(duration//30)
    if fs*30 != n or len(x)<n*epochs: raise ValueError('Bad epoch grid')
    with pyedflib.EdfReader(str(hyp)) as h:
        stages=stages_from_annotations(*h.readAnnotations(),epochs)
    powers=[]
    for i in range(epochs):
        epoch=x[i*n:(i+1)*n]
        if not np.isfinite(epoch).all() or not 0<np.ptp(epoch)<1000:
            stages[i]='UNKNOWN';powers.append(0.);continue
        delta=epoch_bandpower(epoch,fs)['delta']
        if not np.isfinite(delta) or delta<=0:
            stages[i]='UNKNOWN';powers.append(0.)
        else:powers.append(float(np.log(delta)))
    result=matched_transition_control(powers,stages,bin_epochs=60,context_radius=10,min_events=3)
    return dict(source='Sleep-EDF Expanded v1.0.0',recording=psg.name,
                band='delta',bin_epochs=60,context_radius=10,min_events=3,
                time_origin='recording start, not lights-off',result=result,
                source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (psg,hyp)},
                limitations='One recording; crude QC; temporal dependence; no clinical labels, interval or p-value. No pair chosen by effect.')

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--psg',type=Path,required=True);a.add_argument('--hyp',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    args=a.parse_args();result=run(args.psg,args.hyp);args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
