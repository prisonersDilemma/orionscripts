#!/usr/bin/env python3.6

from unittest import TestCase

import whois

log = '/home/na/git/prisonersDilemma/orionscripts/whois/tests/samples-micro/splunk-export.csv'

class TargetsTest(TestCase):

    def test_gettargets(self):
        # date = '2017-11-10'
        trgts = whois.gettargets(log, trgtdate='2017-11-10')
        cntrl = {'103.13.63.22'  : { 'timestamp': "2017-11-10T16:29:46.000-0800", },
                 '176.120.196.61': { 'timestamp': "2017-11-10T16:35:00.000-0800", }, }
        self.assertEqual(trgts, cntrl)


    def test_yesterdaystargets(self):
        trgts = whois.yesterdays_targets(log)
        cntrl = {
            '177.207.7.19':{'timestamp': "2017-11-14T16:41:36.000-0800"},
            '112.209.131.119':{'timestamp': "2017-11-14T16:41:51.000-0800"},
            '211.120.220.233':{'timestamp': "2017-11-14T16:49:58.000-0800"},
            '216.115.243.146':{'timestamp': "2017-11-14T16:55:20.000-0800"},
            '61.34.72.195':{'timestamp': "2017-11-14T17:03:10.000-0800"},
            '121.113.241.248':{'timestamp': "2017-11-14T17:08:36.000-0800"},
            '186.62.147.240':{'timestamp': "2017-11-14T17:09:04.000-0800"},
            '203.140.181.237':{'timestamp': "2017-11-14T17:18:54.000-0800"},
        }
        trgts = whois.gettargets(log, '2017-11-10')


    # Test that we are not making an extra iteration.


if __name__ == '__main__':
    TargetsTest()
    # $ cd whois
    # $ python3.6 -m unittest tests.targets_tests
