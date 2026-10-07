import itertools,sys,random,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dreaming22.support_audit import audit_common_support
from dreaming22.features import STAGES

def oracle(stages,bin_epochs,radius):
    names=tuple(sorted(STAGES)); events={}; stable=[]
    for i in range(1,len(stages)):
        if stages[i-1] not in STAGES or stages[i] not in STAGES:continue
        lo=i-1-radius;hi=i+1+radius
        if lo<0 or hi>len(stages):continue
        ctx=stages[lo:i-1]+stages[i+1:hi]
        if any(s not in STAGES for s in ctx):continue
        key=(stages[i-1],i//bin_epochs,tuple(ctx.count(s) for s in names))
        if stages[i-1]==stages[i]:stable.append((i,key))
        else:events.setdefault(stages[i-1]+'>'+stages[i],[]).append((i,key))
    out={}
    for pair,items in events.items():
        used=set(); retained=[]
        for i,key in items:
            if used.intersection((i-1,i)):continue
            retained.append((i,key));used.update((i-1,i))
        controls=[(i,key) for i,key in stable if not used.intersection((i-1,i))]
        demand={k:sum(q==k for _,q in retained) for _,k in retained}
        best=0
        for bits in range(1<<len(controls)):
            epochs=set();counts={};valid=True;n=0
            for j,(i,key) in enumerate(controls):
                if not bits&(1<<j):continue
                if epochs.intersection((i-1,i)):valid=False;break
                counts[key]=counts.get(key,0)+1
                if counts[key]>demand.get(key,0):valid=False;break
                epochs.update((i-1,i));n+=1
            if valid:best=max(best,n)
        out[pair]=(len(retained),best)
    return out
class SupportBoundOracleTests(unittest.TestCase):
    def test_bound_never_exceeds_exact_unmatched_count(self):
        rng=random.Random(20261007)
        cases=list(itertools.product(('N2','N3'),repeat=9))
        cases += [tuple(rng.choice(('N2','N3','UNKNOWN')) for _ in range(12)) for _ in range(200)]
        checks=0
        for stages in cases:
            stages=list(stages)
            for b,r in ((4,1),(20,1),(4,2)):
                result=audit_common_support(stages,bin_epochs=b,context_radius=r)
                exact=oracle(stages,b,r)
                for pair,p in result['pairs'].items():
                    count,best=exact[pair]
                    self.assertEqual(p['events'],count)
                    self.assertLessEqual(p['unavoidable_unmatched_lower_bound'],count-best,(stages,b,r,pair,p,best))
                    if p['full_matching_impossible']:self.assertLess(best,count)
                    checks+=1
        self.assertEqual(checks,3093)

    def test_zero_bound_is_not_global_feasibility(self):
        stages=['N3','N2','N3','N3','N3','N3','N2','N3','N2','N3']
        p=audit_common_support(stages,bin_epochs=30,context_radius=1)['pairs']['N3>N2']
        self.assertEqual(p['events'],2)
        self.assertFalse(p['full_matching_impossible'])
        self.assertEqual(p['unavoidable_unmatched_lower_bound'],0)
        self.assertEqual(oracle(stages,30,1)['N3>N2'],(2,1))
