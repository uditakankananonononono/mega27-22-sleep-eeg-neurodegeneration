"""Reconcile recording identities before pooling overlapping audit subsets."""
import json,argparse
from pathlib import Path

def reconcile(paths):
    unique={};duplicate=[]
    for p in paths:
        for row in json.loads(p.read_text())['records']:
            n=row['file']
            if n in unique:
                if unique[n]!=row:raise ValueError('Conflicting repeated recording')
                duplicate.append(n)
            else:unique[n]=row
    cells=[p for r in unique.values() for p in r['audit']['pairs'].values() if p['events']>=3]
    return dict(unique_recordings=len(unique),duplicate_files=duplicate,event_floor_cells=len(cells),proven_deficit_cells=sum(p['full_matching_impossible'] for p in cells))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('audits',type=Path,nargs='+');v=a.parse_args();print(json.dumps(reconcile(v.audits),indent=2))
