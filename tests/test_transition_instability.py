import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from dreaming22.transition_instability import robust_mad, transition_instability

class TransitionTests(unittest.TestCase):
    def test_mad(self):
        self.assertEqual(robust_mad([1.,2.,4.]),1.)
        self.assertIsNone(robust_mad([1.,2.]))
    def test_stage_pair_support_and_control(self):
        fs=100;t=np.arange(3000)/fs
        one=np.sin(2*np.pi*2*t)
        stages=['N2','N3','N2','N3','N2','N3','N2','N3']
        x=np.concatenate([one*(1+i*.1) for i in range(len(stages))])
        out=transition_instability(x,fs,stages)
        self.assertEqual(out['transitions']['N2>N3']['delta']['events'],4)
        self.assertIsNotNone(out['transitions']['N2>N3']['delta']['mad_log_change'])
        self.assertEqual(out['transitions']['N3>N2']['delta']['events'],3)
    def test_unknown_not_bridged(self):
        one=np.sin(2*np.pi*2*np.arange(3000)/100)
        x=np.tile(one,5)
        out=transition_instability(x,100,['N2','UNKNOWN','N3','N2','N3'])
        self.assertEqual(out['transitions']['N2>N3']['delta']['events'],1)
        self.assertIsNone(out['transitions']['N2>N3']['delta']['mad_log_change'])
    def test_minimum_not_cherry_picked(self):
        with self.assertRaises(ValueError): transition_instability(np.ones(3000),100,['N2'],min_events=1)
    def test_misalignment(self):
        with self.assertRaises(ValueError): transition_instability(np.ones(2999),100,['N2'])
