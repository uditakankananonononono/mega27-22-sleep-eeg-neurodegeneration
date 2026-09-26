import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from sleep_edfx_pilot import stages_from_annotations

class AnnotationTests(unittest.TestCase):
    def test_full_epoch_and_boundary(self):
        result=stages_from_annotations([0,30,60],[30,30,30],['Sleep stage 2','Sleep stage R','Sleep stage 3'],3)
        self.assertEqual(result,['N2','REM','N3'])
    def test_partial_epoch_excluded(self):
        self.assertEqual(stages_from_annotations([0,20],[20,40],['Sleep stage 2','Sleep stage R'],2),['UNKNOWN','REM'])
    def test_unknown_movement_excluded(self):
        self.assertEqual(stages_from_annotations([0],[30],['Movement time'],1),['UNKNOWN'])
    def test_r_and_n3_harmonize(self):
        self.assertEqual(stages_from_annotations([0,30,60],[30]*3,['Sleep stage R','Sleep stage 3','Sleep stage 4'],3),['REM','N3','N3'])
