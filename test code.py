class Order:
    def __init__(self):
        self.items = []

        self.menu = Menu(self)
        # initializes list of order items

    def add_item(self, order_item):
        self.items.append(order_item)
        for item in self.items:
            print(item)

class OrderItem:
    def __init__(self, item_name, base_price, order):
        self.item_name = item_name
        self.base_price = base_price
        self.order = order
        self.sauces = []
        self.side = None
        self.drink = None

        self.order.add_item(self)

    def add_sauce(self, sauce, price):
        self.sauces.append(sauce, price)

    def add_sides(self, side, price):
        ...

    def add_drink(self, drink, price):
        ...

class Menu:
    def __init__(self, order):
        #a lot of code in this function, but again eventually none of the mapping dictionaries will be necessary
        self.order = order

        self.menu_mapping = {
             "7": self.scratch_sauces_display
        }

        self.sauce_mapping = {
            "1": "City Sauce", "2": "Lemon Thyme Ranch", "3": "Honey Dijon", "4": "Buffalo Bleu",
            "5": "Hot Honey", "6": "Hickory BBQ", "7": "Spicy Mayo"
        }

        self.sauce_menu = {"City Sauce": .75, "Lemon Thyme Ranch": .75, "Honey Dijon": .75, "Buffalo Bleu": .75,
                           "Hickory BBQ": .75, "Spicy Mayo": .75, "Hot Honey": 1,
                           "5oz City Sauce": 5, "5oz Lemon Thyme Ranch": 5, "5oz Honey Dijon": 5, "5oz Buffalo Bleu": 5,
                           "5oz Hickory BBQ": 5, "5oz Spicy Mayo": 5, "5oz Hot Honey": 5}

        self.sauce_size_mapping = {
            "1": "1oz", "2": "5oz Sauce"
        }
        self.main_menu_display()

    def main_menu_display(self):
        # display and gui interaction
        print("\n" * 3)
        print_line()
        print("MAIN MENU")
        print_line()
        print("1. Drink Menu\n"
              "2. Tender Meals\n"
              "3. Tender sandwich Meals\n"
              "4. Salad\n"
              "5. Kids Menu\n"
              "6. Sides\n"
              "7. Sauces\n"
              "8. sandwich Only"
              )
        print_line()
        # this would be a button interaction

        self.menu_mapping[input("Where to?: ")]()

    def scratch_sauces_display(self):
        # in main menu window
        # need to add vinaigrette option

        print("\n" * 1)
        print_line()
        print("SAUCE MENU")
        print_line()
        print(
            "1. City Sauce\n"
            "2. Lemon Thyme Ranch\n"
            "3. Honey Dijon\n"
            "4. Buffalo Bleu\n"
            "5. Hot Honey(+$1)\n"
            "6. Hickory BBQ\n"
            "7. Spicy Mayo"
        )
        print_line()

        ScratchSauceWindow(self, self.sauce_mapping[input("Choose Sauce: ")])

class ScratchSauceWindow:
    def __init__(self, menu,sauce):

        self.menu = menu
        self.sauce = sauce
        self.sauce_size_selection_window()
    def sauce_size_selection_window(self):
            # this would be a Tkinter window that opens after a sauce is pressed in main menu
            print_line()
            print(f"1. {self.sauce} 1oz")
            print(f"2. Catering {self.sauce} 5oz ")
            print_line()

            self.sauce_size = input("Size: ")

            self.sauce_size_selection_window_logic()

    def sauce_size_selection_window_logic(self):
        if self.sauce_size == "1":

            self.item_price = self.menu.sauce_menu[self.sauce]





        elif sauce_size == "2":
            self.sauce = f"5oz {self.sauce}"
            self.item_price = self.menu.sauce_menu[f"5oz {self.sauce}"]


        #creates an instance of order_item and sends sauce and item to it
        OrderItem(self.sauce, self.item_price, self.menu.order)

def print_line():
    print("=" * 40)
Order()