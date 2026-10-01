"""Annotation-only support audit, no EEG/QC/effects or participant inference."""
import argparse,hashlib,json,sys
from pathlib import Path
import pyedflib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dreaming22.support_audit import audit_common_support
from sleep_edfx_pilot import stages_from_annotations
HASHES={'SC4001EC-Hypnogram.edf':'a4cf67694ade1b52a0ddd06d5817fd45d2d3e8bac5302f640f3e9cfbbf12a996',
        'SC4002EC-Hypnogram.edf':'76e8457a67eaaaa62c7f6cc6e098fbe1c0a9c3fa02fa90ea01460aa481d71e82'}
def run(path):
    if path.name not in HASHES or hashlib.sha256(path.read_bytes()).hexdigest()!=HASHES[path.name]:
        raise ValueError('Unverified annotation source')
    with pyedflib.EdfReader(str(path)) as h:o,d,l=h.readAnnotations()
    epochs=int(max(float(a)+float(b) for a,b in zip(o,d))//30)
    stages=stages_from_annotations(o,d,l,epochs)
    return dict(recording=path.name,scope='ANNOTATION ONLY: no raw EEG QC, no effect estimate, not an independent participant; annotation end used for grid',epochs=epochs,result=audit_common_support(stages))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--hyp',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    v=a.parse_args();v.out.write_text(json.dumps(run(v.hyp),indent=2)+'\n')
