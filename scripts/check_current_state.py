"""Read-only current-state audit. Does not count historical tests as current."""
import json,re,unittest,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root),str(root/'scripts')]
from manuscript_tables import run

def check():
    state=json.loads((root/'protocol/current_gates.json').read_text())
    actual=unittest.defaultTestLoader.discover(str(root/'tests')).countTestCases()
    if actual!=state['software_tests']:raise ValueError('Test-count ledger differs from discovered suite')
    words=len((root/'paper/identifiability_working_manuscript.md').read_text().split())
    if words!=state['working_manuscript_words_including_headings_references']:raise ValueError('Manuscript word count drift')
    readme=(root/'README.md').read_text()
    if f'{actual} passing tests' not in readme or f'manuscript is {words} words' not in readme:raise ValueError('README count drift')
    t=run(root/'results');c=state['census']
    for source,prefix in [('sleep_edf_unique','sleep_edf'),('cap_healthy','cap')]:
        for key,field in [('recordings','unique_recordings' if prefix=='sleep_edf' else 'recordings'),('cells','eligible_cells'),('deficits','deficit_cells')]:
            if t[source][key]!=c[prefix+'_'+field]:raise ValueError('Census ledger drift')
    if any(state['gates'].values()):raise ValueError('Current unachieved gate changed: inspect source evidence before updating audit')
    return dict(discovered_tests=actual,manuscript_words=words,gates='All listed clinical/signal/paper-delivery gates remain false')
if __name__=='__main__':print(json.dumps(check(),indent=2))
