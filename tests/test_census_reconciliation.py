import unittest,sys,json,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from reconcile_cassette_counts import reconcile
class ReconciliationTests(unittest.TestCase):
    def test_duplicate_dedup_and_conflict(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.json';b=Path(d)/'b.json'
            row=dict(file='same',audit=dict(pairs={'pair':dict(events=3,full_matching_impossible=True)}))
            a.write_text(json.dumps(dict(records=[row])));b.write_text(a.read_text())
            self.assertEqual(reconcile([a,b]),dict(unique_recordings=1,duplicate_files=['same'],event_floor_cells=1,proven_deficit_cells=1))
            row['audit']['pairs']['pair']['events']=4;b.write_text(json.dumps(dict(records=[row])))
            with self.assertRaises(ValueError):reconcile([a,b])
