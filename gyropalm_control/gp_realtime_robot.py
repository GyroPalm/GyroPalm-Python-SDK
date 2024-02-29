# GyroPalmRealtimeRobot class for Python
# Written by Dominick Lee. Last updated 2/28/2024
# Released under MIT license.

import asyncio
import contextlib
import threading
import websockets
import ssl
import json
import time

class GyroPalmRealtimeRobot:
    def __init__(self, robotID, secret):
        self.robotID = robotID
        self.secret = secret
        self.heartbeat_task_handle = None
        self.loop = asyncio.new_event_loop()
        self.thread = None
        self.onTickerCallback = None
        self.ticker_task_handle = None
        self.ticker_interval = 2
        self.onGestureCallback = None
        self.onIncomingCallback = None
        self.onConnectionCallback = None
        self.onRobotIncomingCallback = None
        self.ws = None
        self.lastSentPayload = time.time()
        self.verbose = False
        self.connectedDevices = []

    def setVerbose(self, verbose):
        self.verbose = verbose

    def setOnGestureCallback(self, callback):
        self.onGestureCallback = callback

    def setOnIncomingCallback(self, callback):
        self.onIncomingCallback = callback

    def setOnRobotIncomingCallback(self, callback):
        self.onRobotIncomingCallback = callback

    def setOnConnectionCallback(self, callback):
        self.onConnectionCallback = callback

    def setTickerFunction(self, user_function, interval=2):
        #Register a user-defined asynchronous function to be called periodically.
        self.onTickerCallback = user_function
        self.ticker_interval = interval

    def start(self):
        self.thread = threading.Thread(target=self._start_event_loop)
        self.thread.start()

    def _start_event_loop(self):
        asyncio.set_event_loop(self.loop)
        if self.onTickerCallback:
            self.ticker_task_handle = asyncio.ensure_future(self._run_ticker_task())  # Schedule the periodic task
        self.loop.run_until_complete(self.main())
        self.loop.close()

    async def _run_ticker_task(self):
        """
        Internal method to schedule and run the user-defined periodic task.
        """
        while True:
            await self.onTickerCallback(self)  # Execute the user-defined function
            await asyncio.sleep(self.ticker_interval)  # Wait for the specified interval

    def run_task(self, async_function):
        asyncio.run_coroutine_threadsafe(async_function(self), self.loop)

    async def cleanup(self):
        if self.heartbeat_task_handle and not self.heartbeat_task_handle.done():
            self.heartbeat_task_handle.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.heartbeat_task_handle

        if self.ticker_task_handle and not self.ticker_task_handle.done():
            self.ticker_task_handle.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.ticker_task_handle

        # Cancel and await all remaining tasks, suppressing the cancellation error.
        tasks = [t for t in asyncio.all_tasks(self.loop) if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

        # Then attempt to close the WebSocket connection.
        if self.ws and not self.ws.closed:
            await self.ws.close()

        # Ensure all tasks are indeed cancelled.
        await asyncio.sleep(0.1)  # Give a moment for all tasks to cancel.

        self.loop.stop()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.create_task, self.cleanup())
        self.thread.join(timeout=5)

    async def sendHeartbeat(self, ws):
        try:
            while True:
                if time.time() - self.lastSentPayload > 1:
                    heartbeat = json.dumps({"action": "heartbeat"})
                    if self.ws is not None and self.ws.open:
                        await ws.send(heartbeat)
                    if self.verbose: print("%s\n" % heartbeat)
                else:
                    if self.verbose: print("Skipped heartbeat. Connection active.\n")
                # Use asyncio.sleep instead of time.sleep and make it interruptible
                await asyncio.sleep(50)
        except asyncio.CancelledError:
            if self.verbose: print("Heartbeat task closed.")

    async def connectRobot(self, robotID, apiKey):
        if self.ws is not None and self.ws.open:
            self.lastSentPayload = time.time()  # Update timestamp when payload sent
            payloadObj = json.dumps({"action": "subRobot", "robotID": robotID, "apiKey": apiKey})
            await self.ws.send(payloadObj)
            self.connectedDevices.append(robotID)
            return True
        else:
            if self.verbose: print("Cannot subscribe. WebSocket is not connected \n")
            return False

    async def sendPayload(self, payload):
        if self.ws is not None and self.ws.open:
            self.lastSentPayload = time.time()  # Update timestamp when payload sent
            payloadObj = json.dumps({"action": "pubRobot", "robotID": self.robotID, "sensorVal": payload})
            await self.ws.send(payloadObj)
        else:
            if self.verbose: print("Cannot send. WebSocket is not connected \n")

    async def main(self):
        try:
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

                self.heartbeat_task_handle = asyncio.create_task(self.sendHeartbeat(self.ws))

                while True:
                    try:
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

                        elif "action" in msg and msg["action"] == "data":
                            for device_id in msg.keys():
                                if device_id != "action":  # Skip the 'action' key
                                    if device_id in self.connectedDevices:
                                        # Found a matching device ID, handle the payload
                                        try:
                                            payload_obj = json.loads(msg[device_id])
                                            # Assuming payload_obj is valid JSON and contains the expected JSON data
                                            if self.onIncomingCallback:
                                                asyncio.ensure_future(self.onIncomingCallback(device_id, payload_obj))

                                        except json.JSONDecodeError:
                                            # Here, you can decide what to do if the command is not valid JSON
                                            if self.onIncomingCallback:
                                                asyncio.ensure_future(self.onRobotIncomingCallback(device_id, msg[device_id]))
                                            if msg[device_id] == 'ping':
                                                await self.sendPayload("pong")

                                        break  # Optional: break if you only expect one device ID match
                    except websockets.exceptions.ConnectionClosedOK:
                        print("WebSocket closed.")
                        break
        except asyncio.CancelledError:
            if self.verbose: print("WebSocket connection and tasks closed.")