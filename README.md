# Restaurant POS System

## Introduction

In the summer of 2024, I embarked on a journey to learn Python and set a goal to recreate the POS (Point of Sale) system from the restaurant where I previously worked. After three months of being self-taught in Python, I successfully completed this project. The functionality of the system closely mirrors the original POS system, surpassing my initial expectations.

## Key Features

- User-friendly interface for order entry
- Real-time order total calculation
- Customizable menu options with categories
- Error handling for invalid inputs
- Efficient data handling with lists and dictionaries

## Code Functionality Overview

The restaurant POS system is built using Python's Tkinter library to create a graphical user interface (GUI). The system replicates the functionality of a typical point-of-sale system used in restaurants, allowing for order entry, modification, and summary display. Below is a brief explanation of how the system is structured and functions behind the scenes:

### Main Components

1. **Main Window Initialization**:
   - The `initiate_main_window` function sets up the main window dimensions, background color, title, and position on the screen.

2. **Order Class**:
   - The `Order` class represents an individual customer order.
   - It manages the order name, service type, balance due, and a list of items.
   - Key methods include adding, removing, and modifying items, updating the order display summary, and handling order renaming.

3. **OrderItem Class**:
   - The `OrderItem` class represents individual items within an order.
   - It tracks the item's name, type, sauces, sides, drinks, notes, and total price.
   - Methods handle updating item details, adding notes, and calculating the total price.

4. **ModificationWindow Class**:
   - The `ModificationWindow` class provides a GUI for modifying order items.
   - It allows the user to select sauces, sides, drinks, and add notes.
   - The interface dynamically updates based on the item type and user selections.

5. **Menu Class**:
   - The `Menu` class manages the display of available menu items and categories.
   - It creates and populates frames for different sections of the menu, such as drinks, tender meals, sandwiches, salads, kids' meals, sides, and sauces.
   - It handles user navigation to modify order items.

### Workflow

1. **Initialization**:
   - The main window is initialized using `initiate_main_window`.
   - An instance of the `Order` class is created, which in turn initializes the menu and creates the order summary frame.

2. **Order Management**:
   - Users can add items to the order from the menu. Each item added is an instance of the `OrderItem` class.
   - Items can be modified through the `ModificationWindow`, which provides options based on the item type.
   - The order summary is dynamically updated to reflect changes, including item additions, modifications, and removals.

3. **GUI Interaction**:
   - The Tkinter library manages user interactions, such as button clicks and form entries.
   - The interface updates in real-time, providing a seamless user experience.

### Future Enhancements

The system is designed to be extendable, with plans to add features such as discount application, multi-order management, and a more comprehensive payment screen interface.

This overview provides a high-level understanding of the POS system's structure and functionality, highlighting the interaction between different classes and methods to deliver a cohesive user experience.
