import unittest
from src.dreaming22.cap_annotations import parse_cap_stages

def row(time,event,duration=30):return '\t'.join(('S2','Unknown',time,event,str(duration),'EEG'))
class CAPParserTests(unittest.TestCase):
    def test_midnight_harmonization_and_microevent(self):
        s='\n'.join((row('23:59:30','SLEEP-S3'),row('23:59:40','MCAP-A1',5),row('00:00:00','SLEEP-S4'),row('00:00:30','SLEEP-REM')))
        self.assertEqual(parse_cap_stages(s),['N3','N3','REM'])
    def test_gap_not_imputed(self):
        self.assertEqual(parse_cap_stages(row('22:00:00','SLEEP-S2')+'\n'+row('22:01:00','SLEEP-S2')),['N2','UNKNOWN','N2'])
    def test_partial_and_unscored_unknown(self):
        s=row('22:00:00','SLEEP-S2',20)+'\n'+row('22:00:30','SLEEP-UNSCORED')
        self.assertEqual(parse_cap_stages(s),['UNKNOWN','UNKNOWN'])
    def test_malformed_rejected(self):
        for text in ('empty',row('25:00:00','SLEEP-S2'),row('22:00:00','SLEEP-S2',0),row('22:00:00','SLEEP-S2')+'\n'+row('22:00:10','SLEEP-S3'),row('22:01:00','SLEEP-S2')+'\n'+row('22:00:00','SLEEP-S3')):
            with self.assertRaises(ValueError):parse_cap_stages(text)
