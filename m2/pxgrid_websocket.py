#!/usr/bin/env python

"""
Author: Nick Russo
Purpose:
https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/pxGrid-Provider
"""

import websocket
import time


class PxGridWebsocket(websocket.WebSocketApp):

    def __init__(self, ws_url, header, sslopt):
        websocket.enableTrace(True)
        super().__init__(
            ws_url, 
            on_message=PxGridWebsocket._on_message,
            on_error=PxGridWebsocket._on_error,
            on_close=PxGridWebsocket._on_close,
            on_open=PxGridWebsocket._on_open,
            header=header,
        )
        self.sslopt = sslopt

    def start(self, pub_node, topic):
        #self.op_open = PxGridWebsocket._on_open
        self.pub_node = pub_node
        self.topic = topic
        self.run_forever(sslopt=self.sslopt)

    def _send_stomp_command(self, command, headers):

        # The command text goes first, followed by a newline
        text = f"{command}\n"

        # Print headers in "key:value" format on separate lines
        for key, value in headers.items():
            text += f"{key}:{value}\n"

        # Add newline and null terminator to signify end of command
        text += "\n\0"

        # Print status message, issue command, and wait. More advanced
        # async techniques are more robust, but out of scope
        # print(f"Sending STOMP command:\n{text}")
        byte_text = text.encode("utf-8")
        print(f"Sending STOMP bytes: {byte_text}")

        # Very important to set BINARY mode (hint buried in pxGrid docs)
        self.send(byte_text, opcode=websocket.ABNF.OPCODE_BINARY)
        time.sleep(1)


    @staticmethod
    def _on_message(ws, message):
        print(f"Received message bytes: {message}")

    @staticmethod
    def _on_error(ws, error):
        print(f"Received error bytes: {error}")

    @staticmethod
    def _on_close(ws):
        print("websocket closed")

    @staticmethod
    def _on_open(ws):
        print("websocket opened")

        # https://stomp.github.io/stomp-specification-1.2.html
        connect_headers = {"accept-version": "1.2", "host": ws.pub_node}
        ws._send_stomp_command("CONNECT", connect_headers)
        print("websocket CONNECT complete")

        subscribe_headers = {"destination": ws.topic, "id": "0"}
        ws._send_stomp_command("SUBSCRIBE", subscribe_headers)
        print("websocket SUBSCRIBE complete")
