//
// Purpose: Create test-scenarios with a combination of phisical and virtual functions to test parts of the system.
// Created by Max Zijlstra on 2023-11-21.
//

#include "UnitTest.h"
#include <iostream>
#include <string>
using namespace std;

#include "Classes/TestCamera.cpp"
#include "Classes/TestConveyor.cpp"

const std::vector<std::string> CLASS_NAMES = {"Camera", "Conveyor", "StorageWheel", "DB", "Touchscreen", "Canbus"};

const std::vector<std::string> scenarios = {
    "takePicureConveyor",
    // Add other scenario names here
};

class UnitTestScenario {

    TestCamera test_camera;
    TestConveyor test_conveyor;

public:
    //Flags are set in main. The constructor sets what code will be executed (physical or virtual).
    explicit UnitTestScenario(const std::vector<bool>& physicalFlags) :
    test_camera(physicalFlags[0]), //Physical Flag will have effect in Class code of Camera (real or virtual is then activated)
    test_conveyor(physicalFlags[1])
    {}

    void takePicureConveyor() const { //This is a scenario you can fill in
        int result = 0; // This is a result for what a function returns. Usualy this is used in the next function.
        int result2 = 0;
        int result3 = 0;
        int result4 = 0;
        result = test_conveyor.moveForward(); // This activates the function
        result2 = test_camera.takePicture();
        result3 = test_camera.processPicture();
        result4 = test_conveyor.moveForward();

    }
    void FILL_IN_SCENARIO() const { //EXAMPLE SCENARIO
        int result3 = 0;
        int result4 = 0;
        result3 = test_camera.processPicture();
        result4 = test_conveyor.moveBackward();
    }
};

std::vector<bool> setGetPhysicalParts(const std::vector<std::string>& classNames) {
    std::vector<bool> physicalFlags;
    physicalFlags.reserve(classNames.size());

    std::cout << "(t for true, Enter for false)" << "\n";
    for (const auto& className : classNames) {
        std::string input;
        std::cout << className << " physical: ";
        std::getline(std::cin, input);
        physicalFlags.push_back(input == "t" || input == "T");
    }
    return physicalFlags;
}

int getScenarioChoice(const std::vector<std::string>& scenarios) {
    std::cout << "Select a scenario:" << std::endl;
    for (size_t i = 0; i < scenarios.size(); ++i) {
        std::cout << i
        << ". " << scenarios[i] << std::endl;
    }

    std::cout << "Enter choice: ";
    std::string input;
    std::getline(std::cin, input);
    int choice = std::stoi(input);  // Convert string to int
    return choice;  // Adjust for 0-based index
}

int main() {
    UnitTestScenario scenario(   setGetPhysicalParts(CLASS_NAMES)   ); //Asks in terminal for testing class physically

    int selectedScenarioIndex = getScenarioChoice(scenarios); // Ask in terminal what scenario you want to test
    switch (selectedScenarioIndex) {
        case (0):
            scenario.takePicureConveyor();
        default: ;
    }
    return 0;
}

