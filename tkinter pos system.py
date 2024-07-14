
###TO DO###
#Implement Discount function
#Clean up OrderItem display and OrderSummary display


#DONE ---Implement Additional Sauces function
#DONE ---Complete Salad modification window
#DONE--- Complete Kids Meal modification window
#DONE--- Add rest of drink buttons on main menu
#DONE ---Implement Scrolling ability
#DONE ---Add Sandwich Only buttons on main menu
#DONE ---Implement Notes function
#DONE ---Implement Rename function











#to start off tomorrow
#review OrderItem logic - specifically looking to consolidate logic, and fix Drink logic

from tkinter import *
import tkinter.font as tkFont



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
        self.order_name = 'Quick Sale'

        #will implement service type prompt later
        self.service_type = 'Dine In'

        self.root = root
        self.item_summary_buttons = []


        self.balance_due = 0.00

        self.items = []
        # initializes list of order items

        self.menu = Menu(self, root)

        self.create_order_summary_frame()



    def rename_order(self):
        print(self.order_name)
        self.rename_window = Toplevel(root)
        self.rename_window.geometry('500x500+1920+0')


        self.order_name_entry = Entry(self.rename_window,width=40)

        self.order_name_entry.grid(row=0,column=0)

        self.confirm_name = Button(self.rename_window, text='Confirm', command= lambda: self.confirm_rename())
        self.confirm_name.grid(row=1, column=0)


    def confirm_rename(self):

        self.order_name = self.order_name_entry.get()
        self.rename_window.destroy()
        print(self.order_name)





    def add_item(self, order_item):
        self.items.append(order_item)
        self.update_order_display_summary()


    def remove_item(self, order_item):
        if order_item in self.items:
            self.items.remove(order_item)
        try:
            self.item_option_window.destroy()
        except AttributeError:
            pass


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
        self.frame_color_bg = '#1e1e1e'
        self.order_summary_canvas = Canvas(self.root, bg=self.frame_color_bg, width=300, height = 925)
        self.order_summary_scrollbar = Scrollbar(self.root, orient='vertical', command= self.order_summary_canvas.yview)
        self.order_summary_frame = Frame(self.order_summary_canvas, bg= self.frame_color_bg)


        #Bind the inner frame to the canvas
        self.order_summary_frame.bind('<Configure>',lambda e: self.order_summary_canvas.configure(scrollregion = self.order_summary_canvas.bbox('all')))

        self.order_summary_canvas.create_window((0,0), window = self.order_summary_frame, anchor='nw')

        self.order_summary_canvas.configure(yscrollcommand=self.order_summary_scrollbar.set)

        #place the canvas and scrollbar in the grid
        self.order_summary_canvas.grid(column=0, row=0)
        self.order_summary_scrollbar.grid(column=1, row=0, sticky='ns')



        self.balance_due_label = Label(self.order_summary_frame, text=f'balance due:{self.balance_due:.2f}')
        self.balance_due_label.grid(column=0, row=1000)


        self.update_balance_due()


    def item_action_window(self, order_item):
        self.item_option_window = Toplevel(root)
        self.item_option_window.geometry('500x500+1920+0')
        self.remove_item_button = Button(self.item_option_window,text='Remove Item', command=lambda: self.remove_item(order_item))
        self.remove_item_button.grid(row=0, column=0)


        if order_item.first_sauce or order_item.side or order_item.drink or order_item.item_type == 'Sauces':
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
            # Helper function to format item with price if price is not 0 or None
            def format_item(name, price):
                return f"{name}({price})" if price not in [0, None] else name

            # Check if each attribute is present and create the corresponding text
            first_sauce_text = f"\n{format_item(item.first_sauce['sauce'], item.first_sauce['price'])}" if item.first_sauce else ""
            second_sauce_text = f"\n{format_item(item.second_sauce['sauce'], item.second_sauce['price'])}" if item.second_sauce else ""
            side_text = f"\n{format_item(item.side['side'], item.side['price'])}" if item.side else ""
            drink_text = f"\n{format_item(item.drink['drink'], item.drink['price'])}" if item.drink else ""

            # Generate the extra sauces text with prices
            extra_sauces_text = "\n" + "\n".join(
                [f"{format_item(s['sauce'], s['price'])}" for s in item.extra_sauces]) if item.extra_sauces else ""

            note_text = f"\n{item.item_note}" if item.item_note else ""

            button_text = f"{item.item_name} ({item.base_price})\n{first_sauce_text}{second_sauce_text}{side_text}{drink_text}{extra_sauces_text}{note_text}"

            # Create the button
            order_item_button = Button(self.order_summary_frame, text=button_text, anchor='w', height=0, width=50,
                                       padx=0, pady=5,
                                       command=lambda item=item: self.item_action_window(
                                           item))  # This lambda captures the current item value
            order_item_button.grid(column=0, row=index)
            self.item_summary_buttons.append(order_item_button)

        #updates balance due label
        self.balance_due_label.config(text=f'Balance Due: {self.balance_due:.2f}')










