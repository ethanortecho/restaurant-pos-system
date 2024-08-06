
#other notes
#need to double check menu prices
#specifically the drink items, smartwater, lacroix
#ensure all sauces, including redundent ones are in all sauce choice

#need to handle dressing present on 1/2 Salad meal sides

#



# THINGS TO REMEMBER DURING TRANSITION


# - every input() is the equivalent of a button press - input error handling will not be necessary

# all mapping dictionaries eventually will not be needed with the integration of Buttons




# TO DO TOMORROW

# - figure out logic to add and remove items, or modify orders

#ItemOrder object logic
# - pricing logic for sides, sauces, and drinks depending on the meal type
# - create __Str__ function
# - might need to create method for dealing with individual tenders
# -

#


















class Order:
    def __init__(self):

        self.items = []

        self.menu = Menu(self)
        # initializes list of order items

    def add_item(self, order_item):
        self.items.append(order_item)


    def display_order_summary(self):
        running_total = 0
        for order in self.items:
            print_line()
            print(order)
            print_line()
            running_total += order.total_price
        print(f'\nrunning total: {running_total}')



class OrderItem:
    def __init__(self, item_name, base_price, order, item_type =None, window=None):
        self.window = window

        self.item_type = item_type

        self.item_name = item_name

        self.base_price = base_price

        self.total_price = base_price


        #saves a reference to current order, to send itself to add_item
        self.order = order
        self.order.add_item(self)

        self.sauces = []
        self.side = {}
        self.drink = {}
        self.extra_sauces = []

    def add_sauce(self, sauce, price):
        if sauce == "Hot Honey":
            price = price
        else:
            price = 0

        self.sauces.append({'sauce': sauce, 'price': price})

        self.total_price += price

    def add_sides(self, side, price):
        #check for redundent code later on


        #handles side logic for tender meals
        if self.item_type == 'Tender meal':
            if side == '1/2 Salad':
                price = 1.49

            else:
                price = 0

            self.side = {'side': side, 'price': price}





        elif self.item_type == 'Sandwich meal':

            if side == '1/2 Salad':
                price = 1.49
            else:
                price = 0
            self.side = {'side': side, 'price': price}


        elif self.item_type == 'Kids meal':
            price = 0
            self.side = {'side': side, 'price': price}


        else:
            self.side = {'side': side, 'price': price}


        self.total_price += price





    def add_drink(self, drink, price):

        if self.item_type == 'Kids meal':
            price = 0
        else:

            price = 1.00

        self.total_price += price


        self.drink = {'drink': drink, 'price':price}








    def add_tenders(self):
        ...

    def __str__(self):
        result = f'{self.item_name}   {self.base_price}\n'

        if self.sauces:
            result += '\n'

            for sauce in self.sauces:
                result+= f'{sauce['sauce']}  {sauce['price']}'
        if self.side:
            result += '\n'
            result += f'{self.side['side']}   {self.side['price']} '

        if self.drink:
            result += '\n'
            result+= f'{self.drink['drink']}  {self.drink['price']}'

        result+= f'\n\ntotal price   {self.total_price}'

        return result




