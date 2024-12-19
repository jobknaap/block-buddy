/*
@purpose This C++ code sets up a raw CAN socket on the Raspberry Pi. This code is focused on demonstrating how to set up a CAN socket in C++. 
@author Max Zijlstra
@date 22 sep 2023
*/

#include <iostream>
#include <string>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <unistd.h>
#include <cstring>

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

    std::cout << "CAN interface " << interface_name << " set up successfully!" << std::endl;

    close(s);
    return 0;
}
