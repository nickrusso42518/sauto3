#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Send bogus NetFlow v5 packets to the DevNet Stealthwatch
Enterprise sandbox FlowCollector component to test policy alarms.
"""

from scapy.all import *

if __name__ == "__main__":

    # Build the Netflow v5 payload
    netflow = (
        NetflowHeader()
        / NetflowHeaderV5(count=1)
        / NetflowRecordV5(
            src="209.182.177.5",
            dst="209.182.177.6",
            srcport=42518,
            dstport=43283,
        )
    )

    # Send the IP packet to the FlowCollector on port 2055 (v5 default)
    # The utun2 interface is my personal VPN interface; yours may vary
    send(IP(dst="10.10.20.61") / UDP(dport=2055) / netflow, iface="utun2")
