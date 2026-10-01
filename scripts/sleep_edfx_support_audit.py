"""Reproduce stage-only support audit on checksum-verified pilot files."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
import pyedflib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dreaming22.support_audit import audit_common_support
from sleep_edfx_pilot import stages_from_annotations
HASHES={'SC4001E0-PSG.edf':'2b40a18adf76af69a42d6db1f30f31d26b369f6d27ca0050ef30147ef892b131',
        'SC4001EC-Hypnogram.edf':'a4cf67694ade1b52a0ddd06d5817fd45d2d3e8bac5302f640f3e9cfbbf12a996'}
def run(psg,hyp):
    for p in (psg,hyp):
        if p.name not in HASHES or hashlib.sha256(p.read_bytes()).hexdigest()!=HASHES[p.name]:
            raise ValueError('Requires verified original pilot bytes')
    with pyedflib.EdfReader(str(psg)) as r:
        idx=r.getSignalLabels().index('EEG Fpz-Cz')
        if r.getPhysicalDimension(idx).strip() not in ('uV','µV'):raise ValueError('Unexpected unit')
        fs=r.getSampleFrequency(idx);x=r.readSignal(idx);epochs=int(r.getFileDuration()//30)
    n=int(fs*30)
    if fs*30!=n or len(x)<n*epochs:raise ValueError('Invalid epoch grid')
    with pyedflib.EdfReader(str(hyp)) as r:s=stages_from_annotations(*r.readAnnotations(),epochs)
    for i in range(epochs):
        e=x[i*n:(i+1)*n]
        if not np.isfinite(e).all() or not 0<np.ptp(e)<1000:s[i]='UNKNOWN'
    return audit_common_support(s,bin_epochs=60,context_radius=10)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--psg',type=Path,required=True);a.add_argument('--hyp',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    v=a.parse_args();v.out.write_text(json.dumps(run(v.psg,v.hyp),indent=2)+'\n')
