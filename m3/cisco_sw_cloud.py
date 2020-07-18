#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a mini-SDK around Cisco Stealthwatch Cloud
to simplify API interactions.
"""

from cisco_sw_base import CiscoSWBase


class CiscoSWCloud(CiscoSWBase):
    """
    Declaration of Cisco Stealthwatch Cloud (SWC) SDK class.
    """

    def __init__(self, account_name, email, api_key):
        """
        Constructor to create a new object. SWC uses a custom
        Authorization header (similar to HTTP basic auth) with the
        user's email address and API key
        """

        # Retain the base URL and create a new, long-lived HTTP session
        host = f"{account_name}.obsrvbl.com"
        super().__init__(host=host)

        # Create the base URL which is used for all requests
        self.base_url = f"https://{self.host}/api/v3"

        # Update the headers dictionary with the authorization header
        self.headers["Authorization"] = f"ApiKey {email}:{api_key}"

    def req(self, resource, **kwargs):
        """
        Describes the basic process to issue an HTTP request to a given
        URL. The default method is "get" and the keyword arguments
        are processed by the well-known request() method.
        """

        # Call the base_req method with the full URL and other kwargs
        resp = super().base_req(f"{self.base_url}/{resource}", **kwargs)

        # If there is a body, it will be JSON; convert to Python objects
        if resp.text:
            # import json; print(json.dumps(resp.json(), indent=2))
            return resp.json()

        # Body was not present; return empty dict for consistency
        return {}
