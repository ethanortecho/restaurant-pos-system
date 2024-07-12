
###what needs attention###
#The order summary frame logic works, but its structure is all over the place. Need to find a way to consolidate it.



import sys
from tkinter import *
import tkinter.font as tkFont


#to do for later-
#update all non window menu items to work like the fountain drink



def initiate_main_window(root):
    width = 1920  # Width of the monitor
    height = 1080  # Height of the monitor
    x_offset = 1920  # Start at the right edge of the primary monitor
    y_offset = 0  # Start at the top of the screen
    root.configure(bg="black")
    root.title("CityBird POS System")
    root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

class Order:
    def __init__(self, root):
        self.root = root
        self.item_summary_buttons = []


        self.balance_due = 0.00

        self.items = []
        # initializes list of order items

        self.menu = Menu(self, root)

        self.create_order_summary_frame()





    def add_item(self, order_item):
        self.items.append(order_item)
        self.update_order_display_summary()


    def remove_item(self, order_item):
        if order_item in self.items:
            self.items.remove(order_item)
        self.item_option_window.destroy()


        self.update_order_display_summary()


    def update_balance_due(self):
        self.balance_due = sum(item.total_price for item in self.items)
        print(self.balance_due)


    def modify_item(self, order_item):
        if order_item in self.items:
            self.menu.kill_frames()
            order_item.window.initiate_window_display()
        self.item_option_window.destroy()



    def create_order_summary_frame(self):
        self.order_summary_frame = LabelFrame(self.root, bg='#1e1e1e', text="Order Summary Frame", width=300,
                                              height=925, padx=0, pady=10)
        self.order_summary_frame.grid(column=0, row=0)
        self.order_summary_frame.grid_propagate(False)

        self.update_balance_due()

        self.balance_due_label = Label(self.order_summary_frame, text=f'balance due:{self.balance_due:.2f}')
        self.balance_due_label.grid(column=0, row=1000)




    def item_action_window(self, order_item):
        self.item_option_window = Toplevel(root)
        self.item_option_window.geometry('500x500+1920+0')
        self.remove_item_button = Button(self.item_option_window,text='Remove Item', command=lambda: self.remove_item(order_item))
        self.remove_item_button.grid(row=0, column=0)


        if order_item.sauces or order_item.side or order_item.drink or order_item.item_type == 'Sauces':
            self.modify_item_button = Button(self.item_option_window, text= 'Modify Item', command=lambda:self.modify_item(order_item))
            self.modify_item_button.grid(row=0, column=1)

    def update_order_display_summary(self):
        self.update_balance_due()

        if not self.order_summary_frame.winfo_exists():
            return

            #clears order summary frame
        for button in self.item_summary_buttons:
            button.destroy()

        for index, item in enumerate(self.items):

            order_item_button = Button(self.order_summary_frame, text=f'{item.item_name}({item.base_price})', anchor='w', height = 0, width = 50, padx=0, pady=5,command=lambda item=item: self.item_action_window(item)  # This lambda captures the current item value
    )
            order_item_button.grid(column=0, row=index)
            self.item_summary_buttons.append(order_item_button)

        #updates balance due label
        self.balance_due_label.config(text=f'Balance Due: {self.balance_due:.2f}')










class OrderItem:
    def __init__(self, item_name, item_type, menu, window=None):

        self.item_name = item_name
        self.item_type = item_type


        self.order = menu.order
        self.menu = menu
        if item_type == 'service':
            self.base_price = 0
        else:
            self.base_price = self.menu.menu[item_type][item_name]

        self.total_price = self.base_price

        self.order.add_item(self)




        self.window = window

        self.item_type = item_type





        #saves a reference to current order, to send itself to add_item


        self.sauces = []
        self.side = {}
        self.drink = {}
        self.extra_sauces = []

    def update_item_name(self, name):
        self.item_name = name
        self.base_price = self.menu.menu[self.item_type][self.item_name]
        self.total_price = self.base_price
        print(self.base_price)
        print(self.total_price)

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

    def add_note(self):
        ...



class WindowFrames:
    def __init__

