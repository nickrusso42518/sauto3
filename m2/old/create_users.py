#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Basic consumption of Cisco Identity Services Engine (ISE)
REST API using the public Cisco DevNet sandbox (requires reservation).
Creates new internal users using the External RESTful Services (ERS)
feature by reading in data from a JSON file.
"""

import json
import requests


def main():
    """
    Execution begins here.
    """

    # The ISE sandbox uses a self-signed cert at present, so let's ignore any
    # obvious security warnings for now.
    requests.packages.urllib3.disable_warnings()

    # The API path below is what the DevNet sandbox uses for API testing,
    # which may change in the future. Be sure to check the IP address as
    # I suspect this changes frequently. See here for more details:
    # https://developer.cisco.com/docs/identity-services-engine
    # You can access the API documentation at URL /ers/sdk
    api_path = "https://10.10.20.70:9060/ers"
    auth = ("admin", "C1sco12345!")

    # Headers are consistent for GET and POST requests
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Load in the list of users to add from the JSON file
    with open("new_users.json", "r") as handle:
        new_users = json.load(handle)

    # Iterate over the list of dictionaries to process each one
    for new_user in new_users:

        # Define a new user by wrapping it in the proper top-most key
        body = {"InternalUser": new_user}

        # Issue HTTP POST request with the new user dict as the message body
        add_user = requests.post(
            f"{api_path}/config/internaluser",
            headers=headers,
            auth=auth,
            json=body,
            verify=False,
        )

        # Print appropriate message based on HTTP status code
        if add_user.status_code == 201:
            print(f"Added new {new_user['name']} user successfully")
        else:
            print(f"Unexpected response for {new_user['name']}")
            print(f"Status: {add_user.status_code}/{add_user.reason}")

    # Perform an HTTP GET to collect the list of users, which should
    # include the recently added user
    get_users = requests.get(
        f"{api_path}/config/internaluser",
        headers=headers,
        auth=auth,
        verify=False,
    )

    # Iterate over users and print out the ID, name, and description
    for user in get_users.json()["SearchResult"]["resources"]:
        print(f"{user['id']}: {user['name']} / {user['description']}")


if __name__ == "__main__":
    main()
