# realtime_robot_test.py
# This is a basic example of how to use the GyroPalmRealtimeRobot SDK for Python
# Integrate this example into your robot control code

import asyncio
from gyropalm_control.gp_realtime_robot import GyroPalmRealtimeRobot

async def onGestureReceived(gestureID):
    print(f"Gesture ID: {gestureID}")

async def onIncoming(payload):
    print("Incoming: %s" % payload)

counter = 0

async def send_data_periodically(realtimeObj):
    while True:
        global counter  # Use global variable for testing
        await realtimeObj.sendPayload("Robot Data " + str(counter))
        counter += 1
        await asyncio.sleep(2)  # Delay a couple seconds before sending (15 FPS max)

if __name__ == '__main__':
    robotID = "r123456"         # Update this to your robotID
    secret = "c1122334455"      # Update this to your robot's secret
    gpRobot = GyroPalmRealtimeRobot(robotID, secret)
    gpRobot.setVerbose(True)      # To enable debug messages. Comment out to disable.
    gpRobot.setOnGestureCallback(onGestureReceived)
    gpRobot.setOnIncomingCallback(onIncoming)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                gpRobot.main(),  # Main routine which handles receiving data callbacks
                send_data_periodically(gpRobot)  # Sub routine for sending data
            )
        )
    finally:
        loop.close()
