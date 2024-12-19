//
// Created by Max Zijlstra on 2023-11-21.

#include <string>
#include <iostream>

class TestConveyor {
    bool physical; // Instance variable to store if the camera is physical or not

public:
    explicit TestConveyor(const bool physical) : physical(physical) {}

    int moveForward() const {
        if (physical) {
            std::cout << "Physical Move Forward" << std::endl;
            //CALL CLASS and Function OF MAIN CODE
            return 1000;
        }
        std::cout << "Virtual Move Forward" << std::endl;
        return 100;
    }

    int moveBackward() const {
        if (physical) {
            std::cout << "Physical MoveBackward" << std::endl;
            //CALL CLASS and Function OF MAIN CODE
            return 2000;
        }
        std::cout << "Virtual MoveBackward" << std::endl;
        return 200;
    }
};