class OrderItem:
    def __init__(self, item_name, item_type, menu, window=None):

        self.item_name = item_name
        self.item_type = item_type

        self.first_sauce = {}
        self.second_sauce = {}
        self.side = {}
        self.drink = {}
        self.extra_sauces = []
        self.item_note = ''

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




    def update_item_name(self, name):
        self.item_name = name
        self.base_price = self.menu.menu[self.item_type][self.item_name]
        self.total_price = self.base_price
        print(self.base_price)
        print(self.total_price)
        self.window.window.update_order_item_summary()

    def add_item_note(self, note):
        self.item_note = ''
        self.item_note += note
        print(self.item_note)


        self.window.window.update_order_item_summary()


    def add_first_sauce(self, sauce):
        if sauce == "Hot Honey":
            price = self.menu.menu['Sauces'][sauce]
        else:
            price = 0
        self.first_sauce = {'sauce':sauce,'price':price}

        self.calculate_total_price()

        self.window.window.update_order_item_summary()

    def add_second_sauce(self,sauce):
        if sauce == "Hot Honey":
            price = self.menu.menu['Sauces'][sauce]
        else:
            price = 0
        self.second_sauce = {'sauce': sauce, 'price': price}

        self.calculate_total_price()

        self.window.window.update_order_item_summary()

    def add_extra_sauce(self,sauce):
        sauce_index = next((index for (index, d) in enumerate(self.extra_sauces) if d['sauce'] == sauce), None)

        if sauce_index is not None:
            # If the sauce is present, remove the dictionary from the list
            self.extra_sauces.pop(sauce_index)
        else:
            # If the sauce is not present, add it to the list
            self.extra_sauces.append({'sauce': sauce, 'price': self.menu.menu['Sauces'][sauce]})
        self.calculate_total_price()
        self.window.window.update_order_item_summary()





    def add_sides(self, side):
        #check for redundent code later on


        #handles side logic for tender meals
        if self.item_type == 'Meals':
            if side in ('1/2 Salad','1/2 salad (Honey Dijon)','1/2 salad (ranch)','1/2 Salad (Vinaigrette)'):
                price = 1.49


            else:
                price = 0
            self.side = {'side': side, 'price': price}






        elif self.item_type == 'Sandwiches':

            if side == '1/2 Salad':
                price = 1.49
            else:
                price = 0
            self.side = {'side': side, 'price': price}


        elif self.item_type == 'Kids meal':
            price = 0
            self.side = {'side': side, 'price': price}

        elif self.item_type == 'Salad':
            price = self.menu.menu['Sides'][side]

        else:
            price = 0
        self.side = {'side': side, 'price': price}

        self.calculate_total_price()
        self.window.window.update_order_item_summary()






    def add_drink(self, drink):

        if drink in ("No Drink", "Tap Water") or self.item_type == 'Kids Meals':
            price = 0
        else:
            price = 1.00




        self.drink = {'drink': drink, 'price':price}
        self.calculate_total_price()

        self.window.window.update_order_item_summary()

    def calculate_total_price(self):
        self.total_price = self.base_price

        if self.first_sauce:
            self.total_price += self.first_sauce.get('price', 0)
        if self.second_sauce:
            self.total_price += self.second_sauce.get('price', 0)
        if self.side:
            self.total_price += self.side.get('price', 0)
        if self.drink:
            self.total_price += self.drink.get('price', 0)
        for sauce in self.extra_sauces:
            self.total_price += sauce.get('price', 0)


    def add_note(self):
        ...



