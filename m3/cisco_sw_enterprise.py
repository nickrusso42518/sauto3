#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around Cisco Stealthwatch Enterprise
to simplify API interactions.
"""

import time
from cisco_sw_base import CiscoSWBase


class CiscoSWEnterprise(CiscoSWBase):
    """
    Declaration of Cisco Stealthwatch Enterprise (SWE) SDK class.
    """

    def __init__(self, smc_host, username, password, tenant_name):
        """
        Constructor to create a new object. SWE uses a username/password
        pair in an HTTP POST body to obtain a cookie, which is automatically
        retained by "requests" when using a session (like SD-WAN).
        """

        # Retain the base URL and create a new, long-lived HTTP session
        super().__init__(host=smc_host)
        self.username = username
        self.password = password

        # Create the base URL, which isn't very generic since SWE has
        # many different API versions and paths
        self.base_url = f"https://{self.host}"

        # Perform initial authentication, ignore response data
        self.refresh_cookie()

        # Collect all tenants; you CANNOT specify an Accept header,
        # even though the response is JSON
        tenants = self.req("sw-reporting/v2/tenants", headers=None)

        # Iterate over all tenants, storing the tenant ID if the
        # tenant exists somewhere in the list of tenants
        for tenant in tenants["data"]:
            if tenant["name"].lower() == tenant_name.lower():
                self.tenant_id = tenant["id"]
                break

        # Tenant not found; cannot continue
        else:
            raise ValueError(f"tenant with name {tenant_name} not found")

    @staticmethod
    def devnet_reservable(self):
        """
        Class-level method that returns an object referencing the DevNet
        reservable sandbox to make it easier for consumers.
        """
        return CiscoSWEnterprise("10.10.20.60", "admin", "C1sco12345", "abc.inc")

    def refresh_cookie(self):
        """
        Get an authorization cookie to access the API. This is
        automatically called by the constructor by can be called by
        users manually when cookies expire.
        """

        # Build the JSON body with the username and password for initial auth
        body = {"username": self.username, "password": self.password}

        # Issue an HTTP POST request with the body above and return response
        resp = self.req("token/v2/authenticate", method="post", json=body)
        return resp

    def get_flows_from_ips(self, start_time, end_time, limit, source_ips):
        """
        Collect all flows from specific IP addresses in a given time period
        and up to a given limit.
        """

        # Define HTTP body to start the flow query
        body = {
            "startDateTime": start_time,
            "endDateTime": end_time,
            "recordLimit": limit,
            "subject": {"ipAddresses": {"includes": source_ips}},
            "flow": {"flowDirection": "BOTH", "includeInterfaceData": True},
        }

        # Construct the URL and issue the request, including the body
        flow_url = f"sw-reporting/v2/tenants/{self.tenant_id}/flows/queries"
        data = self.req(url, method="post", json=body)

        # Extract the query ID
        query_id = resp["data"]["query"]["id"]

        # Loop forever, waiting 5 seconds in between requests
        while True:
            time.sleep(5)

            # Get the flow status to check for completion, and print message
            status_resp = self.req(f"{flow_url}/{query_id}")
            status_msg = status_resp["data"]["query"]["status"].lower()
            print(f"Status of query {query_id}: {status_msg}")

            # If the flow is complete, break from the loop
            if status_msg == "completed":
                break

        # Flow collection complete; return a list of dicts containing flows
        flows = self.req(f"{flow_url}/{query_id}/results")
        return flows["data"]["flows"]