class Menu:
    def __init__(self, order):
        #a lot of code in this function, but again eventually none of the mapping dictionaries will be necessary
        self.order = order





        self.menu = {"Snack Pack": 8.99, "Medium Pack": 10.99, "Large Pack": 12.99, "Mega Pack": 14.99,
        "Kids 2 Tenders": 6.99, "Kids Sandwich": 6.99, "Kid- Milk": 2.69, 'Kid- Juice Pouch':2.69,
        "Citybird Sandwich": 9.99, "Lemon Thyme Sandwich": 9.99, "Spicy Sandwich": 9.99, "Buffalo Bleu Sandwich": 9.99,
        "Citybird Sandwich - Only" : 7.49, "Lemon Thyme Sandwich - Only": 7.49, "Spicy Sandwich - Only": 7.49, "Buffalo Bleu Sandwich - Only": 7.49,
        "Salad": 7.99, 'Add 3 Tenders' : 4.00,
        "Fries": 2.49, "Slaw": 1.99, "1/2 Salad": 3.49, "Apple Sauce": 1.49, "Pickles": .75, "Bun": 1, 'Kids Fries': 2.49,
        }
        self.sauce_menu = {"City Sauce": .75, "Lemon Thyme Ranch": .75, "Honey Dijon": .75, "Buffalo Bleu": .75,
                      "Hickory BBQ": .75, "Spicy Mayo": .75, "Hot Honey": 1, "Citybird Vinaigrette":.75,
                      "5oz City Sauce": 5, "5oz Lemon Thyme Ranch": 5, "5oz Honey Dijon": 5, "5oz Buffalo Bleu": 5,
                      "5oz Hickory BBQ": 5, "5oz Spicy Mayo": 5, "5oz Hot Honey": 5}

        self.drink_menu = {"Fountain Drink": 2.69, "Bottle Water": 2.69, "Juice & Wikki Stix": 2.69,
                      "Milk & Wikki Stix": 2.69, "Lacroix": 2.69, "Milk": 2.69, "Kid- Juice Pouch": 2.69}



        self.menu_mapping = {
            "1": self.add_drink_display,"2": self.tender_meals_display,"3": self.sandwich_meals_display,"4": self.salad_display,
            "5": self.kids_meals_display,"6": self.add_side_display, "7": self.scratch_sauces_display,"8": self.sandwich_only_display
        }
        self.drink_mapping = {"1": "Fountain Drink", "2": "Lacroix","3": "Bottle Water", "4": "Juice & Wikki Stix", '5': "Milk & Wikki Stix"}

        self.kids_drink_mapping = {"1": "Milk", "2": "Kid- Juice Pouch", "3": "Fountain Drink"}


        self.side_mapping = {"1": "1/2 Salad", "2": "Apple Sauce",   "3": "Bun",
                          "4": "Fries", "5": "Pickles", "6": "Slaw", '7': 'On Side Tenders'}

        self.meal_side_mapping = {"1": "Fries",
                        "2": "Slaw",
                        "3": "1/2 Salad",
                        "4": "1/2 Salad",
                        "5": "1/2 Salad",
                        }

        self.kids_side_mapping = {'1':'Kids Fries', '2':'Apple Sauce'}

        self.sauce_mapping = {
            "1": "City Sauce", "2": "Lemon Thyme Ranch", "3": "Honey Dijon", "4": "Buffalo Bleu",
            "5": "Hot Honey", "6": "Hickory BBQ", "7": "Spicy Mayo"
        }
        self.sauce_size_mapping = {
            "1": "1oz", "2": "5oz Sauce"
        }

        self.tender_meal_mapping = {
            "1": "Snack Pack", "2": "Medium Pack", "3": "Large Pack", "4": "Mega Pack", "5": "On Side Tenders"
        }
        self.tender_mapping = {"1": "1 Pieces",
                          "2": "2 Pieces",
                          "3": "3 Pieces",
                          "4": "4 Pieces",
                          "5": "5 Pieces",
                          "6": "6 Pieces",
                          "7": "7 Pieces",
                          "8": "8 Pieces",
                          "9": "9 Pieces"
                          }

        self.sandwich_mapping = {
            "1": "Buffalo Bleu Sandwich", "2": "Citybird Sandwich", "3": "Lemon Thyme Sandwich", "4": "Spicy Sandwich"
        }
        self.sandwich_only_mapping = {"1": "Buffalo Bleu Sandwich - Only", "2": "Citybird Sandwich - Only", "3": "Lemon Thyme Sandwich - Only", "4": "Spicy Sandwich - Only"}

        self.kids_meal_mapping = {
            "1": "Kids 2 Tenders", "2": "Kids Sandwich", "3": "Kid- Juice Pouch", "4": "Kid- Milk",
            "5": "Apple Sauce", "6": "Pickles"
        }
        self.dressing_mapping = {'1': 'Lemon Thyme Ranch', '2': 'Citybird Vinaigrette', '3': 'Honey Dijon'}

        self.main_menu_display()





    def main_menu_display(self):
        # display and gui interaction

        self.order.display_order_summary()

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


    def salad_display(self):
        SaladMealWindow(self)
    def add_drink_display(self):

        print_line()
        print("DRINK MENU")
        print_line()
        print(
            "1. Fountain Drink\n"
            "2. Lacroix\n"
            "3. Smartwater\n"
        )
        print_line()

        drink = self.drink_mapping[input("Choose Drink 1-3: ")]
        price = self.drink_menu[drink]
        OrderItem(drink, price, self.order)

        #redirects to main menu after adding item to order
        self.main_menu_display()



    def add_side_display(self):
        # apart of main menu window
        print("\n")
        print_line()
        print("1. (1/2) Salad\n"
              "2. Apple Sauce\n"
              "3. Bun\n"
              "4. Fries\n"
              "5. Pickles\n"
              "6. Slaw\n"
              '7. On Side Tenders'
              )
        print_line()

        side = self.side_mapping[input("Choose side 1-6: ")]


        if side == '1/2 Salad':
            HalfSaladWindow(self)

        elif side == 'On Side Tenders':
            IndividualTenders(self)

        else:
            price = self.menu[side]
            order_item = OrderItem(side, price, self.order)

            # redirects to main menu after adding item to order
            self.main_menu_display()



    def scratch_sauces_display(self):

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





    def tender_meals_display(self):
        # would be in main menu window

        print_line()
        print("TENDER MENU")
        print_line()
        print("1. Snack Pack\n"
              "2. Medium Pack\n"
              "3. Large Pack\n"
              "4. Mega Pack\n"
              "5. On Side Tenders"
              )
        print_line()
        size = self.tender_meal_mapping[input("Which Tender Meal 1-5: ")]

        if size == 'On Side Tenders':
            IndividualTenders(self)

        else:
            TenderMealWindow(self, size)









    def sandwich_meals_display(self):
        # will be in main menu
        print("\n" * 1)
        print_line()
        print("TENDER SANDWICH MENU")
        print_line()

        print("1. Buffalo Bleu Sandwich\n"
              "2. Citybird Sandwich\n"
              "3. Lemon Thyme Sandwich\n"
              "4. Spicy Sandwich")
        print_line()

        SandwichMealWindow(self,self.sandwich_mapping[input("Which sandwich 1-4: ")])





    def sandwich_only_display(self):
        # in main menu window
        print('\n')
        print_line()
        print("SANDWICH ONLY")
        print_line()
        print("1. Buffalo Bleu - Sandwich Only\n"
              "2. Citybird Sandwich - Sandwich Only\n"
              "3. Lemon Thyme - Sandwich Only\n"
              "4. Spicy - Sandwich Only")
        print_line()
        item = self.sandwich_mapping[input("Which Sandwich 1-4: ")]
        price = self.menu[item]
        OrderItem(item,price,self.order)

        # redirects to main menu after adding item to order
        self.main_menu_display()




    def kids_meals_display(self):
        # within Main Menu function
        print("\n")
        print_line()
        print("KIDS MEAL MENU")
        print_line()

        print("1. Kids 2 Tenders\n"
              "2. Kids sandwich\n"
              "3. Kid- Juice Pouch\n"
              "4. Kid- Milk\n"
              "5. Apple Sauce\n"
              "6. Pickles")
        print_line()

        item = self.kids_meal_mapping[input("Which Meal 1-6: ")]

        if item in ["Kids 2 Tenders", "Kids Sandwich"]:

            KidsMealWindow(self, item)

        else:
            price = self.menu[item]
            OrderItem(item, price, self.order)

            # redirects to main menu after adding item to order
            self.main_menu_display()










