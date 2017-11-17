#!/usr/bin/env python3.6

# Passed.

__date__ = '2017-11-14'
__version__ = (0,0,1)

from unittest import TestCase

import whois


class NaCatTester(TestCase):

    def test_nacat_module(self):
        # This single test actually tests every function in the nacat module,
        # as it uses the join_msg_from function to assemble the msg, in the
        # call to nacat, and join_msg_from uses join_msg.

        # Contains four targets:
        # 107.180.26.137 is the IP to badpackets.net, and 8.8.8.8 is google.
        # The other two are random IPs I grabbed from one of the sample logs.
        trgts = '/home/na/git/prisonersDilemma/orionscripts/whois/tests/samples-micro/nacat-input'
        reply = whois.nacat('whois.cymru.com', 43, whois.join_msg_from(trgts))
        cntrl = """\
Bulk mode; whois.cymru.com [2017-11-14 19:30:40 +0000]
26496   | 107.180.26.137   | AS-26496-GO-DADDY-COM-LLC - GoDaddy.com, LLC, US
4134    | 219.147.201.198  | CHINANET-BACKBONE No.31,Jin-rong Street, CN
24445   | 221.176.182.226  | CMNET-V4HENAN-AS-AP Henan Mobile Communications Co.,Ltd, CN
15169   | 8.8.8.8          | GOOGLE - Google LLC, US"""


if __name__ == '__main__':
    NaCatTester()
