import unittest
from src.dreaming22.support_audit import disjoint_capacity,audit_common_support
class SupportAuditTests(unittest.TestCase):
    def test_maximum_capacity_not_raw_count(self):
        self.assertEqual(disjoint_capacity([1,2,3,4,5]),3)
        self.assertEqual(disjoint_capacity([5,1,1,3]),3)
        self.assertEqual(disjoint_capacity([]),0)
    def test_no_stable_pool_proves_failure(self):
        r=audit_common_support(['N2','N3']*20,bin_epochs=40,context_radius=1)
        for p in r['pairs'].values():
            self.assertTrue(p['full_matching_impossible'])
            self.assertEqual(p['unavoidable_unmatched_lower_bound'],p['events'])
    def test_known_support(self):
        s=['N2']*180
        for i in (30,70,110):s[i]='N3'
        p=audit_common_support(s,bin_epochs=180,context_radius=1)['pairs']['N2>N3']
        self.assertFalse(p['full_matching_impossible'])
        self.assertEqual(p['events'],3)
    def test_unknown_context_counts(self):
        r=audit_common_support(['N2']*10+['UNKNOWN']+['N2']*10,context_radius=1)
        self.assertEqual(r['exclusions']['unknown_pair'],2)
        self.assertEqual(r['exclusions']['unknown_context'],2)
    def test_invalid_parameters(self):
        for v in (0,1.5,True):
            with self.assertRaises(ValueError):audit_common_support(['N2']*20,context_radius=v)
