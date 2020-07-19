#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collect and display the SWC alerts.
"""

import json
import os
from cisco_sw_cloud import CiscoSWCloud

# Quick and dirty approach for variable inputs; update these
# with your account handle, personal SWC email address, and API key
SWC_ACCOUNT = "cisco-nickrus"
SWC_EMAIL = "nickrus@cisco.com"
SWC_API_KEY = "3c47285ded8b42ffa82c85b761fcc279"

# Specify output directory for resulting flow files
OUTDIR = "swc_flows"


def main():
    """
    Execution starts here.
    """

    # Create new SWC object
    swc = CiscoSWCloud(
        account_name=SWC_ACCOUNT, email=SWC_EMAIL, api_key=SWC_API_KEY
    )

    # Load in the query param dicts from JSON file
    with open("flow_query_params.json", "r") as handle:
        flow_queries = json.load(handle)

    # Data loading complete; create output directory for JSON files
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

    # Iterate over each set of query params
    for name, params in flow_queries.items():

        # Collect the flows for a given set of query params
        flows = swc.req("snapshots/session-data/", params=params)

        # Write the flow data to disk
        outfile = f"{OUTDIR}/flow_{name.replace(' ', '_')}.json"
        with open(outfile, "w") as handle:
            json.dump(flows["objects"], handle, indent=2)

        # Print status message to indicate success
        print(f"Wrote flow '{name}' to {outfile}")

if __name__ == "__main__":
    main()
