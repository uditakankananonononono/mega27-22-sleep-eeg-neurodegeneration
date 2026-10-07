"""Reproduce a frozen annotation support sample from local verified files.

Does not download, inspect EEG effects or certify participant independence.
Operator SC-subjects metadata and filename specification resolve subject/night.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import pyedflib
import xlrd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dreaming22.support_audit import audit_common_support
from sleep_edfx_pilot import stages_from_annotations

def run(manifest_path,data_dir,checksum_path,metadata_path):
    if hashlib.sha256(metadata_path.read_bytes()).hexdigest()!='93d65494096d375ee302f1ce3a0506575b17a918b93d7cdaa5a2b32727366080':
        raise ValueError('Operator metadata hash mismatch')
    manifest=json.loads(manifest_path.read_text())
    hashes={l.split()[1]:l.split()[0] for l in checksum_path.read_text().splitlines() if len(l.split())==2}
    sheet=xlrd.open_workbook(str(metadata_path)).sheet_by_index(0)
    metadata={(int(sheet.cell_value(i,0)),int(sheet.cell_value(i,1))):dict(age=sheet.cell_value(i,2),sex_code=sheet.cell_value(i,3)) for i in range(1,sheet.nrows)}
    records=[];seen=set()
    for entry in manifest['files']:
        name=entry['file']
        if Path(name).name!=name or not name.startswith('SC4'):raise ValueError('Unexpected filename')
        subject=int(name[3:5]);night=int(name[5]);meta=metadata[(subject,night)]
        if subject in seen:raise ValueError('Repeated participant')
        seen.add(subject);p=data_dir/name;expected=hashes['sleep-cassette/'+name]
        if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise ValueError('Annotation checksum mismatch')
        with pyedflib.EdfReader(str(p)) as h:o,d,l=h.readAnnotations()
        epochs=int(max(float(a)+float(b) for a,b in zip(o,d))//30)
        audit=audit_common_support(stages_from_annotations(o,d,l,epochs))
        records.append(dict(file=name,subject_id=subject,night=night,metadata=meta,sha256=expected,
                            annotation_epochs=epochs,supported_event_count_pairs=sum(v['events']>=3 for v in audit['pairs'].values()),
                            capacity_not_disproven_pairs=sum(v['events']>=3 and not v['full_matching_impossible'] for v in audit['pairs'].values()),audit=audit))
    return dict(scope=manifest.get('analysis_scope','Exploratory annotation-only feasibility, one previously inspected participant plus nine newly audited. No raw EEG QC, no effect or cognition; no global matching sufficiency claim.'),parameters=dict(bin_epochs=60,context_radius=10,min_events=3),records=records)
if __name__=='__main__':
    a=argparse.ArgumentParser()
    for name in ('manifest','data-dir','checksum','metadata','out'):a.add_argument('--'+name,type=Path,required=True)
    v=a.parse_args();v.out.write_text(json.dumps(run(v.manifest,v.data_dir,v.checksum,v.metadata),indent=2)+'\n')
