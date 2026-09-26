import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from dreaming22.features import stage_transitions, epoch_bandpower, recording_stage_bandpower, transition_context_bandpower

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

class TransitionSignatureTests(unittest.TestCase):
    def test_unknown_gap_never_creates_transition(self):
        signal=np.ones(5*3000)
        self.assertIsNone(transition_context_bandpower(signal,100,["N2","UNKNOWN","REM","N2","REM"], min_events=2))
    def test_two_or_more_separate_transitions(self):
        fs=100
        t=np.arange(3000)/fs
        epochs=[np.sin(2*np.pi*f*t) for f in [2,2,2,2]]
        result=transition_context_bandpower(np.concatenate(epochs),fs,["N2","REM","N2","REM"],min_events=2)
        self.assertAlmostEqual(result["delta"],0.,places=2)
    def test_requires_nonempty_events(self):
        with self.assertRaises(ValueError): transition_context_bandpower(np.ones(3000),100,["N2"],min_events=0)
    def test_rejects_misaligned(self):
        with self.assertRaises(ValueError): transition_context_bandpower(np.ones(2999),100,["REM"])