class ModificationWindow:
    def __init__(self, menu, order_item, item_specific_info):

        self.other_info = item_specific_info

        self.menu = menu
        self.order_item = order_item

        #style
        self.frame_color_bg = '#1e1e1e'
        self.mod_button_font = tkFont.Font(size=15)


        self.initiate_window_display()



    def initiate_window_display(self):
        self.upper_frame = LabelFrame(self.menu.root, bg=self.frame_color_bg, text="Upper Frame", width=1620,
                                      height=100, padx=0, pady=10)
        self.upper_frame.grid(column=1, row=0)
        self.upper_frame.grid_propagate(False)

        self.order_item_summary = LabelFrame(self.menu.root, bg=self.frame_color_bg, text="Order",
                                             width=300,
                                             height=1080, padx=0, pady=0)
        self.order_item_summary.grid(column=0, row=0, rowspan=2)
        self.order_item_summary.grid_propagate(False)

        self.modification_selection_frame = LabelFrame(self.menu.root, bg=self.frame_color_bg, text="Size selection",
                                                       width=1620,
                                                       height=980, padx=0, pady=10)

        self.modification_selection_frame.grid(column=1, row=1)
        self.modification_selection_frame.grid_propagate(False)

        self.populate_upper_frame()
        self.populate_upper_frame()
        #behaves the same
        self.populate_order_item_summary()
        self.update_order_item_summary()









    def populate_upper_frame(self):
        if self.order_item.item_type == 'Sauces':
            self.sauce_type_upper_frame()
            self.sauce_modification()
        elif self.order_item.item_type == 'Meals':
            self.tender_meal_type_upper_frame()
        elif self.order_item.item_type == 'Sandwiches':
            self.sandwich_type_upper_frame()
        elif self.order_item.item_type=='Salad':
            self.salad_type_upper_frame()
        elif self.order_item.item_type == 'Kids Meals':
            self.kids_meal_type_upper_frame()


    def kids_meal_type_upper_frame(self):
        self.get_side()
        self.side_choice_tab = self.create_upper_frame_button(self.upper_frame, "Kids Side Choice", 0,0,lambda: self.get_side())
        self.drink_choice_tab = self.create_upper_frame_button(self.upper_frame, "Kids Meal Drink Choice",0,1,lambda: self.get_drink())
        self.add_item_note_tab = self.create_upper_frame_button(self.upper_frame, "Notes", 0, 5, lambda: self.add_order_item_note())



    def salad_type_upper_frame(self):
        self.get_side()
        self.side_choice_tab = self.create_upper_frame_button(self.upper_frame, "Add 3 Tenders?", 0,0,lambda: self.get_side())

        self.dressing_choice_tab = self.create_upper_frame_button(self.upper_frame, 'Dressing Choice', 0, 1, lambda: self.get_dressing(self.order_item.add_first_sauce))
        if self.order_item.item_name == 'Salad':
            self.dressing_choice_tab = self.create_upper_frame_button(self.upper_frame, 'Dressing Choice', 0, 2, lambda: self.get_dressing(self.order_item.add_second_sauce))
        self.add_item_note_tab = self.create_upper_frame_button(self.upper_frame, "Notes", 0, 5, lambda: self.add_order_item_note())




        ...

    def sandwich_type_upper_frame(self):
        self.get_side()
        self.side_choice_tab = self.create_upper_frame_button(self.upper_frame,'With Fries?', 0,2,lambda: self.get_side())


        self.drink_choice_tab = self.create_upper_frame_button(self.upper_frame, "Drink Choice?",0,3,lambda: self.get_drink())

        self.extra_sauce_choice_tab = self.create_upper_frame_button(self.upper_frame, 'Extra Sauce?', 0, 4, lambda: self.get_sauce(self.order_item.add_extra_sauce))

        self.add_item_note_tab = self.create_upper_frame_button(self.upper_frame, "Notes", 0, 5, lambda: self.add_order_item_note())





    def get_dressing(self, add_dressing_method):
        self.dressings = ['Vinaigrette', 'Lemon Thyme Ranch', 'NO DRESSING', 'Honey Dijon']

        for index, dressing in enumerate(self.dressings):
            dressing_button = self.create_modification_button(self.modification_selection_frame, dressing, 0, index, lambda d=dressing:add_dressing_method(d) )


    def tender_meal_type_upper_frame(self):
        self.get_sauce(self.order_item.add_first_sauce)
        self.sauce_choice_tab = self.create_upper_frame_button(self.upper_frame, 'Sauce Choice',0,0, lambda : self.get_sauce(self.order_item.add_first_sauce))


        if self.order_item.item_name in ('Large Pack','Mega Pack'):
            self.second_sauce_choice_tab = self.create_upper_frame_button(self.upper_frame, "Sauce Choice", 0,1, lambda : self.get_sauce(self.order_item.add_second_sauce))

        self.side_choice_tab = self.create_upper_frame_button(self.upper_frame, "With Fries?", 0,2,lambda: self.get_side())

        self.drink_choice_tab = self.create_upper_frame_button(self.upper_frame, 'Drink Choice?',0,3,lambda: self.get_drink())

        self.extra_sauce_choice_tab = self.create_upper_frame_button(self.upper_frame, 'Extra Sauce?', 0, 4, lambda: self.get_sauce(self.order_item.add_extra_sauce))

        self.add_item_note_tab = self.create_upper_frame_button(self.upper_frame, "Notes", 0, 5, lambda: self.add_order_item_note())

    def add_order_item_note(self):
        self.clear_modification_frame()
        self.note_entry = Entry(self.modification_selection_frame, width=40)
        self.note_entry.grid(row=0, column=0)

        save_note_button = Button(self.modification_selection_frame, text="Save Note", command= lambda:self.order_item.add_item_note(self.note_entry.get()))
        save_note_button.grid(row=0, column=1)

    def create_upper_frame_button(self, parent, text,row, column, command):
        button = Button(parent, text=text, height=4,
               width=15, fg=self.menu.button_colorfg, bg=self.menu.button_colorfg,
               font=self.mod_button_font,
               command=command)
        button.grid(row=row, column=column)
        return button

    def get_side(self):
        self.clear_modification_frame()

        if self.order_item.item_type == "Salad":
            self.add_3_tenders = self.create_modification_button(self.modification_selection_frame, "Add 3 Tenders", 0,0, lambda: self.order_item.add_sides('Add 3 Tenders'))
            self.no_tenders = self.create_modification_button(self.modification_selection_frame, 'No Tenders', 0, 1, lambda: self.order_item.add_sides('No Tenders'))

        elif self.order_item.item_type == "Kids Meals":
            self.kids_fries = self.create_modification_button(self.modification_selection_frame, "Kids Fries", 0,0, lambda: self.order_item.add_sides('Kids Fries'))
            self.apple_sauce = self.create_modification_button(self.modification_selection_frame, "Apple Sauce", 0,1, lambda: self.order_item.add_sides('Apple Sauce'))



        else:
            self.sides = ['Fries', 'Slaw', '1/2 salad (Honey Dijon)', '1/2 salad (ranch)', '1/2 Salad (Vinaigrette)']

            for index, side in enumerate(self.sides):
                side_button = self.create_modification_button(self.modification_selection_frame, side, 0, index, lambda s=side: self.order_item.add_sides(s))



    def create_modification_button(self, parent, text, row, column, command):
        button = Button(parent, text=text, height=4,
                        width=15, fg=self.menu.button_colorfg, bg=self.menu.button_colorfg,
                        font=self.mod_button_font,
                        command=command)
        button.grid(row=row, column=column)
        return button

    def get_drink(self):
        self.drinks_row_1 = ("Coke", "Diet Coke", "Sprite", "Iced Tea","Seasonal Tea", "Lemonade", "Bottle Water", "Juice & Wikki Stix")
        self.drinks_row_2 = ( "Milk & Wikki Stix", "Lemon Lacroix", "GrapeFruit Lacroix", "Tap Water", "No Drink", "Coke Zero")
        self.clear_modification_frame()

        if self.order_item.item_type == "Kids Meals":
            fountain_drink_button = self.create_modification_button(self.modification_selection_frame, 'Fountain Drink & Wikki Stix', 0, 0,
                                                           lambda : self.order_item.add_drink('Fountain Drink & Wikki Stix'))
            drink_button = self.create_modification_button(self.modification_selection_frame, "Juice & Wikki Stix", 0, 1,
                                                           lambda : self.order_item.add_drink('Juice & Wikki Stix'))
            drink_button = self.create_modification_button(self.modification_selection_frame, "Milk & Wikki Stix", 0, 2,
                                                           lambda : self.order_item.add_drink("Milk & Wikki Stix"))
        else:
            for index, drink in enumerate(self.drinks_row_1):
                drink_button = self.create_modification_button(self.modification_selection_frame, drink, 0,index, lambda d = drink: self.order_item.add_drink(d))



            for index, drink in enumerate(self.drinks_row_2):
                drink_button = self.create_modification_button(self.modification_selection_frame, drink, 1, index, lambda d = drink: self.order_item.add_drink(d))


    def get_sauce(self, add_sauce_method):

        self.sauces = ['City Sauce', 'Hickory BBQ','Honey Dijon','Hot Honey','Lemon Thyme Ranch', 'Buffalo Bleu','Sriracha Mayo']
        self.clear_modification_frame()

        for index, sauce in enumerate(self.sauces):
            sauce_button = self.create_modification_button(self.modification_selection_frame, sauce, 0, index, lambda s=sauce:add_sauce_method(s))





    def sauce_type_upper_frame(self):
        self.sauce_size_tab = self.create_upper_frame_button(self.upper_frame, 'Sauce Size?', 0,0, lambda: self.sauce_modification())


        self.note_tab = self.create_upper_frame_button(self.upper_frame, 'Notes', 0,1, lambda: self.note_modification() )




    def sauce_modification(self):
        self.clear_modification_frame()
        self.individual_sauce_button = self.create_modification_button(self.modification_selection_frame, 'Individual Sauce', 0,0,lambda: self.order_item.update_item_name(self.other_info.sauce))

        self.catering_sauce_button = self.create_modification_button(self.modification_selection_frame, 'Party Size (8oz)',0,1, lambda: self.order_item.update_item_name(f'8oz {self.other_info.sauce}'))




    def clear_modification_frame(self):
        for widget in self.modification_selection_frame.winfo_children():
            widget.destroy()
        self.create_done_button()
        self.update_order_item_summary()
        self.create_cancel_button()

    def create_cancel_button(self):
        self.cancel_button = Button(self.modification_selection_frame, text='Cancel', height=5, width=8,
                                  command=lambda: self.cancel_order_item())
        self.cancel_button.grid(row=1000, column=1, pady=600)
    def create_done_button(self):
        self.done_button = Button(self.modification_selection_frame, text='Done', height=5, width=8, state=DISABLED,
                                  command=lambda: self.destroy_frames())
        self.done_button.grid(row=1000, column=0,pady=600)

    def note_modification(self):
        self.clear_modification_frame()
        individual_sauce_button = Button(self.modification_selection_frame, text="Note", height=4,
                                         width=15, fg=self.menu.button_colorfg, bg=self.menu.button_colorfg,
                                         font=self.mod_button_font,
                                         command=lambda: '')
        individual_sauce_button.grid(row=0, column=0)



    def check_required_options(self):
        if self.order_item.item_name in ('Snack Pack', 'Medium Pack'):
            if self.order_item.first_sauce and self.order_item.side and self.order_item.drink:
                self.enable_done_button()

        elif self.order_item.item_name in ('Large Pack', 'Medium Pack'):
            if self.order_item.first_sauce and self.order_item.second_sauce and self.order_item.side and self.order_item.drink:
                self.enable_done_button()

        elif self.order_item.item_type == 'Sandwiches':
            if self.order_item.side and self.order_item.drink:
                self.enable_done_button()

        elif self.order_item.item_type == 'Sauces':
            self.enable_done_button()
        elif self.order_item.item_name == "Salad":
            if self.order_item.first_sauce and self.order_item.second_sauce and self.order_item.side:
                self.enable_done_button()
        elif self.order_item.item_name == '1/2 Salad':
            if self.order_item.first_sauce:
                self.enable_done_button()
        elif self.order_item.item_type == "Kids Meals":
            if self.order_item.side and self.order_item.drink:
                self.enable_done_button()



    def enable_done_button(self):
        self.done_button.config(state=NORMAL)


    def cancel_order_item(self):
        self.menu.order.remove_item(self.order_item)
        self.destroy_frames()




    def destroy_frames(self):
        self.upper_frame.destroy()
        self.order_item_summary.destroy()
        self.modification_selection_frame.destroy()
        self.menu.initiate_main_menu_display()




    def populate_order_item_summary(self):
        self.name_label = Label(self.order_item_summary, bg=self.frame_color_bg, text=self.menu.order.order_name,
                                width=26, font=tkFont.Font(size=18))
        self.name_label.grid(row=0, column=0, padx=0)

        self.order_label = Label(self.order_item_summary, bg=self.frame_color_bg, text='Order')
        self.order_label.grid(row=1, column=0, sticky='w')

        self.service_type_label = Label(self.order_item_summary, bg=self.frame_color_bg,
                                        text=self.menu.order.service_type)
        self.service_type_label.grid(row=2, column=0)



    def update_order_item_summary(self):
        self.check_required_options()
        first_sauce_text = f"\n{self.order_item.first_sauce['sauce']}" if self.order_item.first_sauce else ""
        second_sauce_text = f"\n{self.order_item.second_sauce['sauce']}" if self.order_item.second_sauce else ""
        side_text = f"\n{self.order_item.side['side']}" if self.order_item.side else ""
        drink_text = f"\n{self.order_item.drink['drink']}" if self.order_item.drink else ""
        extra_sauces_text = "\n" + "\n".join(
            [f"{(s['sauce'], s['price'])}" for s in self.order_item.extra_sauces]) if self.order_item.extra_sauces else ""
        note_text = f"\n{self.order_item.item_note}" if self.order_item.item_note else ""


        label_text = f"{self.order_item.item_name} ({self.order_item.base_price}){first_sauce_text}{second_sauce_text}{side_text}{drink_text}{extra_sauces_text}{note_text}"


        self.order_item_label = Label(self.order_item_summary, width=28, pady=5, anchor='w',
                                      text=f'1  {label_text}', font=tkFont.Font(size=15),
                                      highlightbackground='blue', highlightcolor='blue', highlightthickness=1)
        self.order_item_label.grid(row=5, column=0, pady=15, padx=5)




        ...

