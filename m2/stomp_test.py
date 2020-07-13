#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: 
https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/pxGrid-Provider
"""

import requests
import stomp


def main():
    """
    Execution begins here.
    """

    # The ISE sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # Define the sandbox login information
    host, port = ("10.10.20.70", 8910)
    username, password = ("admin", "C1sco12345!")

    https_url = f"https://{host}:{port}/pxgrid"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    resp = requests.post(
        f"{https_url}/control/AccountCreate",
        headers=headers,
        json={"nodeName": "nick"},
        verify=False,
    )
    print(resp.text)

    data = resp.json()
    auth = (data["userName"], data["password"])

    resp = requests.post(
        f"{https_url}/control/AccountActivate",
        headers=headers,
        auth=auth,
        json={"description": "nick testing"},
        verify=False,
    )
    print(resp.text)


def try_stomp():
    # Create a new STOMP connection to ISE for pxGrid connectivity
    host_port = ("10.10.20.70", 8910)
    username, password = "nick", "WgzG0qmTZvr5g3Zz"
    pxgrid = stomp.Connection([host_port])
    pxgrid.set_listener("debugger", stomp.PrintingListener())
    pxgrid.connect(username, password, wait=True)
    


if __name__ == "__main__":
    try_stomp()
    #main()
