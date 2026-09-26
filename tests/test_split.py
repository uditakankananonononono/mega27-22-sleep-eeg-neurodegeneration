import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from dreaming22.split import Record, audit_partitions

class SplitTests(unittest.TestCase):
    def setUp(self):
        self.train=[Record("r1","s1","p1","v1")]
        self.val=[Record("r2","s1","p2","v1")]
        self.test=[Record("r3","s2","p3","v1")]
    def test_distinct_subjects_and_sites(self):
        self.assertEqual(audit_partitions(self.train,self.val,self.test,True)["test"],1)
    def test_person_across_visits_leakage(self):
        with self.assertRaisesRegex(ValueError,"participant"):
            audit_partitions(self.train,self.val,[Record("r3","s1","p1","v2")])
    def test_same_recording_id_leakage(self):
        with self.assertRaisesRegex(ValueError,"recording"):
            audit_partitions(self.train,self.val,[Record("r1","s2","p3","v1")])
    def test_external_test_must_hold_out_source(self):
        with self.assertRaisesRegex(ValueError,"source"):
            audit_partitions(self.train,self.val,[Record("r3","s1","p3","v1")],True)
    def test_missing_identity_fails(self):
        with self.assertRaisesRegex(ValueError,"person_id"):
            Record("r4","s2","","v1")
    def test_empty_fold_fails(self):
        with self.assertRaisesRegex(ValueError,"nonempty"):
            audit_partitions(self.train,[],self.test)

if __name__ == "__main__": unittest.main()