class ScratchSauceWindow:
    def __init__(self, sauce, menu):
        self.menu = menu
        self.sauce = sauce
        self.order_item = OrderItem(sauce,'Sauces',self.menu, self)



        self.initiate_window_display()

    def initiate_window_display(self):
        self.window = ModificationWindow(self.menu, self.order_item, self)


class TenderMealWindow:

    def __init__(self, meal, menu):
        self.menu = menu
        self.meal = meal
        self.order_item = OrderItem(meal, 'Meals', self.menu, self)

        self.initiate_window_display()
    def initiate_window_display(self):
        self.window = ModificationWindow(self.menu,self.order_item, self)

class SandwichMealWindow:
    def __init__(self, meal, menu):
        self.menu = menu
        self.meal = meal
        self.order_item = OrderItem(meal, 'Sandwiches', self.menu, self)

        self.initiate_window_display()

    def initiate_window_display(self):
        self.window = ModificationWindow(self.menu, self.order_item, self)

class SaladWindow:
    def __init__(self, meal, menu):
        self.menu = menu
        self.meal = meal
        self.order_item = OrderItem(meal, 'Salad', self.menu, self)

        self.initiate_window_display()

    def initiate_window_display(self):
        self.window = ModificationWindow(self.menu, self.order_item, self)

