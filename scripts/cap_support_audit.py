"""Hash-verified descriptive CAP annotation audit; no raw EEG or cognition."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dreaming22.cap_annotations import parse_cap_stages
from dreaming22.support_audit import audit_common_support

def run(manifest,data_dir,checksums):
    m=json.loads(manifest.read_text());hashes={x.split()[1].lstrip('*'):x.split()[0] for x in checksums.read_text().splitlines() if len(x.split())==2};rows=[]
    for e in m['files']:
        n=e['file']
        if Path(n).name!=n:raise ValueError('Invalid file')
        p=data_dir/n;digest=hashlib.sha256(p.read_bytes()).hexdigest()
        if digest!=hashes[n]:raise ValueError('Checksum mismatch')
        try:
            stages=parse_cap_stages(p.read_text(encoding='utf-8-sig'));audit=audit_common_support(stages,bin_epochs=m['parameters']['bin_epochs'],context_radius=m['parameters']['context_radius'])
            rows.append(dict(file=n,sha256=digest,epochs=len(stages),unknown_epochs=stages.count('UNKNOWN'),audit=audit))
        except ValueError as err:rows.append(dict(file=n,sha256=digest,parser_error=str(err)))
    cells=[p for r in rows if 'audit' in r for p in r['audit']['pairs'].values() if p['events']>=m['parameters']['min_events']]
    return dict(scope='CAP healthy annotation-only independent-source feasibility; no EEG effect, disease result or proven cross-source participant independence.',parameters=m['parameters'],records=rows,summary=dict(selected=len(rows),parsed=sum('audit' in r for r in rows),event_floor_cells=len(cells),proven_deficit_cells=sum(p['full_matching_impossible'] for p in cells)))
if __name__=='__main__':
    a=argparse.ArgumentParser()
    for n in ('manifest','data-dir','checksums','out'):a.add_argument('--'+n,type=Path,required=True)
    v=a.parse_args();v.out.write_text(json.dumps(run(v.manifest,v.data_dir,v.checksums),indent=2,allow_nan=False)+'\n')
