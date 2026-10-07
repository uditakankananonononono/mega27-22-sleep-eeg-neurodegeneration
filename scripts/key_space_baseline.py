"""Post-review descriptive key occupancy, not a changed matching estimand.

Compares empty candidate pools before/after adding exact context to the same
start-stage/time-bin key, retaining event thinning and event-epoch exclusions.
Coarse pools do not certify matches, unbiased effects or a valid alternative.
"""
import json,sys,math,hashlib,argparse
from pathlib import Path
from collections import defaultdict
import pyedflib
sys.path[:0]=[str(Path(__file__).resolve().parents[1]/'src'),str(Path(__file__).resolve().parent)]
from dreaming22.features import STAGES
from dreaming22.cap_annotations import parse_cap_stages
from sleep_edfx_pilot import stages_from_annotations

def occupancy(stages):
    names=sorted(STAGES);events=defaultdict(list);stable=[]
    for i in range(11,len(stages)-10):
        if stages[i-1] not in STAGES or stages[i] not in STAGES:continue
        ctx=stages[i-11:i-1]+stages[i+1:i+11]
        if any(s not in STAGES for s in ctx):continue
        k=(stages[i-1],i//60,tuple(ctx.count(s) for s in names))
        if stages[i-1]==stages[i]:stable.append((i,k))
        else:events[stages[i-1]+'>'+stages[i]].append((i,k))
    out=[]
    for pair,items in sorted(events.items()):
        used=set();retained=[]
        for i,k in items:
            if used.intersection((i-1,i)):continue
            retained.append((i,k));used.update((i-1,i))
        if len(retained)<3:continue
        pools=defaultdict(list)
        for i,k in stable:
            if not used.intersection((i-1,i)):pools[k[:2]].append(k[2])
        coarse_empty=0;exact_empty=0;bins=[]
        for i,k in retained:
            h=pools[k[:2]]
            coarse_empty+=not h;exact_empty+=k[2] not in h
            bins.append(dict(controls=len(h),observed_histograms=len(set(h))))
        out.append(dict(pair=pair,events=len(retained),coarse_empty=coarse_empty,exact_empty=exact_empty,event_conditional_pools=bins))
    return out

def run(root,data):
    sources={}
    for source,files in [('sleep_edf',['all_cassette_annotation_support.json','cassette_second_night_support.json']),('cap',['cap_healthy_support.json'])]:
        rows={r['file']:r for f in files for r in json.loads((root/f).read_text())['records']};allcells=[]
        for n,r in sorted(rows.items()):
            p=data/n if source=='sleep_edf' else data/'cap'/n
            if hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:raise ValueError('Checksum mismatch')
            if source=='sleep_edf':
                with pyedflib.EdfReader(str(p)) as h:stages=stages_from_annotations(*h.readAnnotations(),r['annotation_epochs'])
            else:stages=parse_cap_stages(p.read_text(encoding='utf-8-sig'))
            cells=occupancy(stages)
            for c in cells:
                original=r['audit']['pairs'][c['pair']]
                if c['events']!=original['events'] or c['exact_empty']!=original['events_with_no_exact_control']:raise ValueError('Baseline differs from original contract')
            allcells.extend(cells)
        pools=[p for c in allcells for p in c['event_conditional_pools']];sizes=sorted(p['controls'] for p in pools);occupied=sorted(p['observed_histograms'] for p in pools)
        sources[source]=dict(recordings=len(rows),cells=len(allcells),events=sum(c['events'] for c in allcells),coarse_empty_events=sum(c['coarse_empty'] for c in allcells),exact_empty_events=sum(c['exact_empty'] for c in allcells),event_weighted_controls_min=min(sizes),event_weighted_controls_median=sizes[len(sizes)//2],event_weighted_controls_max=max(sizes),event_weighted_observed_histograms_median=occupied[len(occupied)//2],event_weighted_observed_histograms_max=max(occupied))
    return dict(scope='Post-review descriptive occupancy diagnostic, not confirmatory or a replacement estimand. Coarse pools do not prove feasible matching.',possible_20_epoch_five_stage_histograms=math.comb(24,4),possible_keys_per_time_bin=5*math.comb(24,4),sources=sources)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--results',type=Path,required=True);a.add_argument('--data',type=Path,required=True);a.add_argument('--out',type=Path,required=True);v=a.parse_args();v.out.write_text(json.dumps(run(v.results,v.data),indent=2)+'\n')
