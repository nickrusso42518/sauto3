#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Send bogus RADIUS packets to the DevNet ISE sandbox to simulate
RADIUS failrues to test STOMP subscription telemetry.
"""

from radius import authenticate, NoResponse

if __name__ == "__main__":
    try:
        # Send some RADIUS packets to ISE with bogus credentials
        authenticate("wrong_secret", "user", "pass", "10.10.20.70", port=1812)
    except NoResponse:
        # Exception should be raised, so do nothing
        pass
