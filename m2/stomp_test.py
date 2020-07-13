#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: 
https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/pxGrid-Provider
"""

import base64
import ssl
import time
import requests
import stomp
import websocket
from websocket import create_connection
# pip install websocket-client


requests.packages.urllib3.disable_warnings()
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

    pxgrid_user = "nick"
    resp = requests.post(
        f"{https_url}/control/AccountCreate",
        headers=headers,
        json={"nodeName":pxgrid_user},
        verify=False,
    )
    print(resp.text)

    data = resp.json()
    auth = (data["userName"], data["password"])

    print(f"Username {pxgrid_user} created. Please approve via ISE UI")

    while True:
        resp = requests.post(
            f"{https_url}/control/AccountActivate",
            headers=headers,
            auth=auth,
            json={"description": "nick testing"},
            verify=False,
        )
        account_state = resp.json()["accountState"].lower()
        print(f"Account state: {account_state}")

        if account_state == "enabled":
            break
        elif account_state == "disabled":
            print("pxGrid account disabled (not approved)")
            return

        time.sleep(10)


def try_stomp():
    # Create a new STOMP connection to ISE for pxGrid connectivity
    host_port = ("10.10.20.70", 8910)
    username, http_password = "nick", "WgzG0qmTZvr5g3Zz"

    password = "jtR8cfkCqrVGR4j9"
    ws_url = "wss://10.10.20.70:8910/pxgrid/ise/pubsub"

    pxgrid = stomp.Connection([host_port])
    pxgrid.set_listener("debugger", stomp.PrintingListener())
    pxgrid.connect(username, password, wait=True)

def reg():
    body = {
        "name":"com.cisco.ise.config.anc",
        "properties": {
            "restBaseUrl":"https://pxgrid-041.cisco.com:8910/pxgrid/ise/config/anc",
            "wsPubsubService":"com.cisco.ise.pubsub",
            "statusTopic":"/topic/com.cisco.ise.config.anc.status"
        },
        "operations":[
            {
                "service": "com.cisco.ise.config.anc",
                 "operation": "gets"
            },
            {
                "service": "com.cisco.ise.config.anc",
                "operation": "sets"
            },
            {
                "service": "com.cisco.ise.pubsub",
                "operation": "publish /topic/com.cisco.ise.config.anc.status"
            },
            {
                "service": "com.cisco.ise.pubsub",
                "operation": "subscribe /topic/com.cisco.ise.config.anc.status"
            }
        ]
    }
    host, port = ("10.10.20.70", 8910)
    https_url = f"https://{host}:{port}/pxgrid"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = ("nick", "JL7iaxwCpWW4IDx5")
    resp = requests.post(
        f"{https_url}/control/ServiceRegister",
        headers=headers,
        auth=auth,
        json=body,
        verify=False,
    )
    print(resp.text)
    

def secret():
    host, port = ("10.10.20.70", 8910)
    https_url = f"https://{host}:{port}/pxgrid"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = ("nick", "JL7iaxwCpWW4IDx5")
    resp = requests.post(
        f"{https_url}/control/AccessSecret",
        headers=headers,
        auth=auth,
        json={"peerNodeName": "ise-pubsub-ise24"},
        verify=False,
    )
    print(resp.text)

def lookup():
    body = { "name":"com.cisco.ise.pubsub" }
    host, port = ("10.10.20.70", 8910)
    https_url = f"https://{host}:{port}/pxgrid"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = ("nick", "JL7iaxwCpWW4IDx5")
    resp = requests.post(
        f"{https_url}/control/ServiceLookup",
        headers=headers,
        auth=auth,
        json={ "name":"com.cisco.ise.session" },
        verify=False,
    )
    print(resp.text)
    resp = requests.post(
        f"{https_url}/control/ServiceLookup",
        headers=headers,
        auth=auth,
        json=body,
        verify=False,
    )
    print(resp.text)

def try_ws():
    node_name = "ise-pubsub-ise24"
    user = "nick"
    b64 = base64.b64encode((f"{user}:jtR8cfkCqrVGR4j9").encode()).decode()
    print(b64)

    try:
        ws = create_connection(
            "wss://ise24.abc.inc:8910/pxgrid/ise/pubsub",
            sslopt={"cert_reqs": ssl.CERT_NONE},
            header={'Authorization': 'Basic ' + b64}
        )
        print("open!")

        while True:
            result =  ws.recv()
            print("Received '%s'" % result)
    except Exception as exc:
        print(exc)
    finally:
        ws.close()






def build_stomp_command(command, headers=None, body=None):

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

    print(text)
    return text


if __name__ == "__main__":
    #main()
    #reg()
    #lookup()
    #secret()
    #try_stomp()
    try_ws()


