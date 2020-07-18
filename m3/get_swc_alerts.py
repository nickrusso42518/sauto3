#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collect and display the SWC alerts.
"""

from cisco_sw_cloud import CiscoSWCloud

# Quick and dirty approach for variable inputs; update these
# with your account handle, personal SWC email address, and API key
SWC_ACCOUNT = "cisco-nickrus"
SWC_EMAIL = "nickrus@cisco.com"
SWC_API_KEY = "3c47285ded8b42ffa82c85b761fcc279"


def main():
    """
    Execution starts here.
    """

    # Create new SWC object
    swc = CiscoSWCloud(
        account_name=SWC_ACCOUNT, email=SWC_EMAIL, api_key=SWC_API_KEY
    )

    # Get the current SWC alerts (watchlist triggers, etc)
    alerts = swc.req("alerts/alert/")
    for alert in alerts["objects"]:

        # Print a two-line summary including the time, type, and description
        print(f"{alert['created']}: {alert['type']}")
        print(f"Details: {alert['description']}\n")


if __name__ == "__main__":
    main()
