# GyroPalmRealtimeRobot class for Python
# Written by Dominick Lee. Last updated 2/28/2024
# Released under MIT license.

import asyncio
import websockets
import ssl
import json
import time

class GyroPalmRealtimeRobot:
    def __init__(self, robotID, secret):
        self.robotID = robotID
        self.secret = secret
        self.onGestureCallback = None
        self.onIncomingCallback = None
        self.onConnectionCallback = None
        self.ws = None
        self.lastSentPayload = time.time()
        self.verbose = False

    def setVerbose(self, verbose):
        self.verbose = verbose

    def setOnGestureCallback(self, callback):
        self.onGestureCallback = callback

    def setOnIncomingCallback(self, callback):
        self.onIncomingCallback = callback

    def setOnConnectionCallback(self, callback):
        self.onConnectionCallback = callback

    async def sendHeartbeat(self, ws):
        while True:
            # Check if more than 1 second has passed since the last payload was sent
            if time.time() - self.lastSentPayload > 1:
                heartbeat = json.dumps({"action": "heartbeat"})
                await ws.send(heartbeat)
                if self.verbose: print("%s\n" % heartbeat)
            else:
                if self.verbose: print("Skipped heartbeat \n")
            await asyncio.sleep(50)

    async def sendPayload(self, payload):
        if self.ws is not None and self.ws.open:
            self.lastSentPayload = time.time()  # Update timestamp when payload sent
            payloadObj = json.dumps({"action": "pubRobot", "robotID": self.robotID, "sensorVal": payload})
            await self.ws.send(payloadObj)
        else:
            if self.verbose: print("Cannot send. WebSocket is not connected \n")

    async def main(self):
        async with websockets.connect("wss://gyropalm.com:3200", ssl=ssl._create_unverified_context()) as self.ws:
            welcomeMessage = await self.ws.recv()
            welcomeMessage = json.loads(welcomeMessage)
            if self.verbose: print("\n%s\n" % welcomeMessage)

            authorizationMessage = json.dumps({'action': "newRobot", 'robotID': self.robotID, 'secret': self.secret}, sort_keys=True, indent=4)
            if self.verbose: print("%s\n" % authorizationMessage)
            await self.ws.send(authorizationMessage)

            confirmationMessage = await self.ws.recv()
            confirmationMessage = json.loads(confirmationMessage)
            if self.verbose: print("%s\n" % confirmationMessage)

            # Initialize other tasks here as needed

            time.sleep(0.5)

            asyncio.ensure_future(self.sendHeartbeat(self.ws))

            while True:
                msg = await self.ws.recv()
                msg = json.loads(msg)
                #print("%s" % msg)

                if "action" in msg and "command" in msg:
                    if msg["action"] == "data" and "command" in msg:
                        try:
                            payload_obj = json.loads(msg["command"])
                            # Assuming payload_obj is valid JSON and contains the expected JSON data
                            if "gestureID" in payload_obj:
                                if self.onGestureCallback:
                                    asyncio.ensure_future(self.onGestureCallback(payload_obj["gestureID"]))
                            else:
                                if self.onIncomingCallback:
                                    asyncio.ensure_future(self.onIncomingCallback(payload_obj))

                        except json.JSONDecodeError:
                            # Here, you can decide what to do if the command is not valid JSON
                            if self.onIncomingCallback:
                                asyncio.ensure_future(self.onIncomingCallback(msg["command"]))

                            if msg["command"] == 'ping':
                                await self.sendPayload("pong")