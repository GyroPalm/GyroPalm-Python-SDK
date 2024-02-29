# realtime_test.py
# This is a basic example of how to use the GyroPalmRealtime SDK for Python

import asyncio
from gyropalm_control.gp_realtime import GyroPalmRealtime

async def onGestureReceived(gestureID):
    print(f"Gesture ID: {gestureID}")

async def onDriveCommand(payload):
    print("Drive: %s" % payload)

async def onIncoming(payload):
    print("Incoming: %s" % payload)

counter = 0

async def send_data_periodically(realtimeObj):
    while True:
        global counter  # Use global variable for testing
        await realtimeObj.sendPayload("Test Data " + str(counter))
        counter += 1
        await asyncio.sleep(2)  # Delay a couple seconds before sending (15 FPS max)

if __name__ == '__main__':
    wearableID = "gp00011122"   # Update this to your wearableID
    apiKey = "c1122334455"      # Update this to your API key
    gyropalm = GyroPalmRealtime(wearableID, apiKey)
    gyropalm.setVerbose(True)      # To enable debug messages. Comment out to disable.
    gyropalm.setOnGestureCallback(onGestureReceived)
    gyropalm.setOnDriveCallback(onDriveCommand)
    gyropalm.setOnIncomingCallback(onIncoming)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                gyropalm.main(),  # Main routine which handles receiving data callbacks
                send_data_periodically(gyropalm)  # Sub routine for sending data to wearable
            )
        )
    finally:
        loop.close()
