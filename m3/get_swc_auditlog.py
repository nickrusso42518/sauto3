#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collect the SWC audit log and create a CSV file for reference.
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
    audit_log = swc.req("audit/log/")

    # Create the column names for the CSV file
    text = "time,user,action,description\n"
    outfile = "audit_log.csv"

    # Iterate over each log entry for processing
    for item in audit_log["objects"]:

        # Actor name is always present but may be blank; use
        # the string "SYSTEM" for cleanliness
        if not item["actor_name"]:
            item["actor_name"] = "SYSTEM"

        # Create the CSV table row containing pertinent information
        text += f"{item['time']},{item['actor_name']},"
        text += f"{item['action']},{item['short_text']}\n"

    # Write the text to the outfile and print useful command to read it
    with open(outfile, "w") as handle:
        handle.write(text)
    print(f"Use 'column -s, -t {outfile} | less -S' to view from shell")


if __name__ == "__main__":
    main()
