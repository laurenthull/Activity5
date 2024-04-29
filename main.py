import uuid
from tkinter import messagebox
import mysql.connector
from decimal import Decimal
import os
import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk


class PizzaOrderApp:
    def __init__(self, master, connection):
        self.master = master
        self.connection = connection
        self.master.title("Pizza Ordering System")
        self.size_var = tk.StringVar()
        self.topping_vars = []  # Changed to list of IntVars for topping selection
        self.style_var = tk.StringVar()
        self.crust_var = tk.StringVar()
        self.quantity_var = tk.IntVar(value=1)
        self.cart_items = []  # List to store cart items



        # Add selected_items_text attribute
        self.selected_items_text = tk.StringVar()

        # Add Cart Text
        self.cart_items_text = tk.StringVar()

        root.configure(bg="white")

        # Add to Cart button


        # Configure rows and columns to expand
        for i in range(6):  # Assuming 6 rows are being used
            master.grid_rowconfigure(i, weight=1)
        for i in range(6):  # Assuming 6 columns are being used
            master.grid_columnconfigure(i, weight=1)

        # Pizza size
        size_label = tk.Label(self.master, bg="white", text="Select Size:", font=("Helvetica", 16))
        size_label.grid(row=0, column=0, sticky="w",padx=25)


        def reset_button_colors(button_list):
            for button in button_list:
                button.config(bg="SystemButtonFace")

        self.buttons_size = []

        # Fetch sizes from the database
        self.size_options = self.get_db_options("PizzaSizes", "SizeName")
        for i, size in enumerate(self.size_options):
            image_path = f"C:/Users/luke/Documents/GitHub/Activity5/images/{size}.jpg"  # Adjust the path for your folder structure
            image = Image.open(image_path)
            image = image.resize((125, 125))  # Resize the image
            photo_image = ImageTk.PhotoImage(image)
            btn = tk.Button(master, image=photo_image, compound=tk.TOP,
                            command=lambda s=size: self.select_option("size", s), font=("Helvetica", 16), width=218,
                            height=150)
            btn.image = photo_image  # Keep a reference to the image
            btn.grid(row= 0, column=i + 1, sticky="w")
            btn.config(bg="SystemButtonFace")  # Set initial color
            btn.bind("<Button-1>",
                     lambda event, b=btn: (reset_button_colors(self.buttons_size), b.config(bg="green2")))
            self.buttons_size.append(btn)  # Store the button and its state


        # Initialize toppings
        self.topping_options = self.get_db_options("Toppings", "ToppingName")

        # Initialize topping vars
        self.topping_vars = [tk.IntVar() for _ in range(len(self.topping_options))]

        # Toppings
        topping_label = tk.Label(master, bg="white", text="Toppings:", font=("Helvetica", 16))
        topping_label.grid(row=1, column=0, sticky="w",padx=25)

        def toggle_button(button):
            current_color = button.cget("bg")
            if current_color == "green2":
                button.config(bg="SystemButtonFace")  # Change back to original color
            else:
                button.config(bg="green2")

        ######topping buttons###########
        self.buttons_toppings = {}

        for i, option in enumerate(self.topping_options):
            image_path = f"C:/Users/luke/Documents/GitHub/Activity5/images/{option}.jpg"  # Adjust the path for your folder structure
            image = Image.open(image_path)
            image = image.resize((125, 125))  # Resize the image
            photo_image = ImageTk.PhotoImage(image)
            btn = tk.Button(master, image=photo_image, text=option, compound=tk.TOP, font=("Helvetica", 16),
                            command=lambda idx=i: self.toggle_topping(idx), width=218, height=150)
            btn.image = photo_image  # Keep a reference to the image
            btn.grid(row=1, column=i+1, sticky="w")
            btn.config(bg="SystemButtonFace")  # Set initial color
            btn.bind("<Button-1>", lambda event, b=btn: toggle_button(b))  # Toggle color on click
            self.buttons_toppings[option] = btn  # Store the button and its state




        # Pizza style
        style_label = tk.Label(master, bg="white", text="Style:", font=("Helvetica", 16))
        style_label.grid(row=len(self.size_options) + 2, column=0, sticky="w",padx=25)

        # Fetch styles from the database
        self.buttons_style = []
        self.style_options = self.get_db_options("PizzaStyles", "StyleName")
        for i, style in enumerate(self.style_options):
            image_path = f"C:/Users/luke/Documents/GitHub/Activity5/images/{style}.jpeg"  # Adjust the path for your folder structure
            image = Image.open(image_path)
            image = image.resize((125, 125))  # Resize the image
            photo_image = ImageTk.PhotoImage(image)
            btn = tk.Button(master, image=photo_image, text=style, compound=tk.TOP, command=lambda s=style: self.select_option("style", s), font=("Helvetica", 16),width=218, height=150)
            btn.image = photo_image  # Keep a reference to the image
            btn.grid(row=len(self.size_options) + 2, column=i+1, sticky="w")
            btn.config(bg="SystemButtonFace")  # Set initial color
            btn.bind("<Button-1>",lambda event, b=btn: (reset_button_colors(self.buttons_style), b.config(bg="green2")))
            self.buttons_style.append(btn) # Store the button and its state

            # Crust typed
        crust_label = tk.Label(master, bg="white", text="Crust:", font=("Helvetica", 16))
        crust_label.grid(row=len(self.size_options) + 3, column=0, sticky="w",padx=25)

        self.buttons_crust = []
        # Fetch crusts from the database
        self.crust_options = self.get_db_options("CrustTypes", "CrustName")
        for i, crust in enumerate(self.crust_options):
            image_path = f"C:/Users/luke/Documents/GitHub/Activity5/images/{crust}.jpg"  # Adjust the path for your folder structure
            image = Image.open(image_path)
            image = image.resize((125, 125))  # Resize the image
            photo_image = ImageTk.PhotoImage(image)
            btn = tk.Button(master, image=photo_image, text=crust, compound=tk.TOP,
                            command=lambda c=crust: self.select_option("crust", c), font=("Helvetica", 16), width=218,
                            height=150)
            btn.image = photo_image  # Keep a reference to the image
            btn.grid(row=len(self.size_options) + 3, column=i + 1, sticky="w")
            btn.config(bg="SystemButtonFace")  # Set initial color
            btn.bind("<Button-1>",
                     lambda event, b=btn: (reset_button_colors(self.buttons_style), b.config(bg="green2")))
            self.buttons_crust.append(btn)  # Store the button and its state
        # Quantity
        quantity_label = tk.Label(master,bg="white", text="Quantity:", font=("Helvetica", 16))
        quantity_label.grid(row=len(self.size_options) + 4, column=0, sticky="w",padx=25)

        self.quantity_entry = tk.Spinbox(master, textvariable=self.quantity_var, width=5,font=("Helvetica", 25), from_ = 0, to = 50, command=self.calculate_total)
        self.quantity_entry.grid(row=len(self.size_options) + 4, column=1, sticky="w")

        # Total price label
        self.total_price_label = tk.Label(master,bg="white", text="Total Price: $0.00", font=("Helvetica", 16))
        self.total_price_label.grid(row=len(self.size_options) + 5, column=0, columnspan=6, pady=10)

        # Sale button
        sale_button = tk.Button(master, text="Apply Sale", font=("Helvetica", 16), command=self.apply_sale_price)
        sale_button.bind("<Button-1>", lambda event, b=sale_button: b.config(bg="green2"))  # Change button color on press

        sale_button.grid(row=len(self.size_options) + 4, column=3, sticky="w")

        # Order button
        order_button = tk.Button(master, text="Place Order", font=("Helvetica", 16), command=self.place_order)
        order_button.grid(row=len(self.size_options) + 4, column=5, pady=10)

        # add to cart button
        add_to_cart_button = tk.Button(master, text="Add to Cart", font=("Helvetica", 16), command=self.add_to_cart)
        add_to_cart_button.grid(row=len(self.size_options) + 4, column=4, pady=10)

        # Selected items label
        self.selected_items_label = tk.Label(master, bg="white",text="Your Order:", font=("Helvetica", 16))
        self.selected_items_label.grid(row=len(self.size_options) + 6, column=0, columnspan=6, sticky="w",padx=25)

        # Selected items display
        self.selected_items_display = tk.Label(master, textvariable=self.selected_items_text, font=("Helvetica", 16), wraplength=600, justify="left")
        self.selected_items_display.grid(row=len(self.size_options) + 7, column=0, columnspan=6, sticky="w",padx=25, pady=15)

        ######### cart stuff #############
        #  cart label
        self.cart = tk.Label(master, bg="white",text="Cart:", font=("Helvetica", 16))
        self.cart.grid(row=len(self.size_options) + 6, column=2, columnspan=6, sticky="w",padx=25)

        # cart items display
        self.cart_display = tk.Label(master, textvariable=self.cart_items_text, font=("Helvetica", 16), wraplength=600, justify="left")
        self.cart_display.grid(row=len(self.size_options) + 7, column=2, columnspan=6, sticky="w",padx=25, pady=15)



    def toggle_topping(self, idx):
        self.topping_vars[idx].set(1 if self.topping_vars[idx].get() == 0 else 0)
        self.calculate_total()
        self.update_selected_items()

    def get_db_options(self, table, column):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT {column} FROM {table}")
        return [row[0] for row in cursor.fetchall()]


    def get_price(self, table, price_column, condition_column, condition_value):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT {price_column} FROM {table} WHERE {condition_column} = %s", (condition_value,))
        result = cursor.fetchone()
        if result is not None:
            price = result[0]
            cursor.close()
            return price
        else:
            cursor.close()
            return 0

    def select_option(self, option_type, value):
        if option_type == "size":
            self.size_var.set(value)
        elif option_type == "style":
            self.style_var.set(value)
        elif option_type == "crust":
            self.crust_var.set(value)
        self.calculate_total()
        self.update_selected_items()

    def calculate_total(self):
        size_price = self.get_price("PizzaSizes", "Price", "SizeName", self.size_var.get())
        topping_prices = sum(self.get_price("Toppings", "Price", "ToppingName", self.topping_options[i]) for i, var in enumerate(self.topping_vars) if var.get() == 1)
        style_price = self.get_price("PizzaStyles", "Price", "StyleName", self.style_var.get())
        crust_price = self.get_price("CrustTypes", "Price", "CrustName", self.crust_var.get())
        total_price = (size_price + topping_prices + style_price + crust_price) * self.quantity_var.get()
        self.total_price_label.config(text="Total Price: $%.2f" % total_price)

    def add_to_cart(self):
        size = self.size_var.get()
        toppings = [self.topping_options[i] for i, var in enumerate(self.topping_vars) if var.get() == 1]
        style = self.style_var.get()
        crust = self.crust_var.get()
        quantity = self.quantity_var.get()

        # Add current order to cart
        self.cart_items.append({"Size": size, "Toppings": toppings, "Style": style, "Crust": crust, "Quantity": quantity})

        # Update cart display
        self.update_cart_display()

    def place_order(self):
        ordered_items = []  # List to store ordered items for display in the popup message

        # Iterate over each item in the cart
        for item in self.cart_items:
            size = item["Size"]
            toppings = item["Toppings"]
            style = item["Style"]
            crust = item["Crust"]
            quantity = item["Quantity"]

            # Fetch prices for selected options
            size_price = self.get_price("PizzaSizes", "Price", "SizeName", size)
            topping_prices = sum(self.get_price("Toppings", "Price", "ToppingName", topping) for topping in toppings)
            style_price = self.get_price("PizzaStyles", "Price", "StyleName", style)
            crust_price = self.get_price("CrustTypes", "Price", "CrustName", crust)

            # Calculate total price for the current item
            total_price = (size_price + topping_prices + style_price + crust_price) * quantity

            # Insert the pizza into the Pizzas table and get the pizza ID
            pizza_id = self.insert_pizza(size, toppings, style, crust)

            # Generate a unique sale ID
            sale_id = str(uuid.uuid4())

            # Insert the sale into the Sales table with the total price
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO Sales (SaleID, PizzaID, Quantity, TotalPrice, SaleDate) VALUES (%s, %s, %s, %s, NOW())",
                (sale_id, pizza_id, quantity, total_price))
            self.connection.commit()
            cursor.close()

            # Append the current item to the ordered items list for display in the popup message
            ordered_items.append(
                f"Size: {size}, Toppings: {', '.join(toppings)}, Style: {style}, Crust: {crust}, Quantity: {quantity}")

        # Display the ordered items in the popup message
        messagebox.showinfo("Order Placed", "\n".join(ordered_items))

        # Reset UI and cart items list
        self.reset_ui()
        self.cart_items = []
        self.update_cart_display()

    def insert_pizza(self, size, toppings, style, crust):
        cursor = self.connection.cursor()

        # Get SizeID
        cursor.execute("SELECT SizeID FROM PizzaSizes WHERE SizeName = %s", (size,))
        size_id = cursor.fetchone()[0]

        # Get ToppingIDs
        topping_ids = []
        for topping in toppings:
            cursor.execute("SELECT ToppingID FROM Toppings WHERE ToppingName = %s", (topping,))
            topping_id = cursor.fetchone()[0]
            topping_ids.append(topping_id)

        # Get StyleID
        cursor.execute("SELECT StyleID FROM PizzaStyles WHERE StyleName = %s", (style,))
        style_id = cursor.fetchone()[0]

        # Get CrustID
        cursor.execute("SELECT CrustID FROM CrustTypes WHERE CrustName = %s", (crust,))
        crust_id = cursor.fetchone()[0]

        # Insert into Pizzas table
        cursor.execute("INSERT INTO Pizzas (SizeID, ToppingID, StyleID, CrustID) VALUES (%s, %s, %s, %s)",
                       (size_id, topping_ids[0], style_id, crust_id))
        self.connection.commit()

        # Get the last inserted PizzaID
        cursor.execute("SELECT LAST_INSERT_ID()")
        pizza_id = cursor.fetchone()[0]

        cursor.close()

        return pizza_id

    def apply_sale_price(self):
        # Calculate sale price (15% off regular price)
        size_price = self.get_price("PizzaSizes", "Price", "SizeName", self.size_var.get())
        topping_prices = sum(self.get_price("Toppings", "Price", "ToppingName", self.topping_options[i]) for i, var in enumerate(self.topping_vars) if var.get() == 1)
        style_price = self.get_price("PizzaStyles", "Price", "StyleName", self.style_var.get())
        crust_price = self.get_price("CrustTypes", "Price", "CrustName", self.crust_var.get())
        total_price = (size_price + topping_prices + style_price + crust_price) * self.quantity_var.get()
        self.sale_price = Decimal(total_price) * Decimal('0.85')
        self.total_price_label.config(text="Total Price: $%.2f" % self.sale_price)

    def update_selected_items(self):
        size = self.size_var.get()
        toppings = [self.topping_options[i] for i, var in enumerate(self.topping_vars) if var.get() == 1]
        style = self.style_var.get()
        crust = self.crust_var.get()

        selected_items = f"Size: {size}\nToppings: {', '.join(toppings)}\nStyle: {style}\nCrust: {crust}"
        self.selected_items_text.set(selected_items)

    #######cart function##############
    def update_cart_display(self):
        # Display items in the cart
        cart_display_text = ""
        for item in self.cart_items:
            cart_display_text += f"Size: {item['Size']}, Toppings: {', '.join(item['Toppings'])}, Style: {item['Style']}, Crust: {item['Crust']}, Quantity: {item['Quantity']}\n"
        self.cart_items_text.set(cart_display_text)
        self.reset_ui()


    # resets the UI after ordering
    def reset_ui(self):
        self.size_var.set("")
        for var in self.topping_vars:
            var.set(0)
        self.style_var.set("")
        self.crust_var.set("")
        self.selected_items_text.set("")
        self.quantity_var.set(1)


        # Reset button colors
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="SystemButtonFace")



if __name__ == "__main__":
    # Creating connection object
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SQlt20043",
        database="Pizza"  # Change this to your database name
    )

    root = tk.Tk()
    app = PizzaOrderApp(root, mydb)
    root.mainloop()
