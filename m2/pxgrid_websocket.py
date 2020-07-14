import websocket

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

    def start(self, ise_host, topic):
        #self.op_open = PxGridWebsocket._on_open
        self.ise_host = ise_host
        self.topic = topic
        self.run_forever(sslopt=self.sslopt)

    def _send_stomp_command(self, command, headers=None, body=None):

        # The command text goes first, followed by a newline
        text = f"{command}\n"

        # If headers exist, print in "key:value" format on separate lines
        if headers:
            for key, value in headers.items():
                text += f"{key}:{value}\n"

        # If body exists, append to text with leading newline
        if body:
            text += f"\n{body}"

        # Add null terminator to signify end of command
        text += "\0"

        # Print status message, issue command, and wait. More advanced
        # async techniques are more robust, but out of scope
        print(f"Sending STOMP command:\n{text}")
        self.send(text.encode("utf-8"))
        #time.sleep(5)


    @staticmethod
    def _on_message(ws, message):
        print(f"Message: {message}")

    @staticmethod
    def _on_error(ws, error):
        print(f"Error: {error}")

    @staticmethod
    def _on_close(ws):
        print("websocket closed")

    @staticmethod
    def _on_open(ws):
        print("websocket opened")

        connect_headers = {"host": ws.ise_host, "accept-version": "1.2"}
        connect_recv = ws._send_stomp_command("CONNECT", connect_headers)
        print("websocket CONNECT complete")

        subscribe_headers = {"destination": ws.topic, "id": "my-id"} 
        subscribe_rx = ws._send_stomp_command("SUBSCRIBE", subscribe_headers)
        print("websocket SUBSCRIBE complete")
