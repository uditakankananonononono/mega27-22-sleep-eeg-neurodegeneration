import unittest
import numpy as np
from src.dreaming22.matched_controls import matched_transition_control, equal_recording_summary

class MatchedControlTests(unittest.TestCase):
    def make(self):
        # Identical sparse stage motifs repeated within one fixed time stratum.
        s=['N2']*180
        for i in (30,70,110): s[i]='N3'
        return s
    def test_zero_change_matched_null(self):
        s=self.make();r=matched_transition_control(np.zeros(len(s)),s,bin_epochs=180,context_radius=1)
        self.assertTrue(r['pairs']['N2>N3']['complete_support'])
        self.assertEqual(r['pairs']['N2>N3']['mad_difference'],0.)
        used=[]
        for i,j in r['pairs']['N2>N3']['indices']: used.extend((i-1,i,j-1,j))
        self.assertEqual(len(used),len(set(used)))
    def test_matching_does_not_inspect_power(self):
        s=self.make();a=matched_transition_control(np.zeros(len(s)),s,bin_epochs=180,context_radius=1)
        b=matched_transition_control(np.arange(len(s))**2,s,bin_epochs=180,context_radius=1)
        self.assertEqual(a['pairs']['N2>N3']['indices'],b['pairs']['N2>N3']['indices'])
    def test_missing_common_support_is_missing(self):
        s=['N2','N3']*20
        r=matched_transition_control(np.zeros(len(s)),s,bin_epochs=40,context_radius=1)
        self.assertIsNone(r['recording_median_difference'])
        self.assertTrue(all(not p['complete_support'] for p in r['pairs'].values()))
    def test_unknown_context_excluded(self):
        s=self.make();s[29]='UNKNOWN'
        r=matched_transition_control(np.zeros(len(s)),s,bin_epochs=180,context_radius=1)
        self.assertIsNone(r['pairs']['N2>N3']['mad_difference'])
    def test_no_cross_time_bin_match(self):
        s=self.make();r=matched_transition_control(np.zeros(len(s)),s,bin_epochs=20,context_radius=1)
        for p in r['pairs'].values():
            for i,j in p['indices']: self.assertEqual(i//20,j//20)
    def test_reject_nonfinite_and_alignment(self):
        for x in ([0.], [0.,float('nan')]):
            with self.assertRaises(ValueError): matched_transition_control(x,['N2','N2'])
    def test_equal_recording_not_pair_weighted(self):
        self.assertEqual(equal_recording_summary([{'recording_median_difference':1.}, {'recording_median_difference':3.}, {'recording_median_difference':None}]),2.)
    def test_known_dispersion_injection(self):
        s=self.make();x=np.zeros(len(s));x[30]=1;x[70]=2;x[110]=3
        r=matched_transition_control(x,s,bin_epochs=180,context_radius=1)
        self.assertEqual(r['pairs']['N2>N3']['mad_difference'],1.)

if __name__=='__main__': unittest.main()