class ScratchSauceWindow:

    def __init__(self, menu, sauce):

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





        elif self.sauce_size == "2":
            self.sauce = f"5oz {self.sauce}"
            self.item_price = self.menu.sauce_menu[self.sauce]


        #creates an instance of order_item and sends sauce and item to it
        self.order_item = OrderItem(self.sauce, self.item_price, self.menu.order)

        # redirects to main menu after adding item to order
        self.menu.main_menu_display()














class TenderMealWindow:
    #eventually with GUI, a button would auto append a specific item to order along with price
    #eliminating the need for any item mapping

    #display functions should only display contents, and have input
    #they will eventually be a GUI with buttons, and the buttons won't be doing logic

    def __init__(self, menu, size):

        self.menu = menu

        self.item_name = size #sets the item name to the pack size - ex item_name = 'snack pack'

        self.item_price = self.menu.menu[self.item_name] #sets the item price to the price of item_name in dictionary



        #creates OrderItem object, sends item name and base price
        self.order_item = OrderItem(self.item_name, self.item_price, self.menu, 'Tender meal', self)

        self.get_sauce_display_1()




    def get_sauce_display_1(self):
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

        #eventually won't be necessary
        sauce = self.menu.sauce_mapping[(input("Choose a sauce 1-7: "))]

        #sends first sauce choice to OrderItem object
        self.order_item.add_sauce(sauce, self.menu.sauce_menu[sauce])


        #only way I can prompt for a second sauce depending on pack, later this will be handled
        #in the initialization of the GUI
        if self.item_name in ("Large Pack", "Mega Pack"):
            self.get_sauce_choice_display_2()

        else:
            self.tender_meal_sides_display()

    def get_sauce_choice_display_2(self):
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
        sauce = self.menu.sauce_mapping[input("Choose a sauce 1-7: ")]
        price = self.menu.sauce_menu[sauce]

        self.order_item.add_sauce(sauce, price)

        self.tender_meal_sides_display()

    def tender_meal_sides_display(self):
        print("\n" * 1)
        print_line()
        print("With Fries?")
        print_line()
        print("1. Fries\n"
              "2. City Slaw\n"
              "3. 1/2 Salad (Honey Dijon)\n"
              "4. 1/2 Salad (Ranch)\n"
              "5. 1/2 Salad (Vinaigrette)"
              )
        print_line()
        side = self.menu.meal_side_mapping[input("Choose side 1-5: ")]
        price = self.menu.menu[side]

        self.order_item.add_sides(side, price)

        self.tender_meal_drink_display()


    def tender_meal_drink_display(self):
        print("\n")
        print_line()
        print("Drink Choice?")
        print_line()
        print("1. Fountain Drink\n"
              "2. Lacroix\n"
              "3. Bottle Water\n"
              "4. Juice & Wikki Stix\n"
              "5. Milk & Wikki Stix\n"

              )
        print_line()

        drink = self.menu.drink_mapping[input("Choose Drink 1-5: ")]

        price = self.menu.drink_menu[drink]

        self.order_item.add_drink(drink, price)

        self.order_item.modify()

        self.menu.main_menu_display()











