import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from manuscript_tables import summarize,run
class ManuscriptTableTests(unittest.TestCase):
    def test_known_archived_counts(self):
        t=run(Path(__file__).resolve().parents[1]/'results')
        for source,expected in [('sleep_edf_unique',(153,1417,1415)),('sleep_edf_earliest',(78,707,705)),('sleep_edf_second',(77,726,726)),('cap_healthy',(16,77,77))]:
            s=t[source];self.assertEqual((s['recordings'],s['cells'],s['deficits']),expected)
        p=t['sleep_edf_unique']['pairs']
        self.assertEqual(p['N2>N3']['cells']-p['N2>N3']['deficits'],2)
        self.assertEqual(sum(q['cells']-q['deficits'] for q in p.values()),2)
    def test_unparsed_rejected(self):
        with self.assertRaises(ValueError):summarize([dict(file='n1',parser_error='error')])
