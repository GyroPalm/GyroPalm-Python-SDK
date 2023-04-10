# GyroPalmDriving class for robotic control
# Written by Dominick Lee. Last updated 4/3/2023
# Released under MIT license.

import asyncio
import time

class GyroPalmDriving:
    def __init__(self):
        # Change these constants as desired
        self.easing_accel = 0.2     # Typically 0.2
        self.easing_decel = 0.6     # Typically 0.6
        self.refreshPeriod = 40     # In miliseconds. 30ms = 33.3 FPS, 40ms = 25 FPS, 50ms = 20 FPS
        self.snap_x = 1             # Snap joystick X to 0 when its below this value
        self.snap_y = 1             # Snap joystick Y to 0 when its below this value
        self.joyXmin = -100         # Min X input value
        self.joyXmax = 100          # Max X input value
        self.joyYmin = -100         # Min Y input value
        self.joyYmax = 100          # Max Y input value
        self.outXmin = -1.0         # Min X output value
        self.outXmax = 1.0          # Max X output value
        self.outYmin = -1.0         # Min Y output value
        self.outYmax = 1.0          # Max Y output value
        # Do NOT edit below
        self.joyX = 0.0
        self.joyY = 0.0
        self.x = 0.0
        self.y = 0.0
        self.drive_robot_callback = None
        self.lastInput = time.time()
        self.stopSent = False

    # Helper function that maps one range to another and contrains the output
    def constrainMap(self, value, from_low, from_high, to_low, to_high):
        mapped_value = (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low
        contrained_value = max(min(mapped_value, to_high), to_low)
        final_val = round(contrained_value, 6) # Round to 6 decimals
        return final_val

    # Sets the rate of acceleration and deceleration smoothing
    def setAccelProfile(self, accel_ease, decel_ease):
        self.easing_accel = accel_ease
        self.easing_decel = decel_ease

    # Sets the threshold for respective snapping on X and Y axes
    def setSnapCenter(self, snapX, snapY):
        self.snap_x = snapX
        self.snap_y = snapY

    # Sets the input and output values for mapping and constrain
    def setInputOutputRange(self, inXmin, inXmax, inYmin, inYmax, outXmin, outXmax, outYmin, outYmax):
        self.joyXmin = inXmin
        self.joyXmax = inXmax
        self.joyYmin = inYmin
        self.joyYmax = inYmax
        self.outXmin = outXmin
        self.outXmax = outXmax
        self.outYmin = outYmin
        self.outYmax = outYmax

    # Sets the callback method for output X and Y back to the user
    def setDriveRobotCallback(self, callback):
        self.drive_robot_callback = callback

    # Run this input method whenever joystick receives new raw data
    def newInput(self, inX, inY):
        self.joyX = inX
        self.joyY = inY
        self.stopSent = False   # Reset stop
        self.lastInput = time.time()    # Update sent time

    # Helper function to determine if user is accelerating or decelerating
    def isDecelerating(self, current, target):
        return (current < 0 and target > current) or (current > 0 and target < current)

    # Driving loop that runs processDriveEasing and forwards smoothed output to callback
    async def loop(self):
        while True:
            # Assumes the user ran 'newInput' function
            # processDriveEasing takes in joyX and joyY, setting new values for x and y
            self.processDriveEasing(self.joyX, self.joyY)

            # Get timestamp in seconds to time-out on inactive input
            unixTS = time.time()

            # Check if callback is set
            if self.drive_robot_callback is not None:
                # Forward callback if no signal loss (more than 2 seconds is signal loss)
                if unixTS - self.lastInput < 2:
                    # Normalize and Constrain
                    finalX = self.constrainMap(self.x, self.joyXmin, self.joyXmax, self.outXmin, self.outXmax)
                    finalY = self.constrainMap(self.y, self.joyYmin, self.joyYmax, self.outYmin, self.outYmax)
                    # Forward values to callback
                    self.drive_robot_callback(finalX, finalY)
                else:
                    # Send stop command once
                    if self.stopSent is False:
                        # Send stop command couple times
                        for x in range(2):
                            self.x = 0.0
                            self.y = 0.0
                            finalX = self.constrainMap(self.x, self.joyXmin, self.joyXmax, self.outXmin, self.outXmax)
                            finalY = self.constrainMap(self.y, self.joyYmin, self.joyYmax, self.outYmin, self.outYmax)
                            self.drive_robot_callback(finalX, finalY)
                            await self.delay(self.refreshPeriod)
                        self.stopSent = True

            await self.delay(self.refreshPeriod) # Non-blocking delay

    def processDriveEasing(self, targetX, targetY):
        # Snap to center filter
        if abs(targetX) <= self.snap_x:
            targetX = 0
        if abs(targetY) <= self.snap_y:
            targetY = 0

        # Perform cumulative easing
        easing_x = self.easing_decel if self.isDecelerating(self.x, targetX) else self.easing_accel
        self.x += (targetX - self.x) * easing_x

        easing_y = self.easing_decel if self.isDecelerating(self.y, targetY) else self.easing_accel
        self.y += (targetY - self.y) * easing_y

        # Round to 6 decimals
        self.x = round(self.x, 6)
        self.y = round(self.y, 6)

    # Helper function to mimic non-blocking delay
    async def delay(self, milliseconds):
        await asyncio.sleep(milliseconds / 1000)


