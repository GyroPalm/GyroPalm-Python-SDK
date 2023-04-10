# driving_test.py
# This is an example of how to use the GyroPalmRealtime and GyroPalmDriving for Python

import asyncio
from gyropalm_control.gp_driving import GyroPalmDriving
from gyropalm_control.gp_realtime import GyroPalmRealtime

startControl = False

async def onGestureReceived(gestureID):
    print(f"Gesture ID: {gestureID}")

async def onDriveCommand(payload):
    print("Drive: %s" % payload)
    x = payload.get('x', 0)
    y = payload.get('y', 0)
    # Forward new input values to gpDriving
    gpDriving.newInput(x, y)

async def onIncoming(payload):
    print("Incoming: %s" % payload)

async def onConnection(isConnected):
    global startControl

    if isConnected:
        print("Wearable is Online")
        startControl = True
    else:
        print("Wearable is Offline")

def drive_robot_callback(x, y):
    # Print out processed X and Y
    if startControl:
        print("x: {}, y: {}".format(x, y))
        # Write your code here to forward x and y values to your robot

async def main():
    # Run both realtime and driving
    await asyncio.gather(realtime.loop(), gpDriving.loop())

if __name__ == '__main__':
    wearableID = "gp00011122"   # Update this to your wearableID
    apiKey = "c1122334455"      # Update this to your API key
    realtime = GyroPalmRealtime(wearableID, apiKey)
    realtime.setOnConnectionCallback(onConnection)
    realtime.setOnGestureCallback(onGestureReceived)
    realtime.setOnDriveCallback(onDriveCommand)
    realtime.setOnIncomingCallback(onIncoming)

    gpDriving = GyroPalmDriving()
    # Set the callback for robot output
    gpDriving.setDriveRobotCallback(drive_robot_callback)
    # Set the min/max ranges of your inputs/outputs for map and constrain
    gpDriving.setInputOutputRange(-400, 400, -400, 400, -0.3, 0.3, -0.3, 0.3)
    # Input x and y will snap to 0 when below these numbers
    gpDriving.setSnapCenter(35, 35)
    # Set acceleration/deceleration easing constants
    gpDriving.setAccelProfile(0.25, 0.6)

    # Run loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
