"""Reproduce descriptive coverage and stage-only candidate assignments.

Rechecks annotation checksums. Zero-valued power is a placeholder only; no
signal-derived statistic is returned. No inference, disease or EEG QC claim.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
import pyedflib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dreaming22.matched_controls import matched_transition_control
from sleep_edfx_pilot import stages_from_annotations

def run(audit_path,data_dir):
    audit=json.loads(audit_path.read_text());rows=audit['records'];cells=[];candidates=[]
    for row in rows:
        pairs={k:p for k,p in row['audit']['pairs'].items() if p['events']>=3}
        cells.extend(pairs.values())
        if not row['capacity_not_disproven_pairs']:continue
        path=data_dir/row['file']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Annotation checksum mismatch')
        with pyedflib.EdfReader(str(path)) as h:ann=h.readAnnotations()
        stages=stages_from_annotations(*ann,row['annotation_epochs'])
        match=matched_transition_control(np.zeros(len(stages)),stages)
        for pair,p in pairs.items():
            if p['full_matching_impossible']:continue
            q=match['pairs'][pair]
            candidates.append(dict(subject=row['subject_id'],pair=pair,events=p['events'],matched_events=q['matched_events'],complete_support=q['complete_support'],indices=q['indices']))
    return dict(scope='Descriptive annotation-only census; zero placeholder power, no EEG effect or clinical inference.',participants=len(rows),age_min=min(r['metadata']['age'] for r in rows),age_max=max(r['metadata']['age'] for r in rows),event_floor_cells=len(cells),proven_deficit_cells=sum(p['full_matching_impossible'] for p in cells),assignment_candidates=candidates)
if __name__=='__main__':
    a=argparse.ArgumentParser()
    for name in ('audit','data-dir','out'):a.add_argument('--'+name,type=Path,required=True)
    v=a.parse_args();v.out.write_text(json.dumps(run(v.audit,v.data_dir),indent=2,allow_nan=False)+'\n')
