"""Deterministic descriptive manuscript tables from archived audit outputs."""
import json,argparse
from collections import defaultdict
from pathlib import Path

def summarize(rows):
    unique={}
    for r in rows:
        name=r['file']
        if name in unique and unique[name]!=r:raise ValueError('Conflicting recording')
        unique[name]=r
    pairs=defaultdict(lambda:dict(cells=0,deficits=0,events=0,no_exact_pool_events=0,unmatched_lower_bound=0))
    for row in unique.values():
        if 'audit' not in row:raise ValueError('Unparsed recording cannot enter summary')
        for name,p in row['audit']['pairs'].items():
            if p['events']<3:continue
            q=pairs[name];q['cells']+=1;q['deficits']+=int(p['full_matching_impossible']);q['events']+=p['events'];q['no_exact_pool_events']+=p['events_with_no_exact_control'];q['unmatched_lower_bound']+=p['unavoidable_unmatched_lower_bound']
    return dict(recordings=len(unique),cells=sum(q['cells'] for q in pairs.values()),deficits=sum(q['deficits'] for q in pairs.values()),pairs=dict(sorted(pairs.items())))
def run(root):
    first=json.loads((root/'all_cassette_annotation_support.json').read_text())['records']
    second=json.loads((root/'cassette_second_night_support.json').read_text())['records']
    cap=json.loads((root/'cap_healthy_support.json').read_text())['records']
    return dict(scope='Descriptive annotation support. Event sums are within retained pair cells, not independent people or EEG effects. Sources not pooled.',sleep_edf_unique=summarize(first+second),sleep_edf_earliest=summarize(first),sleep_edf_second=summarize(second),cap_healthy=summarize(cap))
def markdown(tables):
    text='# Verified manuscript tables\n\n'+tables['scope']+'\n'
    for source in ('sleep_edf_unique','sleep_edf_earliest','sleep_edf_second','cap_healthy'):
        s=tables[source]
        text+='\n## '+source+'\n\nRecordings: '+str(s['recordings'])+'. Eligible cells: '+str(s['cells'])+'. Proven deficits: '+str(s['deficits'])+'.\n\n'
        text+='| Stage pair | Cells >=3 events | Deficit cells | Retained events | No exact pool events | Unmatched lower bound |\n|---|---:|---:|---:|---:|---:|\n'
        for pair,q in s['pairs'].items():text+='| '+pair+' | '+' | '.join(str(q[k]) for k in ('cells','deficits','events','no_exact_pool_events','unmatched_lower_bound'))+' |\n'
    return text
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--results',type=Path,required=True);a.add_argument('--json-out',type=Path,required=True);a.add_argument('--markdown-out',type=Path,required=True);v=a.parse_args();t=run(v.results);v.json_out.write_text(json.dumps(t,indent=2)+'\n');v.markdown_out.write_text(markdown(t))
