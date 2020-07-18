#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Abstract base class to encompass common logic for all
Cisco Stealthwatch security products.
"""

import requests


class CiscoSWBase:
    """
    Abstract base class for Cisco Stealthwatch security products.
    """

    def __init__(self, host):
        """
        Contains common logic when creating objects for any Cisco
        security product. The "base_url" is a string representing the
        first half of any request as individual resources can be
        appended for each request.
        """

        # Retain supplied host and create a new, long-lived HTTP session
        self.host = host
        self.sess = requests.session()

        # Sometimes common headers can be re-used over and over.
        # Content-Type not supplied because it isn't always JSON, and
        # just by setting the "json" kwarg, requests sets the Content-Type.
        self.headers = {"Accept": "application/json"}

    def base_req(self, url, method="get", **kwargs):
        """
        Describes the basic process to issue an HTTP request to a given
        URL. The default method is "get" and the keyword arguments
        are processed by the well-known request() method.
        """

        # If headers were not supplied, use the default headers. Some
        # requests have wildly different headers, so we cannot use
        # them all the time
        if "headers" not in kwargs:
            kwargs["headers"] = self.headers

        # Issue the generic HTTP request using the object's session attribute
        resp = self.sess.request(
            url=url,
            method=method,
            **kwargs,
        )

        # If any errors occurred (status code >= 400), raise an HTTPError
        resp.raise_for_status()

        # No errors occurred; return the entire response object
        return resp

    def req(self, resource, **kwargs):
        """
        Abstract method that children must implement. Will generally rely on
        base_req() for the core logic with some additional input/output
        processing as required for each product.
        """

        raise NotImplementedError("Abstract method that children must implement")