class SandwichMealWindow:
    def __init__(self, menu, item_name):

        self.menu = menu

        #Name of each item will be encoded into its respective button in main menu, and passed as item_name
        self.item_name = item_name

        self.item_price = self.menu.menu[self.item_name]

        self.order_item = OrderItem(self.item_name, self.item_price, self.menu.order, 'Sandwich meal')

        self.sandwich_meal_sides_display()




    def sandwich_meal_sides_display(self):
        print("\n" * 1)
        print_line()
        print("With Fries?")
        print_line()
        print("1. Fries\n"
              "2. City Slaw\n"
              "3. 1/2 Salad (Honey Dijon)\n"
              "4. 1/2 Salad (Ranch)\n"
              "5. 1/2 Salad (Vinaigrette)"
              )
        print_line()

        side = self.menu.meal_side_mapping[input("Choose side 1-5: ")]
        price = self.menu.menu[side]

        self.order_item.add_sides(side, price)

        self.sandwich_meal_drink_display()







    def sandwich_meal_drink_display(self):
        print("\n")
        print_line()
        print("DRINK Choice?")
        print_line()
        print("1. Fountain Drink\n"
              "2. Bottle Water\n"
              "3. Juice & Wikki Stix\n"
              "4. Milk & Wikki Stix\n"
              "5. Lacroix\n"
              )

        drink = self.menu.drink_mapping[input("Choose Drink 1-5: ")]

        price = self.menu.drink_menu[drink]

        self.order_item.add_drink(drink, price)

        #redirects to main menu
        self.menu.main_menu_display()






