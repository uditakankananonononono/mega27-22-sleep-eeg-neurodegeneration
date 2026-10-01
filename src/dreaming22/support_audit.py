"""Stage-only common-support audit. Does not compute or select EEG effects.

Capacity is an upper bound: disjoint epochs are enforced within each exact
stratum, not across strata. Hence a deficit proves infeasibility, while enough
capacity does not certify a globally feasible assignment.
"""
from collections import defaultdict
from .features import STAGES, stage_transitions


def disjoint_capacity(boundaries):
    """Maximum disjoint equal-length adjacent pairs by chronological scheduling."""
    last=-2; count=0
    for i in sorted(set(boundaries)):
        if i>last+1:
            count+=1;last=i
    return count


def audit_common_support(stages, *, bin_epochs=60, context_radius=10):
    for v in (bin_epochs,context_radius):
        if type(v) is not int or v<1: raise ValueError('Positive integer parameters required')
    stage_transitions(stages)
    names=tuple(sorted(STAGES)); events=defaultdict(list); stable=[]
    exclusions=defaultdict(int)
    def key(i):
        lo=i-1-context_radius; hi=i+1+context_radius
        if lo<0 or hi>len(stages):return None,'edge'
        context=list(stages[lo:i-1])+list(stages[i+1:hi])
        if any(s not in STAGES for s in context):return None,'unknown_context'
        return (stages[i-1],i//bin_epochs,tuple(context.count(s) for s in names)),None
    for i in range(1,len(stages)):
        if stages[i-1] not in STAGES or stages[i] not in STAGES:
            exclusions['unknown_pair']+=1;continue
        k,reason=key(i)
        if reason:exclusions[reason]+=1;continue
        if stages[i-1]==stages[i]:stable.append((i,k))
        else:events[f'{stages[i-1]}>{stages[i]}'].append((i,k))
    result={}
    for pair,items in sorted(events.items()):
        retained=[];used=set()
        for i,k in items:
            if {i-1,i}&used:continue
            retained.append((i,k));used.update((i-1,i))
        controls=[(j,k) for j,k in stable if not {j-1,j}&used]
        demand=defaultdict(list);pools=defaultdict(list)
        for i,k in retained:demand[k].append(i)
        for j,k in controls:pools[k].append(j)
        deficit=0; absent=0;strata=[]
        for k,ii in sorted(demand.items()):
            jj=pools[k];capacity=disjoint_capacity(jj)
            short=max(0,len(ii)-capacity);deficit+=short
            if not jj:absent+=len(ii)
            strata.append(dict(start_stage=k[0],time_bin=k[1],context_counts=list(k[2]),
                               demand=len(ii),raw_controls=len(jj),
                               disjoint_capacity_upper_bound=capacity,deficit_lower_bound=short))
        result[pair]=dict(events=len(retained),events_with_no_exact_control=absent,
                          unavoidable_unmatched_lower_bound=deficit,
                          full_matching_impossible=deficit>0,strata=strata)
    return dict(pairs=result,exclusions=dict(exclusions),stage_order=list(names),
                scope='Stage/time/context support only; capacity sufficient is not global matching proof')
