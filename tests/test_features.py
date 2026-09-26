import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from dreaming22.features import stage_transitions, epoch_bandpower, recording_stage_bandpower

class FeatureTests(unittest.TestCase):
    def test_transitions_do_not_bridge_unknown(self):
        self.assertEqual(stage_transitions(["N2", "UNKNOWN", "REM", "N2", "N2"]), {"REM>N2": 1})
    def test_bad_stage_fails_closed(self):
        with self.assertRaises(ValueError): stage_transitions(["R", "N2"])
    def test_delta_signal(self):
        fs = 100
        signal = np.sin(2*np.pi*2*np.arange(3000)/fs)
        bands = epoch_bandpower(signal, fs)
        self.assertGreater(bands["delta"], 100*bands["alpha"])
    def test_bad_signal_fails_closed(self):
        with self.assertRaises(ValueError): epoch_bandpower(np.array([0., np.nan]), 100)
    def test_full_epoch_match(self):
        with self.assertRaises(ValueError): recording_stage_bandpower(np.zeros(2999),100,["REM"])
    def test_rem_stage_kept_separate(self):
        fs=100
        signal=np.sin(2*np.pi*2*np.arange(3000)/fs)
        result=recording_stage_bandpower(np.r_[signal,signal],fs,["REM","N3"])
        self.assertEqual(set(result), {"REM", "N3"})

if __name__ == "__main__": unittest.main()