class KidsMealWindow:
    def __init__(self, meal, menu):
        self.menu = menu
        self.meal = meal
        self.order_item = OrderItem(meal, 'Kids Meals', self.menu, self)

        self.initiate_window_display()

    def initiate_window_display(self):
        self.window = ModificationWindow(self.menu, self.order_item, self)





















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
                "Citybird - Sandwich Only": 7.49,
                "Lemon Thyme - Sandwich Only": 7.49,
                "Spicy - Sandwich Only": 7.49,
                "Buffalo Bleu - Sandwich Only": 7.49,
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
                "Sriracha Mayo": 0.75,
                "Hot Honey": 1.00,
                "Citybird Vinaigrette": 0.75,
                "8oz City Sauce": 5.00,
                "8oz Lemon Thyme Ranch": 5.00,
                "8oz Honey Dijon": 5.00,
                "8oz Buffalo Bleu": 5.00,
                "8oz Hickory BBQ": 5.00,
                "8oz Sriracha Mayo": 5.00,
                "8oz Hot Honey": 5.00,
                '8oz Citybird Vinaigrette':5.00
            },
            "Drinks": {
                "Root Beer":2.69,
                "Coke": 2.69,
                "Diet Coke":2.69,
                "Coke Zero": 2.69,
                "Sprite": 2.69,
                "Iced Tea": 2.69,
                "Seasonal Tea": 2.69,
                "Lemonade":2.69,
                "Tap Water" :0.00,
                "Bottle Water": 2.69,
                "Smart Water": 2.69,
                "Juice & Wikki Stix": 2.69,
                "Milk & Wikki Stix": 2.69,
                'Fountain Drink & Wikki Stix': 2.69,
                "Lemon Lacroix": 2.69,
                'Grapefruit Lacroix': 2.69,
                "Milk": 2.69,
                "Kid- Juice Pouch": 2.69
            },
            "Salad":{
                '1/2 Salad':3.49,
                "Salad":7.99
                     }
        }
        self.create_frames()
        self.populate_menu_items_frame()
        self.populate_bottom_row_frame()

    def navigate_to(self, window, item_name):
        self.menu_items_canvas.destroy()
        self.bottom_row_frame.destroy()
        self.order.order_summary_canvas.destroy()
        window(item_name, self)

    def kill_frames(self):
        self.menu_items_canvas.destroy()
        self.bottom_row_frame.destroy()
        self.order.order_summary_canvas.destroy()

    def initiate_main_menu_display(self):
        self.create_frames()
        self.order.create_order_summary_frame()
        self.populate_frames()








    def create_frames(self):
        #initiated once

        self.frame_color_bg = '#1e1e1e'





        self.menu_items_canvas = Canvas(self.root, bg=self.frame_color_bg, width=1580, height=925)
        self.menu_items_scrollbar = Scrollbar(self.root, orient="vertical", command=self.menu_items_canvas.yview)
        self.menu_items_frame = Frame(self.menu_items_canvas, bg=self.frame_color_bg)

        # Bind the inner frame to the canvas
        self.menu_items_frame.bind("<Configure>", lambda e: self.menu_items_canvas.configure(
            scrollregion=self.menu_items_canvas.bbox("all")))

        # Create a window in the canvas to hold the inner frame
        self.menu_items_canvas.create_window((0, 0), window=self.menu_items_frame, anchor="nw")

        # Configure the canvas to use the scrollbar
        self.menu_items_canvas.configure(yscrollcommand=self.menu_items_scrollbar.set)

        # Place the canvas and the scrollbar in the grid
        self.menu_items_canvas.grid(column=2, row=0, sticky='nsew')
        self.menu_items_scrollbar.grid(column=3, row=0, sticky='ns')





        #dont know where else to put this label, needs to be initiated once






        self.bottom_row_frame = LabelFrame(self.root, bg=self.frame_color_bg,text = "Random stuff", width=1920,height=175)
        self.bottom_row_frame.grid(column=0,row=1, columnspan=4)
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
        carryout = Button(self.menu_items_frame, text = '--CARRYOUT--',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:OrderItem('--CARRY OUT--','service', self))
        rename = Button(self.menu_items_frame, text = 'Rename',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda: self.order.rename_order())

        dine_in.grid(column=0, row=0, padx = button_padx, pady = button_pady)
        carryout.grid(column=1, row=0, padx = button_padx, pady = button_pady)
        rename.grid(column=2, row=0, padx = button_padx, pady = button_pady)



        #beverage label


        #drink options
        self.drinks = ("Coke", "Coke Zero","Root Beer","Diet Coke", "Grapefruit Lacroix", "Iced Tea", "Lemon Lacroix", "Lemonade", "Seasonal Tea", "Smart Water","Sprite","Tap Water")
        for index, drink in enumerate(self.drinks):
            drink_button = Button(self.menu_items_frame, text=drink,height = button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda d=drink: OrderItem(d,'Drinks', self))
            drink_button.grid(column=index, row=2)



        #sandwich only options
        self.sandwich_only = ("Citybird - \nSandwich Only", "Lemon Thyme - \nSandwich Only", "Spicy - \nSandwich Only", "Buffalo Bleu - \nSandwich Only")

        for index, sandwich in enumerate(self.sandwich_only):
            sandwich_only_button = Button(self.menu_items_frame, text=sandwich,height = button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda s=sandwich: OrderItem(s.replace("\n",""),'Sandwiches', self))
            sandwich_only_button.grid(column=index, row=15)







        #tender meal options
        snack_pack = Button(self.menu_items_frame, text="Snack Pack(4)",height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,font=self.button_font, command=lambda: self.navigate_to(TenderMealWindow,'Snack Pack'))
        medium_pack = Button(self.menu_items_frame, text = 'Medium Pack(6)',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:self.navigate_to(TenderMealWindow,'Medium Pack'))
        large_pack = Button(self.menu_items_frame, text = 'Large Pack(8)',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:self.navigate_to(TenderMealWindow,'Large Pack'))
        mega_pack = Button(self.menu_items_frame, text = 'Mega Pack(10)',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:self.navigate_to(TenderMealWindow,'Mega Pack'))
        on_side_tenders = Button(self.menu_items_frame, text = 'On Side Tenders',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')

        snack_pack.grid(column=0, row=4, padx = button_padx, pady = button_pady)
        medium_pack.grid(column=1, row=4, padx = button_padx, pady = button_pady)
        large_pack.grid(column=2, row=4, padx = button_padx, pady = button_pady)
        mega_pack.grid(column=3, row=4, padx = button_padx, pady = button_pady)
        on_side_tenders.grid(column=4, row=4, padx = button_padx, pady = button_pady)






        #sandwich meal options
        buffalo_blue_sandwich = Button(self.menu_items_frame,text='Buffalo Bleu\n Sandwich', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:self.navigate_to(SandwichMealWindow,'Buffalo Bleu Sandwich'))
        citybird_sandwich = Button(self.menu_items_frame, text = 'CityBird \nSandwich',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        lemon_thyme_sandwich = Button(self.menu_items_frame, text = 'Lemon\nThyme\nSandwich',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')
        spicy_sandwich = Button(self.menu_items_frame, text = 'Spicy\nSandwich',height= button_height, width = button_width, fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:'')

        buffalo_blue_sandwich.grid(column=0, row=6, padx = button_padx, pady = button_pady)
        citybird_sandwich.grid(column=1, row=6, padx = button_padx, pady = button_pady)
        lemon_thyme_sandwich.grid(column=2, row=6, padx = button_padx, pady = button_pady)
        spicy_sandwich.grid(column=3, row=6, padx = button_padx, pady = button_pady)





        #salad button
        salad = Button(self.menu_items_frame, text='Salad',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:self.navigate_to(SaladWindow,'Salad'))
        salad.grid(column=0, row=8, padx = button_padx, pady = button_pady)





        #kids meal options
        kids_2_tender = Button(self.menu_items_frame, text='Kids 2\nTenders',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda: self.navigate_to(KidsMealWindow, 'Kids 2 Tenders'))
        kids_sandwich = Button(self.menu_items_frame, text='Kids\nSandwich',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:'')
        kid_juice_pouch = Button(self.menu_items_frame, text='Kid-Juice\nPouch',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:OrderItem('Kid- Juice Pouch','Drinks',self))
        kid_milk = Button(self.menu_items_frame,text='Kid- Milk', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:OrderItem('Milk', 'Drinks',self))
        apple_sauce = Button(self.menu_items_frame, text='Apple\nSauce',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:OrderItem('Apple Sauce', 'Sides', self))
        pickles = Button(self.menu_items_frame, text='Pickles',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font, command=lambda:OrderItem('Pickles','Sides',self))


        kids_2_tender.grid(column=0, row=10, padx = button_padx, pady = button_pady)
        kids_sandwich.grid(column=1, row=10, padx = button_padx, pady = button_pady)
        kid_juice_pouch.grid(column=2, row=10, padx = button_padx, pady = button_pady)
        kid_milk.grid(column=3, row=10, padx = button_padx, pady = button_pady)
        apple_sauce.grid(column=4, row=10, padx = button_padx, pady = button_pady)
        pickles.grid(column=5, row=10, padx = button_padx, pady = button_pady)




        #side options
        half_salad = Button(self.menu_items_frame,text='(1/2) Salad', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font,command=lambda: self.navigate_to(SaladWindow, '1/2 Salad'))
        apple_sauce = Button(self.menu_items_frame, text='Apple\nSauce',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:OrderItem('Apple Sauce', 'Sides', self))
        bun = Button(self.menu_items_frame,text='Bun', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:OrderItem('Bun','Sides', self))
        fries = Button(self.menu_items_frame, text='Fries',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font,command=lambda:OrderItem('Fries','Sides',self))
        pickles = Button(self.menu_items_frame,text='Pickles', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,  font=self.button_font,command=lambda:OrderItem('Pickles','Sides',self))
        slaw = Button(self.menu_items_frame, text='Slaw',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font, command=lambda:OrderItem('Slaw','Sides',self))
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
        city_sauce = Button(self.menu_items_frame, text='City Sauce',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:self.navigate_to(ScratchSauceWindow,'City Sauce'))
        citybird_vinaigrette = Button(self.menu_items_frame, text='Citybird\n Vinaigrette',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:self.navigate_to(ScratchSauceWindow,'Citybird Vinaigrette'))
        hickory_bbq = Button(self.menu_items_frame, text='Hickory\nBBQ',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,font=self.button_font, command=lambda:self.navigate_to(ScratchSauceWindow,'Hickory BBQ'))
        honey_dijon = Button(self.menu_items_frame,text='Honey Dijon', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg,font=self.button_font, command=lambda:self.navigate_to(ScratchSauceWindow,'Honey Dijon'))
        hot_honey = Button(self.menu_items_frame, text='Hot Honey',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:self.navigate_to(ScratchSauceWindow,'Hot Honey'))
        lemon_thyme_ranch = Button(self.menu_items_frame, text='Lemon Thyme Ranch',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:self.navigate_to(ScratchSauceWindow,'Lemon Thyme Ranch'))
        sriracha_mayo = Button(self.menu_items_frame,text='Sriracha\nMayo', height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:self.navigate_to(ScratchSauceWindow,'Sriracha Mayo'))
        sriracha_mayo_c = Button(self.menu_items_frame, text='Sriracha\nMayo C',height = button_height, width = button_width,fg= self.button_colorfg, bg= self.button_colorfg, font=self.button_font,command=lambda:self.navigate_to(ScratchSauceWindow,'Sriracha Mayo'))

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








