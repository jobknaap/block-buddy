/*
@purpose This C++ code acts as a main hub for the canbus. The code listens and has sending threads.
@author Max Zijlstra
@date 22 sep 2023
*/


#include <iostream>
#include <string>
#include <cstring>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <unistd.h>
#include <thread>
#include <chrono>

void send_can_messages(int s) {
    struct can_frame frame;
    frame.can_id = 0x123;
    frame.can_dlc = 8;
    frame.data[0] = 0x11;
    frame.data[1] = 0x22;
    frame.data[2] = 0x33;
    frame.data[3] = 0x44;
    frame.data[4] = 0x55;
    frame.data[5] = 0x66;
    frame.data[6] = 0x77;
    frame.data[7] = 0x88;

    while (true) {
        if (write(s, &frame, sizeof(struct can_frame)) != sizeof(struct can_frame)) {
            std::cerr << "Error while sending CAN message" << std::endl;
        } else {
            std::cout << "Sent message with ID: " << frame.can_id << std::endl;
        }
        std::this_thread::sleep_for(std::chrono::seconds(5));  // Send every 5 seconds
    }
}

int main() {
    int s;
    struct sockaddr_can addr;
    struct ifreq ifr;

    // Create a socket for CAN interface
    s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if (s < 0) {
        std::cerr << "Error while opening socket" << std::endl;
        return -1;
    }

    // Name of the CAN interface (e.g., "can0")
    std::string interface_name = "can0";
    strcpy(ifr.ifr_name, interface_name.c_str());
    ioctl(s, SIOCGIFINDEX, &ifr);

    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    // Bind the socket to the CAN interface
    if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        std::cerr << "Error in socket bind" << std::endl;
        return -2;
    }

    // Start a thread to send CAN messages
    std::thread sender_thread(send_can_messages, s);

    // Listen for incoming messages
    struct can_frame frame;
    std::cout << "Listening for CAN messages on " << interface_name << "..." << std::endl;
    while (true) {
        int nbytes = read(s, &frame, sizeof(struct can_frame));
        if (nbytes > 0) {
            std::cout << "Received message with ID: " << frame.can_id << " Data: ";
            for (int i = 0; i < frame.can_dlc; i++) {
                std::cout << std::hex << static_cast<int>(frame.data[i]) << " ";
            }
            std::cout << std::endl;
        }
    }

    sender_thread.join();
    close(s);
    return 0;
}
