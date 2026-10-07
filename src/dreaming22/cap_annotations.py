"""Conservative CAP REMlogic staging parser, no gap carry-forward.

Epoch grid begins at the first explicit sleep-stage event. Unknown intervals
stay unknown. R&K stages 3/4 map to N3. CAP microevents are not sleep labels.
"""
import re
from .features import STAGES
MAP={'SLEEP-S0':'W','SLEEP-S1':'N1','SLEEP-S2':'N2','SLEEP-S3':'N3','SLEEP-S4':'N3','SLEEP-REM':'REM'}
def parse_cap_stages(text):
    events=[];offset=0;previous=None;columns=None
    for line in text.splitlines():
        fields=line.split('\t')
        if fields[0]=='Sleep Stage':
            columns={name.replace('Duration [s]','Duration[s]'):i for i,name in enumerate(fields)}
            if not all(k in columns for k in ('Time [hh:mm:ss]','Event','Duration[s]')):raise ValueError('Missing staging columns')
            continue
        if columns is None:continue
        if len(fields)<=max(columns.values()):continue
        fields=[fields[columns['Sleep Stage']],'',fields[columns['Time [hh:mm:ss]']],fields[columns['Event']],fields[columns['Duration[s]']]]
        if not fields[3].startswith('SLEEP-'):continue
        if not re.fullmatch(r'\d{2}[:.]\d{2}[:.]\d{2}',fields[2]):raise ValueError('Bad stage clock')
        h,m,s=map(int,re.split('[:.]',fields[2]))
        if h>23 or m>59 or s>59:raise ValueError('Bad stage clock')
        t=h*3600+m*60+s
        if previous is not None and t<previous:
            if previous-t<12*3600:raise ValueError('Nonchronological staging')
            offset+=86400
        previous=t;t+=offset
        d=float(fields[4])
        if not d>0 or not d<float('inf'):raise ValueError('Invalid duration')
        if events and t<events[-1][0]+events[-1][1]:raise ValueError('Overlapping stage intervals')
        events.append((t,d,MAP.get(fields[3],'UNKNOWN')))
    if not events:raise ValueError('No stage events')
    origin=events[0][0];end=max(t+d for t,d,_ in events);n=int((end-origin)//30)
    stages=[];j=0
    for i in range(n):
        lo=origin+i*30;hi=lo+30
        while j<len(events) and events[j][0]+events[j][1]<=lo:j+=1
        if j<len(events) and events[j][0]<=lo and events[j][0]+events[j][1]>=hi:stages.append(events[j][2])
        else:stages.append('UNKNOWN')
    return stages
