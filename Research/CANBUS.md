# CanBus research

In this document we will describe why we chose CanBus for our project. The protocol is interesting to learn more about. Here you will find the research for it

## Communication Protocols Overview
1. I2C (Inter-Integrated Circuit):

    Reliability: I2C uses a bus arbitration method to handle data collisions, making it fairly reliable. However, it's more susceptible to noise interference compared to other protocols.

    Implementation: I2C is natively supported by both Raspberry Pi and Pico. It requires two wires (SDA for data and SCL for clock) and can connect multiple devices in a master-slave configuration.

2. SPI (Serial Peripheral Interface):

    Reliability: SPI is faster than I2C and is considered reliable due to its full-duplex communication. However, it requires more pins as the number of devices increases.

    Implementation: Both Raspberry Pi and Pico support SPI. It uses a master-slave architecture with separate clock, master input/slave output, and master output/slave input lines.

3. UART (Universal Asynchronous Receiver-Transmitter):

    Reliability: UART is simple and reliable for point-to-point communication. However, it's not ideal for multi-device communication due to its asynchronous nature.

    Implementation: Both Raspberry Pi and Pico have UART pins. It's suitable for direct communication between two devices using transmit (TX) and receive (RX) lines.

## Why CAN bus is the Best Choice
1. Robustness:

CAN bus was designed for noisy environments, like automobiles. Its differential signaling and error-handling capabilities make it exceptionally robust against electrical noise and interference.
2. Multi-device Communication:

Unlike UART, which is primarily for point-to-point communication, CAN bus supports multi-device setups. This is crucial for systems like BlockBuddy, where multiple components need to communicate simultaneously.
3. Error Handling:

CAN bus has built-in error detection and signaling. If a device detects an error in a message, it can flag it, ensuring high data integrity.
4. Efficiency:

With CAN bus, messages are sent with identifiers rather than device addresses. This means the message's importance, not the device's importance, dictates its priority, leading to efficient data transmission.
5. Scalability:

Adding new devices to a CAN bus network is straightforward, making it suitable for projects that might scale in complexity.
6. Community & Support:

Given its widespread use in the automotive and industrial sectors, there's a vast community and a plethora of resources available for CAN bus. This ensures easier troubleshooting and better community support.
Other Considerations
Power Consumption:

CAN bus operates at lower power levels compared to some other protocols, making it suitable for projects where power efficiency is crucial.
Real-time Capabilities:

For systems requiring real-time responses, like BlockBuddy, CAN bus's prioritized message transmission can be a significant advantage.
Cost:

While CAN bus modules might have a slightly higher cost than simple UART or I2C modules, the benefits in terms of reliability, scalability, and robustness often justify the investment.

## Conclusion 

While there are multiple communication protocols available for Raspberry Pi and Pico integration, CAN bus emerges as the frontrunner due to its robustness, efficiency, and scalability. Its design, rooted in the demanding automotive sector, ensures high reliability and efficient multi-device communication. For a system like BlockBuddy, which requires seamless and error-free communication between its components, CAN bus is undoubtedly the optimal choice. We also want to learn to work with canbus for industrial purposes.



# Setup CAN bus on a Raspberry Pi

Implementing CAN bus on a Raspberry Pi involves both hardware and software configurations. Here's a step-by-step guide:

## Hardware Requirements:

    Raspberry Pi: Any model with GPIO pins will work, but this guide assumes Raspberry Pi 3/4.
    MCP2515 CAN bus module with SPI interface: Commonly used with Raspberry Pi.
    OBD-II cable or CAN bus breakout board: For connecting to CAN devices or networks.
    Jumper wires.
    10kΩ resistors: For pull-up on the interrupt line, if needed.

## Hardware Setup:

    Connect the MCP2515 to the Raspberry Pi:
        VCC to 3.3V (Pin 1).
        GND to GND (Pin 6).
        SCK to SPI SCLK (Pin 23).
        SI to SPI MOSI (Pin 19).
        SO to SPI MISO (Pin 21).
        CS to SPI CE0 (Pin 24).
        INT to GPIO25 (Pin 22).
    If you're connecting the Raspberry Pi to a CAN network, ensure that the network has the necessary 120Ω termination resistors at both ends.

## Software Setup:

    Update and Upgrade:

    bash

sudo apt update && sudo apt upgrade

## Install Necessary Packages:

bash

sudo apt install can-utils

## Enable SPI Interface:

    Run sudo raspi-config.
    Navigate to Interfacing Options > SPI and enable it.
    Exit and reboot.

## Load Kernel Modules:

bash

sudo modprobe can
sudo modprobe can-dev
sudo modprobe can-raw
sudo modprobe mcp251x

## Configure CAN Interface:

bash

    sudo ip link set can0 up type can bitrate 500000

    Note: Here, 500000 is the bitrate. Adjust it based on your CAN network's requirements.

    Test the Setup:
        Use candump can0 to listen to messages on the CAN bus.
        Use cansend to send messages. For example: cansend can0 123#1122334455667788.

## Automate on Boot:

To ensure the CAN interface is set up on boot:

    Edit /etc/network/interfaces:

    bash

sudo nano /etc/network/interfaces

## Add the following lines:

bash

    allow-hotplug can0
    iface can0 can static
        bitrate 500000
        up /sbin/ip link set $IFACE down
        up /sbin/ip link set $IFACE up

    Save and exit.

## Conclusion:

This was to set up CAN bus communication on your Raspberry Pi. You can use tools from the can-utils package to send, receive, and analyze CAN messages. For more advanced applications, consider integrating with Python or other programming languages to create custom scripts and applications for your CAN network.


# Here's how you can test sending and receiving messages using can-utils:
1. Setting up the CAN interface:

If you haven't already set up the can0 interface:

bash

sudo ip link set can0 up type can bitrate 500000

This sets up the can0 interface with a bitrate of 500,000 bits per second. Adjust the bitrate as needed.
2. Listening for CAN messages:

Open a terminal and run:

bash

candump can0

This command will listen for messages on the can0 interface and display them as they're received.
3. Sending a CAN message:

Open a second terminal and run:

bash

cansend can0 123#1122334455667788

This sends a message on the can0 interface with an ID of 123 and data 1122334455667788.
4. Verifying the message:

Switch back to the first terminal where you ran candump. You should see the message you sent displayed there, confirming that the message was sent and received successfully.

Note: If you're testing on a single Raspberry Pi without any other devices on the CAN bus, you might not see the sent message in candump. For a more comprehensive test, you'd typically have two devices on the CAN bus: one sending messages and the other receiving them. If you have two Raspberry Pis, you can set up one to send messages and the other to receive them. If you're using just one Raspberry Pi, you can set it up in loopback mode, but remember that this is just for testing and doesn't guarantee communication with other devices.