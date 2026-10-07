import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from key_space_baseline import occupancy
class KeySpaceTests(unittest.TestCase):
    def test_exact_empty_contains_coarse_empty(self):
        stages=['N2']*180
        for i in (30,70,110):stages[i]='N3'
        cells=occupancy(stages)
        self.assertTrue(cells)
        for c in cells:
            self.assertLessEqual(c['coarse_empty'],c['exact_empty'])
            self.assertLessEqual(c['exact_empty'],c['events'])
            self.assertTrue(all(p['observed_histograms']<=p['controls'] for p in c['event_conditional_pools']))
