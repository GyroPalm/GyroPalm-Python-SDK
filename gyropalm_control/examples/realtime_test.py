# gyropalm_test.py
# This is a basic example of how to use the GyroPalmRealtime SDK for Python

import asyncio
from gp_realtime import GyroPalmRealtime

async def onGestureReceived(gestureID):
    print(f"Gesture ID: {gestureID}")

async def onDriveCommand(payload):
    print("Drive: %s" % payload)

async def onIncoming(payload):
    print("Incoming: %s" % payload)

if __name__ == '__main__':
    wearableID = "gp00011122"   # Update this to your wearableID
    apiKey = "c1122334455"      # Update this to your API key
    gyropalm = GyroPalmRealtime(wearableID, apiKey)
    gyropalm.setOnGestureCallback(onGestureReceived)
    gyropalm.setOnDriveCallback(onDriveCommand)
    gyropalm.setOnIncomingCallback(onIncoming)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(gyropalm.main())
    finally:
        loop.close()