class SaladMealWindow:

    def __init__(self, menu):

        self.menu = menu

        self.item_name = "Salad"

        self.item_price = self.menu.menu[self.item_name]

        self.order_item = OrderItem(self.item_name, self.item_price, self.menu.order)

        self.add_3_tenders_display()


    def add_3_tenders_display(self):
        self.answer_mapping = {'1': 'Add 3 Tenders', '2': None}
        print_line()
        print("Add 3 Tenders?")
        print("1. Add 3 Tenders")
        print("2. No Tenders")
        print_line()

        response = self.answer_mapping[input("Choose 1-2:")]
        print(response)
        if response:
            self.order_item.add_sides(response, self.menu.menu[response])

        self.get_dressing_choice_display()


    def get_dressing_choice_display(self):
        # will likely exist as a function in the eventual salad_meal_window class
        for i in range(2):
            print("\n" * 1)
            print_line()
            print("DRESSING CHOICE")
            print_line()
            print("1. Lemon Thyme Ranch\n2. Citybird Vinaigrette\n3. Honey Dijon")
            print_line()

            dressing = self.menu.dressing_mapping[input("Choose a Dressing 1-3: ")]

            price = self.menu.sauce_menu[dressing]

            self.order_item.add_sauce(dressing, price)

            # redirects to main menu
            self.menu.main_menu_display()












class HalfSaladWindow:

    def __init__(self, menu):
        self.menu = menu

        self.item_name = '1/2 Salad'

        self.item_price = self.menu.menu[self.item_name]

        self.order_item = OrderItem(self.item_name, self.item_price, self.menu.order)

        self.get_dressing_choice_display()


    def get_dressing_choice_display(self):
        # will likely exist as a function in the eventual salad_meal_window class
        print("\n" * 1)
        print_line()
        print("DRESSING CHOICE")
        print_line()
        print("1. Lemon Thyme Ranch\n2. Citybird Vinaigrette\n3. Honey Dijon")
        print_line()

        dressing = self.menu.dressing_mapping[input("Choose a Dressing 1-3: ")]

        price = self.menu.sauce_menu[dressing]

        self.order_item.add_sauce(dressing, price)

        # redirects to main menu
        self.menu.main_menu_display()


    def add_tender(self):
        ...




class KidsMealWindow:

    def __init__(self, menu, item_name):

        self.menu = menu

        self.item_name = item_name

        self.item_price = self.menu.menu[self.item_name]

        self.order_item = OrderItem(self.item_name, self.item_price, self.menu.order, 'Kids meal')

        self.kids_sides_display()


    def kids_sides_display(self):
        print("\n" * 1)
        print_line()
        print("Kids Side Choice")
        print_line()
        print("1. Kids Fries\n"
              "2. Apple Sauce\n"
              )
        print_line()

        side = self.menu.kids_side_mapping[input("Choose side 1-2: ")]

        price = self.menu.menu[side]

        self.order_item.add_sides(side, price)

        self.kids_drink_display()


    def kids_drink_display(self):
        print("\n")
        print_line()
        print("KIDS DRINK MENU")
        print_line()
        print("1. Milk\n2. Juice Box\n3. Fountain Drink")
        print_line()

        drink = self.menu.kids_drink_mapping[input("Choose Drink 1-3: ")]

        price = self.menu.drink_menu[drink]

        self.order_item.add_drink(drink, price)

        # redirects to main menu
        self.menu.main_menu_display()



class IndividualTenders:
    def __init__(self, menu):

        self.menu = menu
        self.item_name = 'On Side Tenders'

        self.order_item = OrderItem(self.item_name, 0, self.menu.order)

        self.get_tender_amount_display()


    def get_tender_amount_display(self):
        print("\n" * 1)
        print_line()
        print("Add Tenders")
        print_line()
        print("1. 1 Tenders\n"
              "2. 2 Tenders\n"
              "3. 3 Tenders\n"
              "4. 4 Tenders\n"
              "5. 5 Tenders\n"
              "6. 6 Tenders\n"
              "7. 7 Tenders\n"
              "8. 8 Tenders\n"
              "9. 9 Tenders\n")
        print_line()

        #1.could send tenders individually to order_item, then handle price logic there

        #2.or send number amount along with price of combined tenders
        tender_amount = input("How many Tenders? 1-8: ")

        price = int(tender_amount)

        name = self.menu.tender_mapping[tender_amount]

        self.order_item.add_sides(name, price)
        print(self.order_item)
        # redirects to main menu
        self.menu.main_menu_display()













def print_line():
    print("=" * 40)


Order()