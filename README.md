# GyroPalm Python SDK
Python SDK for GyroPalm Developers

## Overview ##
The GyroPalm Python software development kit (SDK) enables developers to wirelessly connect to one or more GyroPalm Encore wearables without any additional dependencies. This Python package contains three independent classes, `GyroPalmRealtime`, `GyroPalmDriving`, and `GyroPalmRealtimeRobot`, which include methods to enable developers in establishing bi-directional communication with GyroPalm devices for creating unlimited hands-free Python interactions, especially for remotely controlling and monitoring robots. This repository also contains examples that demonstrate typical usage.

### GyroPalmRealtime vs. GyroPalmRealtimeRobot
This library exposes the `GyroPalmRealtime` object, which encapsulates secure websockets (WSS) within our real-time low latency server. Using enhanced methods and function callbacks, gestures, commands, and other data can be retrieved from the wearable in milliseconds. The `GyroPalmRealtime` object is designed to **enable a computer (client machine) to receive gesture commands from a GyroPalm Encore wearable, as well as to send data** to the wearable. This object is wearable-centric, meaning a client machine can instantiate a `GyroPalmRealtime` object for every GyroPalm wearable it needs to receive commands from. In this configuration, the client computer running `GyroPalmRealtime` must first have the user's `apiKey` and `wearableID` to subscribe to the wearable.

Introduced in the `GyroPalm VIMPAACT` project in 2023, the capability for interfacing with multiple industrial robots (Python-based ROS instances) has been added. This raised the need for a more secure configuration where **neither the client computer nor wearable would be initiating the request to bind the connection** with each other. Instead, the connection between wearable and robot would be established by the user scanning a QR code from a 3rd party device such as a pair of Vuzix Blade 2 AR glasses (part of the GyroPalm Spectrum package). In this case, the **binding of said connection between robot machine and GyroPalm wearable is ephemeral** as the binding is cleared when either device decides to withdraw the connection. This form of target based device selection and single-use realtime control can be very effective since the **authentication credentials to pair both devices are not stored on the robot machine nor wearable**. Privacy between wearables and "robot stations" is maintained in a clean manner. In other words, access for any GyroPalm wearable to control any specific robot can be instantly established by a 3rd party device (REST API request) through a revocable `secret` key.

To accomplish this, the `GyroPalmRealtimeRobot` object is designed to **assign a computer (robot machine) a target `robotID` which allows the robot to be globally shared in a secure manner with other control interfaces** such as GyroPalm Encore wearables and web browsers. In this configuration, any device can subscribe to the `robotID` as long as it has a valid `secret` key. Through the GyroPalm Dashboard, the owner of a robot can provision as many `secret` keys as desired, set expiry dates, and track their usage. An end-user can call the GyroPalm bind request through the v2 REST API with their `apiKey`, `wearableID`, `robotID`, and `secret` to establish a binding between their wearable and the target robot.

### When to use GyroPalmRealtimeRobot
For small use-cases or experimental setups where you can hardcode the user's API key and wearableID using `GyroPalmRealtime` into the deployment machine, you do not need to use `GyroPalmRealtimeRobot`. The `GyroPalmRealtime` object is best for end-to-end where one end is always defined - the wearable side. For industrial or enterprise use-cases that require one or more wearables be used to control multiple robots through intelligent device selection, then you will need to instantiate `GyroPalmRealtimeRobot` on every robot machine that you want your wearable(s) to bind to.

### Driving Mobile Robots using GyroPalm Encore
Using the `GyroPalmRealtime` object, developers can write applications that can control ROS-based robots. Furthermore, the `GyroPalmDriving` library provides methods for smooth acceleration/deceleration easing, emergency-stop on signal loss, center-snapping, and constrain/normalization of command velocity values. 

Although the `GyroPalmRealtime` library can be used independently, the `GyroPalmDriving` library is essential in enhancing safety in robotic operation as well as enhancing both the end-user and developer experience.

## Requirements ##
To implement this SDK for its intended use, it is highly recommended that the developer has a GyroPalm Developer Kit or equivalent GyroPalm package to do proper testing. To order one or more wearables, visit the [GyroPalm Online store](https://gyropalm.com/order/).

In addition, the host machine must have Python 3.6 or newer, and the `websockets` library installed. The host machine needs to have an internet connection so that it can connect to the `GyroPalmRealtime` server.

## Installation ##
There are two simple ways to acquire this package: By running a `pip install` command, or downloading the latest release from this GitHub repository.

### Install Package from PyPi ###
To easily install this package from PyPi by running the following:
```shell
sudo pip install gyropalm_control
```

### Install Package from GitHub Repo ###
You can also install this package from GitHub by running the following:
```shell
sudo git clone https://github.com/GyroPalm/GyroPalm-Python-SDK.git
```