class ScratchSauceWindow:
    def __init__(self, sauce, menu):
        self.menu = menu
        self.sauce = sauce
        self.order_item = OrderItem(sauce,'Sauces',self.menu, self)



        self.initiate_window_display()

    def initiate_window_display(self):
        self.create_frames()
        self.populate_frames()

    def create_frames(self):
        self.frame_color_bg = '#1e1e1e'
        self.upper_sauce_frame = LabelFrame(self.menu.root, bg=self.frame_color_bg, text="Upper Frame", width=1620,
                                           height=150, padx=0, pady=10)
        self.upper_sauce_frame.grid(column=1, row=0)
        self.upper_sauce_frame.grid_propagate(False)



        self.order_item_summary = LabelFrame(self.menu.root, bg=self.frame_color_bg, text="Order",
                                               width=300,
                                               height=1080, padx=0, pady=10)
        self.order_item_summary.grid(column=0, row=0, rowspan=2)
        self.order_item_summary.grid_propagate(False)



        self.sauce_size_selection_frame = LabelFrame(self.menu.root, bg=self.frame_color_bg, text="Size selection", width=1620,
                                           height=925, padx=0, pady=10)

        self.sauce_size_selection_frame.grid(column=1, row=1)
        self.sauce_size_selection_frame.grid_propagate(False)

    def populate_frames(self):
        self.populate_sauce_size_selection_frame()
        self.populate_order_item_summary()


    def populate_sauce_size_selection_frame(self):
        individual_sauce_button = Button(self.sauce_size_selection_frame, text= "Individual Sauce", height = 7, width = 15, fg= self.menu.button_colorfg, bg= self.menu.button_colorfg, font=self.menu.button_font, command=lambda: self.silly_button(self.sauce))
        individual_sauce_button.grid(row=0,column=0)

        catering_sauce_button =  Button(self.sauce_size_selection_frame, text= "Party Size (8oz)", height = 7, width = 15, fg= self.menu.button_colorfg, bg= self.menu.button_colorfg, font=self.menu.button_font, command=lambda: self.silly_button(f'8oz {self.sauce}'))
        catering_sauce_button.grid(row=0, column=1)

    def populate_order_item_summary(self):
        self.name_label = Label(self.order_item_summary, text='Quick Sale')
        self.name_label.grid(row=0, column=0, padx=0)

        self.order_label = Label(self.order_item_summary, text='Order')
        self.order_label.grid(row=1, column=0)

        self.service_type = Label(self.order_item_summary, text='Carryout')
        self.service_type.grid(row=2, column=0)

        self.sauce_choice_label = Label(self.order_item_summary, text= self.sauce)
        self.sauce_choice_label.grid(row=3, column=0)


        ...

    def silly_button(self, sauce):
        self.order_item.update_item_name(sauce)
        self.upper_sauce_frame.destroy()
        self.order_item_summary.destroy()
        self.sauce_size_selection_frame.destroy()
        self.menu.initiate_main_menu_display()















        ...




