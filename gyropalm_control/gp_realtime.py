# GyroPalmRealtime class for Python
# Written by Dominick Lee. Last updated 4/3/2023
# Released under MIT license.

import asyncio
import websockets
import ssl
import json
import time

class GyroPalmRealtime:
    def __init__(self, wearableID, apiKey):
        self.wearableID = wearableID
        self.apiKey = apiKey
        self.onGestureCallback = None
        self.onDriveCallback = None
        self.onIncomingCallback = None
        self.onConnectionCallback = None
        self.ws = None

    def setOnGestureCallback(self, callback):
        self.onGestureCallback = callback

    def setOnDriveCallback(self, callback):
        self.onDriveCallback = callback

    def setOnIncomingCallback(self, callback):
        self.onIncomingCallback = callback

    def setOnConnectionCallback(self, callback):
        self.onConnectionCallback = callback

    async def sendHeartbeat(self, ws):
        while True:
            heartbeat = json.dumps({"action": "heartbeat"})
            await ws.send(heartbeat)
            print("%s\n" % heartbeat)
            await asyncio.sleep(50)

    async def sendPayload(self, payload):
        await self.ws.send(payload)

    async def loop(self):
        async with websockets.connect("wss://gyropalm.com:3200", ssl=ssl._create_unverified_context()) as self.ws:
            welcomeMessage = await self.ws.recv()
            welcomeMessage = json.loads(welcomeMessage)
            print("\n%s\n" % welcomeMessage)

            authorizationMessage = json.dumps({'action': "sub", 'wearableID': self.wearableID, 'apiKey': self.apiKey}, sort_keys=True, indent=4)
            print("%s\n" % authorizationMessage)
            await self.ws.send(authorizationMessage)

            confirmationMessage = await self.ws.recv()
            confirmationMessage = json.loads(confirmationMessage)
            print("%s\n" % confirmationMessage)

            # Initialize other tasks here as needed

            time.sleep(0.5)

            asyncio.ensure_future(self.sendHeartbeat(self.ws))

            while True:
                msg = await self.ws.recv()
                msg = json.loads(msg)
                #print("%s" % msg)

                if self.wearableID in msg:
                    payload_obj = json.loads(msg[self.wearableID])
                    if "gestureID" in payload_obj:
                        if self.onGestureCallback:
                            asyncio.ensure_future(self.onGestureCallback(payload_obj["gestureID"]))
                    elif "x" in payload_obj and "y" in payload_obj:
                        if self.onDriveCallback:
                            asyncio.ensure_future(self.onDriveCallback(payload_obj))
                    else:
                        if self.onIncomingCallback:
                            asyncio.ensure_future(self.onIncomingCallback(payload_obj))

                    if msg[self.wearableID] == 'ping':
                        print("pong")

                if "action" in msg and "stat" in msg:
                    if msg['action'] == 'info' and msg['stat'] == 'online':
                        if self.onConnectionCallback:
                            asyncio.ensure_future(self.onConnectionCallback(True))
                    elif msg['action'] == 'info' and msg['stat'] == 'offline':
                        if self.onConnectionCallback:
                            asyncio.ensure_future(self.onConnectionCallback(False))


