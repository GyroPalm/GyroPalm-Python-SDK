# realtime_robot_test.py
# This is a basic example of how to use the GyroPalmRealtimeRobot SDK for Python
# Integrate this example into your robot control code

import asyncio
import time
from gyropalm_control.gp_realtime_robot import GyroPalmRealtimeRobot

async def onGestureReceived(gestureID):
    print(f"Gesture ID: {gestureID}")

async def onIncoming(payload):
    print("Incoming: %s" % payload)

async def onRobotIncoming(robotID, payload):
    print(f"Robot {robotID}: {payload}")

counter = 0

async def send_data_periodically(realtimeObj):
    global counter  # Use global variable for testing
    await realtimeObj.sendPayload("Robot Data " + str(counter))
    print("Data published")
    counter += 1

async def subscribe_to_robot(realtimeObj):
    while True:
        print("Connecting to robot...")
        is_connected = await realtimeObj.connectRobot("r123457", "c1122334455")
        if is_connected == True:
            print("Robot subscribed")
            break
        await asyncio.sleep(2)

if __name__ == '__main__':
    robotID = "r123456"         # Update this to your robotID
    secret = "c1122334455"      # Update this to your robot's secret
    gpRobot = GyroPalmRealtimeRobot(robotID, secret)
    gpRobot.setVerbose(True)      # To enable debug messages. Comment out to disable.
    gpRobot.setOnGestureCallback(onGestureReceived)
    gpRobot.setOnIncomingCallback(onIncoming)
    gpRobot.setOnRobotIncomingCallback(onRobotIncoming)
    gpRobot.setTickerFunction(send_data_periodically, interval=2) # Delay a couple seconds before sending (15 FPS max)

    gpRobot.start()

    ind = 0
    try:
        #gpRobot.run_task(subscribe_to_robot)      # Connect to another robot (Optional)
        while True:
            # Your code here to run repeatedly
            print("Hello World " + str(ind))
            ind += 1
            time.sleep(1)
    except KeyboardInterrupt:
        # Handle program exit via KeyboardInterrupt (Ctrl+C)
        print("Closing the connections gracefully...")
    finally:
        gpRobot.stop()