class Menu:
    def __init__(self, order, root):
        self.order = order
        self.root = root

        #a lot of code in this function, but again eventually none of the mapping dictionaries will be necessary

        self.menu = {
            "Meals": {
                "Snack Pack": 8.99,
                "Medium Pack": 10.99,
                "Large Pack": 12.99,
                "Mega Pack": 14.99,
            },
            "Kids Meals": {
                "Kids 2 Tenders": 6.99,
                "Kids Sandwich": 6.99,
                "Kid- Milk": 2.69,
                "Kid- Juice Pouch": 2.69,
            },
            "Sandwiches": {
                "Citybird Sandwich": 9.99,
                "Lemon Thyme Sandwich": 9.99,
                "Spicy Sandwich": 9.99,
                "Buffalo Bleu Sandwich": 9.99,
                "Citybird Sandwich - Only": 7.49,
                "Lemon Thyme Sandwich - Only": 7.49,
                "Spicy Sandwich - Only": 7.49,
                "Buffalo Bleu Sandwich - Only": 7.49,
            },
            "Sides": {
                "Salad": 7.99,
                "Add 3 Tenders": 4.00,
                "Fries": 2.49,
                "Slaw": 1.99,
                "1/2 Salad": 3.49,
                "Apple Sauce": 1.49,
                "Pickles": 0.75,
                "Bun": 1.00,
                "Kids Fries": 2.49,
            },
            "Sauces": {
                "City Sauce": 0.75,
                "Lemon Thyme Ranch": 0.75,
                "Honey Dijon": 0.75,
                "Buffalo Bleu": 0.75,
                "Hickory BBQ": 0.75,
                "Spicy Mayo": 0.75,
                "Hot Honey": 1.00,
                "Citybird Vinaigrette": 0.75,
                "8oz City Sauce": 5.00,
                "8oz Lemon Thyme Ranch": 5.00,
                "8oz Honey Dijon": 5.00,
                "8oz Buffalo Bleu": 5.00,
                "8oz Hickory BBQ": 5.00,
                "8oz Spicy Mayo": 5.00,
                "8oz Hot Honey": 5.00,
            },
            "Drinks": {
                "Fountain Drink": 2.69,
                "Bottle Water": 2.69,
                "Juice & Wikki Stix": 2.69,
                "Milk & Wikki Stix": 2.69,
                "Lacroix": 2.69,
                "Milk": 2.69,
                "Kid- Juice Pouch": 2.69,
            }
        }
        self.create_frames()
        self.populate_menu_items_frame()
        self.populate_bottom_row_frame()

    def navigate_to(self, window, item_name):
        self.menu_items_frame.destroy()
        self.bottom_row_frame.destroy()
        self.order.order_summary_frame.destroy()
        window(item_name, self)

    def kill_frames(self):
        self.menu_items_frame.destroy()
        self.bottom_row_frame.destroy()
        self.order.order_summary_frame.destroy()

    def initiate_main_menu_display(self):
        self.create_frames()
        self.order.create_order_summary_frame()
        self.populate_frames()








    def create_frames(self):
        #initiated once

        self.frame_color_bg = '#1e1e1e'



        self.menu_items_frame = LabelFrame(self.root, bg=self.frame_color_bg, text="All menu items", width=1600, height=925, padx = 0, pady=10)
        self.menu_items_frame.grid(column=1, row=0)
        self.menu_items_frame.grid_propagate(False)









        #dont know where else to put this label, needs to be initiated once






        self.bottom_row_frame = LabelFrame(self.root, bg=self.frame_color_bg,text = "Random stuff", width=1920,height=175)
        self.bottom_row_frame.grid(column=0,row=1, columnspan=2)
        self.bottom_row_frame.grid_propagate(False)



    def populate_frames(self):
        self.populate_menu_items_frame()
        self.populate_bottom_row_frame()
        self.order.update_order_display_summary()

    def populate_bottom_row_frame(self):
        ...

    def populate_menu_items_frame(self):
        #initiated once


        #button customization
        button_width = 10
        button_height = 4
        button_padx = 0
        button_pady = 0,10
        self.button_colorfg = 'black'
        self.button_colorfg = 'black'
        self.button_font= tkFont.Font(size=13)

        #label customization
        font = tkFont.Font(size=20)
        label_pady = 3
        label_padx =0

    #LABELS

        beverages = Label(self.menu_items_frame, text="BEVERAGES", font=font,bg=self.frame_color_bg)
        beverages.grid(column=0, row=1, padx=label_padx, pady=label_pady, sticky='w')

        # tender meal label
        tender_meals = Label(self.menu_items_frame, text="TENDER MEALS", font=font, bg=self.frame_color_bg,)
        tender_meals.grid(column=0, row=3, columnspan=2,padx=label_padx, pady=label_pady,sticky='w')

        # sandwich meal label
        tender_sandwich_meals = Label(self.menu_items_frame, text="TENDER SANDWICH MEALS", font=font, bg=self.frame_color_bg)
        tender_sandwich_meals.grid(column=0, row=5, columnspan=3, padx=label_padx, pady=label_pady,sticky='w')

        # salad label
        salad_label = Label(self.menu_items_frame, text="SALAD", font=font, bg=self.frame_color_bg)
        salad_label.grid(column=0, row=7, padx=label_padx, pady=label_pady,sticky='w')

        # kids meal label
        kids_menu = Label(self.menu_items_frame, text="Kids Menu", font=font, bg=self.frame_color_bg)
        kids_menu.grid(column=0, row=9, padx=label_padx, pady=label_pady,sticky='w')

        # side label
        sides_label = Label(self.menu_items_frame, text="SIDES", font=font, bg=self.frame_color_bg)
        sides_label.grid(column=0, row=11, padx=label_padx, pady=label_pady,sticky='w')


        #sauce label
        sauce_label = Label(self.menu_items_frame, text="SAUCES", font=font, bg=self.frame_color_bg)
        sauce_label.grid(column=0, row=13, padx=label_padx, pady=label_pady,sticky='w')






    #main menu  buttons

        #carry out , dine in , rename
        dine_in = Button(self.menu_items_frame, text = '--DINE IN--',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda: OrderItem('--DINE IN--','service', self))
        carryout = Button(self.menu_items_frame, text = '--CARRYOUT--',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        rename = Button(self.menu_items_frame, text = 'Rename',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')

        dine_in.grid(column=0, row=0, padx = button_padx, pady = button_pady)
        carryout.grid(column=1, row=0, padx = button_padx, pady = button_pady)
        rename.grid(column=2, row=0, padx = button_padx, pady = button_pady)



        #beverage label


        #drink options
        coke = Button(self.menu_items_frame, text= "coke", height = button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda: OrderItem('Fountain Drink', 'Drinks', self))

        coke.grid(column=0, row=2,padx = button_padx, pady = button_pady)






        #tender meal options
        snack_pack = Button(self.menu_items_frame, text="Snack Pack(4)",height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg)
        medium_pack = Button(self.menu_items_frame, text = 'Medium Pack(6)',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        large_pack = Button(self.menu_items_frame, text = 'Large Pack(8)',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        mega_pack = Button(self.menu_items_frame, text = 'Mega Pack(10)',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        on_side_tenders = Button(self.menu_items_frame, text = 'On Side Tenders',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')

        snack_pack.grid(column=0, row=4, padx = button_padx, pady = button_pady)
        medium_pack.grid(column=1, row=4, padx = button_padx, pady = button_pady)
        large_pack.grid(column=2, row=4, padx = button_padx, pady = button_pady)
        mega_pack.grid(column=3, row=4, padx = button_padx, pady = button_pady)
        on_side_tenders.grid(column=4, row=4, padx = button_padx, pady = button_pady)






        #sandwich meal options
        buffalo_blue_sandwich = Button(self.menu_items_frame,text='Buffalo Bleu\n Sandwich', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        citybird_sandwich = Button(self.menu_items_frame, text = 'CityBird \nSandwich',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        lemon_thyme_sandwich = Button(self.menu_items_frame, text = 'Lemon\nThyme\nSandwich',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        spicy_sandwich = Button(self.menu_items_frame, text = 'Spicy\nSandwich',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')

        buffalo_blue_sandwich.grid(column=0, row=6, padx = button_padx, pady = button_pady)
        citybird_sandwich.grid(column=1, row=6, padx = button_padx, pady = button_pady)
        lemon_thyme_sandwich.grid(column=2, row=6, padx = button_padx, pady = button_pady)
        spicy_sandwich.grid(column=3, row=6, padx = button_padx, pady = button_pady)





        #salad button
        salad = Button(self.menu_items_frame, text='Salad',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:'')
        salad.grid(column=0, row=8, padx = button_padx, pady = button_pady)





        #kids meal options
        kids_2_tender = Button(self.menu_items_frame, text='Kids 2\nTenders',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:'')
        kids_sandwich = Button(self.menu_items_frame, text='Kids\nSandwich',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:'')
        kid_juice_pouch = Button(self.menu_items_frame, text='Kid-Juice\nPouch',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:'')
        kid_milk = Button(self.menu_items_frame,text='Kid- Milk', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:'')
        apple_sauce = Button(self.menu_items_frame, text='Apple\nSauce',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:'')
        pickles = Button(self.menu_items_frame, text='Pickles',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:'')


        kids_2_tender.grid(column=0, row=10, padx = button_padx, pady = button_pady)
        kids_sandwich.grid(column=1, row=10, padx = button_padx, pady = button_pady)
        kid_juice_pouch.grid(column=2, row=10, padx = button_padx, pady = button_pady)
        kid_milk.grid(column=3, row=10, padx = button_padx, pady = button_pady)
        apple_sauce.grid(column=4, row=10, padx = button_padx, pady = button_pady)
        pickles.grid(column=5, row=10, padx = button_padx, pady = button_pady)




        #side options
        half_salad = Button(self.menu_items_frame,text='(1/2) Salad', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font,command=lambda:'')
        apple_sauce = Button(self.menu_items_frame, text='Apple\nSauce',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        bun = Button(self.menu_items_frame,text='Bun', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        fries = Button(self.menu_items_frame, text='Fries',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font,command=lambda:'')
        pickles = Button(self.menu_items_frame,text='Pickles', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font,command=lambda:'')
        slaw = Button(self.menu_items_frame, text='Slaw',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        on_side_tenders = Button(self.menu_items_frame, text='On Side Tenders',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font,command=lambda:'')

        half_salad.grid(column=0, row=12, padx = button_padx, pady = button_pady)
        apple_sauce.grid(column=1, row=12, padx = button_padx, pady = button_pady)
        bun.grid(column=2, row=12, padx = button_padx, pady = button_pady)
        fries.grid(column=3, row=12, padx = button_padx, pady = button_pady)
        pickles.grid(column=4, row=12, padx = button_padx, pady = button_pady)
        slaw.grid(column=5, row=12, padx = button_padx, pady = button_pady)
        on_side_tenders.grid(column=6, row=12, padx = button_padx, pady = button_pady)





        #sauce options
        buffalo_bleu = Button(self.menu_items_frame, text='Buffalo\nBleu',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,font=self.button_font,command=lambda:self.navigate_to(ScratchSauceWindow,'Buffalo Bleu'))
        city_sauce = Button(self.menu_items_frame, text='City Sauce',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:'')
        citybird_vinaigrette = Button(self.menu_items_frame, text='Citybird\n Vinaigrette',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:'')
        hickory_bbq = Button(self.menu_items_frame, text='Hickory\nBBQ',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,font=self.button_font, command=lambda:'')
        honey_dijon = Button(self.menu_items_frame,text='Honey Dijon', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,font=self.button_font, command=lambda:'')
        hot_honey = Button(self.menu_items_frame, text='Hot Honey',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:'')
        lemon_thyme_ranch = Button(self.menu_items_frame, text='Lemon Thyme Ranch',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:'')
        sriracha_mayo = Button(self.menu_items_frame,text='Sriracha\nMayo', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:'')
        sriracha_mayo_c = Button(self.menu_items_frame, text='Sriracha\nMayo C',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:'')

        buffalo_bleu.grid(column=0, row=14, padx = button_padx, pady = button_pady)
        city_sauce.grid(column=1, row=14, padx = button_padx, pady = button_pady)
        citybird_vinaigrette.grid(column=2, row=14, padx = button_padx, pady = button_pady)
        hickory_bbq.grid(column=3, row=14, padx = button_padx, pady = button_pady)
        honey_dijon.grid(column=4, row=14, padx = button_padx, pady = button_pady)
        hot_honey.grid(column=5, row=14, padx = button_padx, pady = button_pady)
        lemon_thyme_ranch.grid(column=6, row=14, padx = button_padx, pady = button_pady)
        sriracha_mayo.grid(column=7, row=14, padx = button_padx, pady = button_pady)
        sriracha_mayo_c.grid(column=8, row=14, padx = button_padx, pady = button_pady)





















root = Tk()

initiate_main_window(root)

order = Order(root)

root.mainloop()








