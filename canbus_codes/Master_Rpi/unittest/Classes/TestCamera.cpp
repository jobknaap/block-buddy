//
// Created by Max Zijlstra on 2023-11-21.#include <string>
#include <string>
#include <iostream>

class TestCamera {
    bool physical; // Instance variable to store if the camera is physical or not

public:
    explicit TestCamera(const bool physical) : physical(physical) {}

    int takePicture() const {
        if (physical) {
            std::cout << "Physical Camera picture SUCCESS" << std::endl;
            //CALL CLASS and Function OF MAIN CODE
            return 1000;
        }
        std::cout << "Virtual Camera picture SUCCESS" << std::endl;
        return 100;
    }

    int processPicture() const {
        if (physical) {
            std::cout << "Physical Process Picture DONE" << std::endl;
            //CALL CLASS and Function OF MAIN CODE
            return 2000;
        }
        std::cout << "Virtual test image processed SUCCESS" << std::endl;
        return 200;
    }
};