# GyroPalm Python SDK
Python SDK for GyroPalm Developers

## Overview ##
The GyroPalm Python software development kit (SDK) enables developers to wirelessly connect to one or more GyroPalm Encore wearables without any additional dependencies. This Python package contains two independent classes, `GyroPalmRealtime` and `GyroPalmDriving`, which include methods to enable developers in establishing bi-directional communication with GyroPalm devices for creating unlimited hands-free Python interactions, especially for remotely controlling and monitoring robots. This repository also contains examples that demonstrate typical use.

This library exposes the `GyroPalmRealtime` object, which encapsulates secure websockets (WSS) with our real-time low latency server. Using enhanced methods and function callbacks, gestures, commands, and other data can be retrieved from the wearable in milliseconds. Using the `GyroPalmRealtime` object, developers can write applications that can control ROS-based robots. Furthermore, the `GyroPalmDriving` library provides methods for smooth acceleration/deceleration easing, emergency-stop on signal loss, center-snapping, and constrain/normalization of command velocity values. 

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