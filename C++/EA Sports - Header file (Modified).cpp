#ifndef GAMEOBJECTS_H
#define GAMEOBJECTS_H

#include <string>
#include <vector>
#include <unordered_map>  // For optimized item management in Inventory
#include <stdexcept>      // For exception handling

// Forward declarations
class Event;
class Memory;
class Sim;
class SocialRelationship;
class Emotion;

// Abstract Base Class for Expansion Packs
class ExpansionPack {
public:
    virtual void install() = 0; // Pure virtual function for installation
};

// Derived class from ExpansionPack
class DynamicMemoriesExpansion : public ExpansionPack {
public:
    void install() override; // Implement install function
    void activate();
    void deactivate();
    void recordMemory(const Event& event);
};

// Game class that handles saving and loading
class Sims4Game {
public:
    void loadSave(const std::string& savedGame);
    std::string saveGame() const;
};

// Sim Class representing a character in the game
class Sim {
private:
    std::string name;
    int age;
    std::string career;
    std::vector<Memory> memories; // Stores memories of the Sim

public:
    Sim(const std::string& name, int age, const std::string& career);

    // Getters and Setters
    std::string getName() const;
    int getAge() const;
    std::string getCareer() const;
    void addMemory(const Memory& memory);

    // Sim interactions
    void experienceLifeEvent(const Event& event);
    void interactWith(Sim& otherSim);
};

// Memory Class representing a memory in the game
class Memory {
private:
    Event event;
    std::string emotionEffect;
    int duration;

public:
    Memory(const Event& event, const std::string& emotionEffect, int duration);

    // Getters for memory data
    const Event& getEvent() const;
    std::string getEmotionEffect() const;
    int getDuration() const;
};

// Event Class representing an event in the game
class Event {
private:
    std::string type;
    std::string description;

public:
    Event(const std::string& type, const std::string& description);

    // Getters for event data
    std::string getType() const;
    std::string getDescription() const;
};

// SocialRelationship Class to model the relationship between two Sims
class SocialRelationship {
private:
    Sim& sim1;
    Sim& sim2;
    std::string status;
    std::vector<Memory> sharedMemories;

public:
    SocialRelationship(Sim& sim1, Sim& sim2, const std::string& status);

    // Getters and Setters
    std::string getStatus() const;
    void addSharedMemory(const Memory& memory);
};

// Emotion Class representing an emotional effect
class Emotion {
private:
    std::string type;
    int intensity;
    int duration;

public:
    Emotion(const std::string& type, int intensity, int duration);

    // Getters
    std::string getType() const;
    int getIntensity() const;
    int getDuration() const;
};

// New Inventory Class
class Inventory {
private:
    // Using unordered_map to hold items with string keys for quick lookup and deletion
    std::unordered_map<std::string, int> items; // Map of item name and quantity

public:
    Inventory();

    // Add an item to the inventory
    void add_item(const std::string& itemName, int quantity);

    // Remove an item from the inventory
    void remove_item(const std::string& itemName);

    // Get the quantity of an item
    int get_item_quantity(const std::string& itemName) const;

    // Check if an item exists in the inventory
    bool has_item(const std::string& itemName) const;
};

// Implementation of Inventory methods

inline Inventory::Inventory() {}

inline void Inventory::add_item(const std::string& itemName, int quantity) {
    items[itemName] += quantity;  // Adds the quantity to the item if it exists
}

inline void Inventory::remove_item(const std::string& itemName) {
    auto it = items.find(itemName);
    if (it != items.end()) {
        items.erase(it); // Removes the item from the map if it exists
    } else {
        throw std::invalid_argument("Item not found in inventory.");
    }
}

inline int Inventory::get_item_quantity(const std::string& itemName) const {
    auto it = items.find(itemName);
    if (it != items.end()) {
        return it->second;
    } else {
        return 0; // Item not found, return 0 quantity
    }
}

inline bool Inventory::has_item(const std::string& itemName) const {
    return items.find(itemName) != items.end();
}

#endif // GAMEOBJECTS_H
