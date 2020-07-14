#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: 
https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/pxGrid-Provider
"""

from base64 import b64encode
import ssl
import time
import requests
from websocket import create_connection


class PxGrid:
    def __init__(self, ise_host, verify=False):

        # If verify is false, we should also disable SSL warnings (sandbox)
        self.verify = verify
        if not self.verify:
            requests.packages.urllib3.disable_warnings()

        # Create a long-lived TCP session for HTTP requests, plus base URL
        self.sess = requests.session()
        self.ise_host = ise_host
        self.base_url = f"https://{self.ise_host}:8910/pxgrid/control"
        self.auth = None

        # Define generic send/receive JSON headers for HTTP
        self.http_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    #
    # Generic helper methods
    #

    def req(self, resource, method="post", **kwargs):
        if not "json" in kwargs:
            kwargs["json"] = {}

        resp = self.sess.request(
            url=f"{self.base_url}/{resource}",
            method=method,
            headers=self.http_headers,
            auth=self.auth,
            verify=self.verify,
            **kwargs
        )
        resp.raise_for_status()

        if resp.text:
            return resp.json()

        return {}

    def lookup_service(self, service_name):
        serv_resp = self.req("ServiceLookup", json={"name": service_name})
        return serv_resp

    def send_stomp_command(self, command, headers=None, body=None):

        # The command text goes first, followed by a newline
        text = f"{command}\n"

        # If headers exist, print in "key:value" format on separate lines
        if headers:
            for key, value in headers.items():
                text += f"{key}:{value}\n"

        # Forced newline to separate command/headers from body
        text += "\n"

        # If body exists, append to text
        if body:
            text += body

        # Add null terminator to signify end of command
        text += "\0"

        # Print status message, issue command, and wait. More advanced
        # async techniques are more robust, but out of scope
        print(f"Sending STOMP command:\n{text}")
        self.ws.send(text)
        time.sleep(10)

        # Return whatever response data was seen in response
        return self.ws.recv()

    #
    # User/connection initialization
    #

    def activate_user(self, username):

        # Store the username for later (used for websockets too)
        self.username = username

        # Issue a POST request to create a new account with specified username
        # This request does not require authentication
        acct = self.req("AccountCreate", json={"nodeName": username})

        # Build the HTTP basic auth 2-tuple for future requests
        self.auth = (self.username, acct["password"])

        # User creation successful; print status message
        print(f"PxGrid user {username} created. Please approve via ISE UI")

        # Loop forever (or until otherwise broken)
        while True:
            activate = self.req("AccountActivate")
            account_state = activate["accountState"].lower()
            print(f"Account state: {account_state}")

            # Test for different states. Enabled is good, disabled is bad
            if account_state == "enabled":
                break
            elif account_state == "disabled":
                raise ValueError(f"PxGrid user {username} disabled")

            # Docs recommend waiting 60 seconds between requests; will use
            # a smaller value to speed up testing
            time.sleep(10)

        print(f"PxGrid user {username} activated")

    def stomp_connect(self):
        """
        Not everyone wants to subscribe to security feeds via STOMP.
        """

        # Next, look up the pubsub service to get nodeName and websocket URL
        serv_resp = self.lookup_service("com.cisco.ise.pubsub")
        pub_node = serv_resp["services"][0]["nodeName"]

        # Issue POST request to generate secret between consumer (us) and
        # specific ISE node publisher
        secret_resp = self.req("AccessSecret", json={"peerNodeName": pub_node})

        # Extract the secret and manually build the HTTP basic auth base 64
        # encoded string, since websockets isn't as user-friendly as requests
        self.secret = secret_resp["secret"]
        b64 = b64encode((f"{self.username}:{self.secret}").encode()).decode()

        # Create the websocket headers and URL for use with STOMP later
        self.ws_headers = {"Authorization": f"Basic {b64}"}
        self.ws_url = serv_resp["services"][0]["properties"]["wsUrl"]

        try:
            self.ws = create_connection(
                self.ws_url,
                header=self.ws_headers,
                sslopt={"cert_reqs": ssl.CERT_NONE},
            )

            # Issue STOMP CONNECT message with host header targeting ISE node
            rx = self.send_stomp_command("CONNECT", {"host": self.ise_host})
            print(f"Received: {rx}")

        except Exception as exc:
            print(f"websocket exception raised: {exc}")
            raise
        finally:
            self.ws.close()
            print(f"websocket connect to {self.ise_host} closed")


def main():
    """
    Execution begins here.
    """

    # IP address is 10.10.20.70
    pxgrid = PxGrid("ise24.abc.inc")

    pxgrid.activate_user("nick")
    pxgrid.stomp_connect()

    # pxgrid.subscribe("whatever")


if __name__ == "__main__":
    main()
