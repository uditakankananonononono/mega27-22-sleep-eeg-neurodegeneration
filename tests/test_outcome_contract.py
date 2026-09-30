import unittest
from dataclasses import replace
from src.dreaming22.outcome_contract import ProspectiveMetadata, audit_linkage

class TestOutcomeContract(unittest.TestCase):
    def setUp(self):
        self.row = ProspectiveMetadata('synthetic-site', 'p1', 'sub-p1', '1', 70., 500., 2500., True)
        self.thresholds = dict(min_event_days=365.,max_event_days=2190.,min_negative_followup_days=2190.)
    def check(self, row):
        row.validate(**self.thresholds)
    def test_valid_positive_and_negative(self):
        self.check(self.row)
        self.check(replace(self.row, label=False,event_days=None))
    def test_unknown_followup_is_not_negative(self):
        for followup in (0., 1000., float('nan')):
            with self.assertRaises(ValueError):
                self.check(replace(self.row, label=False,event_days=None,followup_days=followup))
    def test_prevalent_and_late_events_rejected(self):
        for event in (-1.,0.,364.,2191.,float('nan'),None):
            with self.assertRaises(ValueError): self.check(replace(self.row,event_days=event))
    def test_string_false_is_not_true(self):
        for label in ('FALSE','TRUE',0,1,None):
            with self.assertRaises(ValueError): self.check(replace(self.row,label=label))
    def test_conflicting_event_metadata(self):
        with self.assertRaises(ValueError): self.check(replace(self.row,label=False))
        with self.assertRaises(ValueError): self.check(replace(self.row,followup_days=400.))
    def test_missing_linkage(self):
        with self.assertRaises(ValueError): self.check(replace(self.row,person=''))
    def test_thresholds_must_be_explicit_and_ordered(self):
        with self.assertRaises(ValueError): self.row.validate(min_event_days=2200.,max_event_days=2190.,min_negative_followup_days=2190.)
    def test_duplicate_person_or_file(self):
        with self.assertRaises(ValueError): audit_linkage([self.row,replace(self.row,session='2')])
        with self.assertRaises(ValueError): audit_linkage([self.row,replace(self.row,person='p2')])
        self.assertEqual(audit_linkage([self.row]),dict(participants=1,sources=1))
    def test_empty_cohort(self):
        with self.assertRaises(ValueError): audit_linkage([])

if __name__ == '__main__': unittest.main()
