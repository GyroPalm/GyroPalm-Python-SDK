# realtime_robot_test.py
# This is a basic example of how to use the GyroPalmRealtimeRobot SDK for Python
# Integrate this example into your robot control code

import asyncio
from gyropalm_control.gp_realtime_robot import GyroPalmRealtimeRobot

async def onGestureReceived(gestureID):
    print(f"Gesture ID: {gestureID}")

async def onIncoming(payload):
    print("Incoming: %s" % payload)

if __name__ == '__main__':
    robotID = "r123456"         # Update this to your robotID
    secret = "c1122334455"      # Update this to your robot's secret
    gpRobot = GyroPalmRealtimeRobot(robotID, secret)
    gpRobot.setOnGestureCallback(onGestureReceived)
    gpRobot.setOnIncomingCallback(onIncoming)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(gpRobot.main())
    finally:
        loop.close()
