

from tkinter import *
import tkinter.font as tkFont



def initiate_main_window(root):
    width = 1920  # Width of the monitor
    height = 1080  # Height of the monitor
    x_offset = 1920  # Start at the right edge of the primary monitor
    y_offset = 0  # Start at the top of the screen
    root.configure(bg="black")
    root.title("CityBird POS System")
    root.geometry(f"{width}x{height}+{0}+{y_offset}")

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
        self.update_order_display_summary()
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
        self.order_summary_canvas = Canvas(self.root, bg=self.frame_color_bg, width=300, height = 980)
        self.order_summary_scrollbar = Scrollbar(self.root, orient='vertical', command= self.order_summary_canvas.yview)
        self.order_summary_frame = Frame(self.order_summary_canvas, bg= self.frame_color_bg)


        #Bind the inner frame to the canvas
        self.order_summary_frame.bind('<Configure>',lambda e: self.order_summary_canvas.configure(scrollregion = self.order_summary_canvas.bbox('all')))

        self.order_summary_canvas.create_window((0,0), window = self.order_summary_frame, anchor='nw')

        self.order_summary_canvas.configure(yscrollcommand=self.order_summary_scrollbar.set)

        #place the canvas and scrollbar in the grid
        self.order_summary_canvas.grid(column=0, row=0)
        self.order_summary_scrollbar.grid(column=1, row=0, sticky='ns')




        self.name_label = Label(self.order_summary_frame, text='Quick Sale', width=26, font=tkFont.Font(size=18), bg=self.frame_color_bg)

        self.name_label.grid(row=0, column=0, padx=0,sticky='nsew')

        self.order_label = Label(self.order_summary_frame, bg=self.frame_color_bg, text=self.order_name,
                                width=26, font=tkFont.Font(size=18))
        self.name_label.grid(row=0, column=0, padx=0)


        self.balance_due_label = Label(self.order_summary_frame, text=f'balance due:{self.balance_due:.2f}', bg=self.frame_color_bg)
        self.balance_due_label.grid(column=0, row=1000)



        self.update_balance_due()


    def item_action_window(self, order_item):
        self.item_option_window = Toplevel(root)
        self.item_option_window.geometry('+1920+0')
        self.item_option_window.title(f"{order_item.item_name}")



        self.remove_item_button = Button(self.item_option_window,text='Remove Item', command=lambda: self.remove_item(order_item),padx=25,pady=30)
        self.remove_item_button.grid(row=0, column=0)


        if order_item.first_sauce or order_item.side or order_item.drink or order_item.item_type == 'Sauces':
            self.modify_item_button = Button(self.item_option_window, text= 'Modify Item', command=lambda:self.modify_item(order_item),padx=25,pady=30)
            self.modify_item_button.grid(row=0, column=1)

    def update_order_display_summary(self):
        self.update_balance_due()


        if not self.order_summary_frame.winfo_exists():
            return

            #clears order summary frame
        for button in self.item_summary_buttons:
            button.destroy()
        self.name_label.configure(text=self.order_name)
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

            button_text = f"{item.item_name} ({item.base_price:.2f})\n{first_sauce_text}{second_sauce_text}{side_text}{drink_text}{extra_sauces_text}{note_text}"

            # Create the button
            order_item_button = Button(self.order_summary_frame, text=button_text, font=('Coolvetica','15'), height=0, width=50,
                                       padx=0, pady=5,
                                       command=lambda item=item: self.item_action_window(
                                           item))  # This lambda captures the current item value
            order_item_button.grid(column=0, row=index+1)
            self.item_summary_buttons.append(order_item_button)

        #updates balance due label
        self.balance_due_label.config(text=f'Balance Due: {self.balance_due:.2f}')










class OrderItem:
    def __init__(self, item_name, item_type, menu, window=True):

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





        self.item_type = item_type
        if window==True:
            self.menu.kill_frames()

            self.window = ModificationWindow(self.menu, self, self.item_name)





        #saves a reference to current order, to send itself to add_item




    def update_item_name(self, name):
        self.item_name = name
        self.base_price = self.menu.menu[self.item_type][self.item_name]
        self.total_price = self.base_price
        print(self.base_price)
        print(self.total_price)
        self.window.update_order_item_summary()

    def add_item_note(self, note):
        self.item_note = ''
        self.item_note += note
        print(self.item_note)


        self.window.update_order_item_summary()


    def add_first_sauce(self, sauce):
        if sauce == "Hot Honey":
            price = self.menu.menu['Sauces'][sauce]
        else:
            price = 0
        self.first_sauce = {'sauce':sauce,'price':price}

        self.calculate_total_price()

        self.window.update_order_item_summary()

    def add_second_sauce(self,sauce):
        if sauce == "Hot Honey":
            price = self.menu.menu['Sauces'][sauce]
        else:
            price = 0
        self.second_sauce = {'sauce': sauce, 'price': price}

        self.calculate_total_price()

        self.window.update_order_item_summary()

    def add_extra_sauce(self,sauce):
        sauce_index = next((index for (index, d) in enumerate(self.extra_sauces) if d['sauce'] == sauce), None)

        if sauce_index is not None:
            # If the sauce is present, remove the dictionary from the list
            self.extra_sauces.pop(sauce_index)
        else:
            # If the sauce is not present, add it to the list
            self.extra_sauces.append({'sauce': sauce, 'price': self.menu.menu['Sauces'][sauce]})
        self.calculate_total_price()
        self.window.update_order_item_summary()





    def add_sides(self, side):
        #check for redundent code later on


        #handles side logic for tender meals
        if self.item_type == 'Meals'or self.item_type == 'Sandwiches':
            if side in ('1/2 Salad','1/2 salad (Honey Dijon)','1/2 salad (ranch)','1/2 Salad (Vinaigrette)'):
                price = 1.49

            else:
                price = 0



        elif self.item_type == 'Kids meal':
            price = 0

        elif self.item_type == 'Salad':
            if side == 'No Tenders':
                price = 0
            else:
                price = self.menu.menu['Sides'][side]




        else:
            price = 0
        self.side = {'side': side, 'price': price}



        self.calculate_total_price()
        self.window.update_order_item_summary()






    def add_drink(self, drink):

        if drink in ("No Drink", "Tap Water") or self.item_type == 'Kids Meals':
            price = 0
        else:
            price = 1.00




        self.drink = {'drink': drink, 'price':price}
        self.calculate_total_price()

        self.window.update_order_item_summary()

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
    def __init__(self, menu, order_item, item_name):

        self.item_name = item_name
        self.menu = menu
        self.order_item = order_item

        #style
        self.frame_color_bg = '#1e1e1e'
        self.mod_button_font = tkFont.Font(size=15)


        self.initiate_window_display()



    def initiate_window_display(self):
        self.upper_frame = LabelFrame(self.menu.root, bg=self.frame_color_bg, width=1620,
                                      height=100, padx=0, pady=10)
        self.upper_frame.grid(column=1, row=0)
        self.upper_frame.grid_propagate(False)

        self.order_item_summary = LabelFrame(self.menu.root, bg=self.frame_color_bg,
                                             width=300,
                                             height=1080, padx=0, pady=0)
        self.order_item_summary.grid(column=0, row=0, rowspan=2)
        self.order_item_summary.grid_propagate(False)

        self.modification_selection_frame = Frame(self.menu.root, bg=self.frame_color_bg,
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
        button = Button(parent, text=text, height=3,
                        width=10, fg=self.menu.button_colorfg, bg=self.menu.button_colorfg,
                        font=('Coolvetica',20),
                        command=command)
        button.grid(row=row, column=column,sticky='nsew')
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
                        width=14, fg=self.menu.button_colorfg, bg=self.menu.button_colorfg,
                        font=self.mod_button_font,
                        command=command)
        button.grid(row=row, column=column, pady=20)
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
        self.individual_sauce_button = self.create_modification_button(self.modification_selection_frame, 'Individual Sauce', 0,0,lambda: self.order_item.update_item_name(self.item_name))

        self.catering_sauce_button = self.create_modification_button(self.modification_selection_frame, 'Party Size (8oz)',0,1, lambda: self.order_item.update_item_name(f'8oz {self.item_name}'))




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
        self.service_type_label.grid(row=2, column=0, sticky='w')



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

        self.menu_items_canvas = Canvas(self.root, bg=self.frame_color_bg, width=1580, height=980)
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

        self.bottom_row_frame = Frame(self.root, bg=self.frame_color_bg, width=1920, height=100)
        self.bottom_row_frame.grid(column=0,row=1, columnspan=4)
        self.bottom_row_frame.grid_propagate(False)



    def populate_frames(self):
        self.populate_menu_items_frame()
        self.populate_bottom_row_frame()
        self.order.update_order_display_summary()

    def populate_bottom_row_frame(self):
        ...
    def populate_menu_items_frame(self):

        #button customization
        self.button_width = 10
        self.button_height = 3
        self.button_padx = 0
        self.button_pady = 0,10
        self.button_colorfg = 'black'
        self.button_colorfg = 'black'
        self.button_font= tkFont.Font(font='Coolvetica', size=15)

        #label customization
        self.create_top_row()
        self.create_drink_row()
        self.create_tender_meal_row()
        self.create_sandwich_meal_row()
        self.create_salad_row()
        self.create_kids_meal_row()
        self.create_side_row()
        self.create_sauce_row()
        self.create_sandwich_only_row()
        self.create_menu_labels()

    def create_top_row(self):
        dine_in = self.create_menu_button('--DINE IN--', 0, 0, lambda: OrderItem('--DINE IN--', 'service', self, False),'grey')

        carryout = self.create_menu_button('--CARRYOUT--', 0, 1, lambda: OrderItem('--CARRY OUT--', 'service', self, False),'Grey')

        rename = self.create_menu_button('Rename', 0, 2, lambda: self.order.rename_order(),'grey')
    def create_menu_button(self, name, row, column, command, highlight):
        menu_button = Button(self.menu_items_frame, text=name, height=self.button_height, width=self.button_width,
                        font=('Coolvetica', 20), command=command,pady= 0, borderwidth=1)
        menu_button.grid(row=row, column=column+1, padx=3)
        return menu_button


    def create_drink_row(self):
        self.drinks = (
        "Coke", "Coke Zero", "Root Beer", "Diet Coke", "Grapefruit\n Lacroix", "Iced Tea", "Lemon\n Lacroix", "Lemonade",
        "Seasonal\n Tea", "Smart Water", "Sprite")
        for index, drink in enumerate(self.drinks):
            self.create_menu_button(drink, 2, index, lambda d=drink: OrderItem(d.replace('\n',''), 'Drinks', self, False),'#2F66FF')


    def create_sandwich_only_row(self):
        self.sandwich_only = ("Citybird - \nSandwich Only", "Lemon Thyme - \nSandwich Only", "Spicy - \nSandwich Only",
                              "Buffalo Bleu - \nSandwich Only")

        for index, sandwich in enumerate(self.sandwich_only):
            self.create_menu_button(sandwich, 16, index,
                                    lambda s=sandwich: OrderItem(s.replace("\n", ""), 'Sandwiches', self, False),'blue')


    def create_sauce_row(self):
        self.menu_sauces = (
            'Buffalo \nBleu', 'City Sauce', 'Citybird\n Vinaigrette', 'Hickory \nBBQ', 'Honey Dijon', 'Hot Honey',
            'Lemon \nThyme Ranch', 'Sriracha \nMayo')
        for index, sauce in enumerate(self.menu_sauces):
            self.create_menu_button(sauce, 14, index, lambda s=sauce: OrderItem(s.replace('\n', ''), 'Sauces', self),'blue')


    def create_side_row(self):
        self.sides = ('Apple \nSauce', 'Bun','Fries', 'Pickles','Slaw')
        half_salad = self.create_menu_button('(1/2) Salad', 12, 0, lambda: OrderItem('1/2 Salad', "Salad",self),'lightblue')
        for index, side in enumerate(self.sides):
            self.create_menu_button(side, 12, index+1, lambda s=side: OrderItem(s.replace('\n',''),'Sides', self, False),'lightblue')

    def create_tender_meal_row(self):
        self.tender_meals = ("Snack Pack", "Medium Pack", "Large Pack", "Mega Pack")
        for index, tender_meal in enumerate(self.tender_meals):
            self.create_menu_button(tender_meal, 4, index, lambda m=tender_meal: OrderItem(m, "Meals", self),'yellow')
    def create_sandwich_meal_row(self):
        self.sandwich_meals = ('Buffalo Bleu\n Sandwich', 'Citybird \nSandwich', 'Lemon \nThyme \nSandwich', 'Spicy \nSandwich')
        for index, sandwich_meal in enumerate(self.sandwich_meals):
            self.create_menu_button(sandwich_meal, 6, index, lambda s= sandwich_meal : OrderItem(s.replace('\n',''), 'Sandwiches', self),'red')

    def create_salad_row(self):
        self.create_menu_button('Salad', 8,0, lambda:OrderItem('Salad', 'Salad',self),'green')

    def create_kids_meal_row(self):

        self.create_menu_button('Kids 2\n Tenders', 10, 0, lambda:OrderItem( 'Kids 2 Tenders','Kids Meals', self),'purple')
        self.create_menu_button('Kids\n Sandwich', 10, 1, lambda:OrderItem( 'Kids Sandwich','Kids Meals', self),'purple')

        self.create_menu_button('Kid-Juice\nPouch', 10, 2, lambda:OrderItem('Kid- Juice Pouch','Drinks',self, False),'purple')
        self.create_menu_button('Kid- Milk', 10, 3, lambda:OrderItem('Kid- Milk','Drinks',self, False),'purple')

        self.create_menu_button('Apple\n Sauce', 10,4, lambda:OrderItem('Apple Sauce', 'Sides', self, False),'purple')
        self.create_menu_button('Pickles', 10,5, lambda:OrderItem('Pickles', 'Sides', self, False),'purple')





    def create_menu_labels(self):
        font = tkFont.Font(size=20)
        label_pady = 3
        label_padx = 0
        #color coded
        label = self.create_color_code('blue',2)
        self.create_color_code('yellow',4)
        self.create_color_code('red',6)
        self.create_color_code('green',8)
        self.create_color_code('purple',10)
        self.create_color_code('lightblue',12)
        self.create_color_code('blue',14)
        self.create_color_code('red',16)




        #labels
        beverages = self.create_menu_label('BEVERAGES', 1,0)

        tender_meals = self.create_menu_label('TENDER MEALS', 3, 0,6)

        tender_sandwich_meals = self.create_menu_label('TENDER SANDWICH MEALS', 5, 0,4)
        salad_label = self.create_menu_label('SALAD', 7, 0)
        kids_menu = self.create_menu_label('Kids Menu', 9, 0)
        sides_label = self.create_menu_label('SIDES', 11, 0)
        sauce_label = self.create_menu_label('SAUCES', 13, 0)
        sandwich_only_label = self.create_menu_label('SANDWICH ONLY',15, 0, 4)



    def create_color_code(self,color,row):
        label = Label(self.menu_items_frame,bg=color,padx=3,pady=28)
        label.grid(column=0, row=row)


        ...

    def create_menu_label(self, text, row, column, columnspan=0):
        font = ('Helvetica',22)
        label_pady = 10,3
        label_padx = 0
        label = Label(self.menu_items_frame, text=text, bg=self.frame_color_bg, font=font)
        if columnspan >= 2:
            label.grid(column=column, row=row, columnspan=columnspan, padx=label_padx, pady=label_pady, sticky='w')
        else:
            label.grid(column=column, row=row,  padx=label_padx, pady=label_pady, sticky='w',columnspan=2)





root = Tk()

initiate_main_window(root)

order = Order(root)

root.mainloop()








