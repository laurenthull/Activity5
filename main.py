import pymongo
import uuid
from tkinter import messagebox
from decimal import Decimal
import os
import tkinter as tk
from PIL import Image, ImageTk


class PizzaOrderApp:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.title("Pizza Ordering System")
        self.size_var = tk.StringVar()
        self.topping_vars = []
        self.style_var = tk.StringVar()
        self.crust_var = tk.StringVar()
        self.quantity_var = tk.IntVar(value=1)
        self.cart_items = []

        # Add selected_items_text attribute
        self.selected_items_text = tk.StringVar()

        # Add Cart Text
        self.cart_items_text = tk.StringVar()

        root.configure(bg="white")

        # Add to Cart button

        # Configure rows and columns to expand
        for i in range(6):
            master.grid_rowconfigure(i, weight=1)
        for i in range(6):
            master.grid_columnconfigure(i, weight=1)

        # Pizza size
        size_label = tk.Label(self.master, bg="white", text="Select Size:", font=("Helvetica", 16))
        size_label.grid(row=0, column=0, sticky="w",padx=25)

        def reset_button_colors(button_list):
            for button in button_list:
                button.config(bg="SystemButtonFace")


        self.buttons_size = []
        self.size_options = self.get_db_options("pizza_sizes", "SizeName")


        for i, size in enumerate(self.size_options):
            image_path = f"images/{size}.jpg"
            image = Image.open(image_path)
            image = image.resize((125, 125))
            photo_image = ImageTk.PhotoImage(image)
            btn = tk.Button(master, image=photo_image, compound=tk.TOP,
                            command=lambda s=size: self.select_option("size", s), font=("Helvetica", 16), width=218,
                            height=150)
            btn.image = photo_image
            btn.grid(row= 0, column=i + 1, sticky="w")
            btn.config(bg="SystemButtonFace")
            btn.bind("<Button-1>",lambda event, b=btn: (reset_button_colors(self.buttons_size), b.config(bg="green2")))
            self.buttons_size.append(btn)

        # Initialize toppings
        self.topping_options = self.get_db_options("toppings", "ToppingName")

        # Initialize topping vars
        self.topping_vars = [tk.IntVar() for _ in range(len(self.topping_options))]
        # Toppings
        topping_label = tk.Label(master, bg="white", text="Toppings:", font=("Helvetica", 16))
        topping_label.grid(row=1, column=0, sticky="w",padx=25)

        def toggle_button(button):
            current_color = button.cget("bg")
            if current_color == "green2":
                button.config(bg="SystemButtonFace")
            else:
                button.config(bg="green2")



        self.buttons_toppings = {}

        for i, option in enumerate(self.topping_options):
            image_path = f"images/{option}.jpg"
            image = Image.open(image_path)
            image = image.resize((125, 125))
            photo_image = ImageTk.PhotoImage(image)
            btn = tk.Button(master, image=photo_image, text=option, compound=tk.TOP, font=("Helvetica", 16),
                            command=lambda idx=i: self.toggle_topping(idx), width=218, height=150)
            btn.image = photo_image
            btn.grid(row=1, column=i+1, sticky="w")
            btn.config(bg="SystemButtonFace")
            btn.bind("<Button-1>", lambda event, b=btn: toggle_button(b))
            self.buttons_toppings[option] = btn


        # Pizza style
        style_label = tk.Label(master, bg="white", text="Style:", font=("Helvetica", 16))
        style_label.grid(row=len(self.size_options) + 2, column=0, sticky="w",padx=25)


        self.style_options = self.get_db_options("pizza_styles", "StyleName")
        self.buttons_style = []
        for i, style in enumerate(self.style_options):
            image_path = f"images/{style}.jpeg"
            image = Image.open(image_path)
            image = image.resize((125, 125))
            photo_image = ImageTk.PhotoImage(image)
            btn = tk.Button(master, image=photo_image, text=style, compound=tk.TOP, command=lambda s=style: self.select_option("style", s), font=("Helvetica", 16),width=218, height=150)
            btn.image = photo_image
            btn.grid(row=len(self.size_options) + 2, column=i+1, sticky="w")
            btn.config(bg="SystemButtonFace")
            btn.bind("<Button-1>",lambda event, b=btn: (reset_button_colors(self.buttons_style), b.config(bg="green2")))
            self.buttons_style.append(btn)

        # Crust typed
        crust_label = tk.Label(master, bg="white", text="Crust:", font=("Helvetica", 16))
        crust_label.grid(row=len(self.size_options) + 3, column=0, sticky="w",padx=25)

        self.crust_options = self.get_db_options("crust_types", "CrustName")
        self.buttons_crust = []
        for i, crust in enumerate(self.crust_options):
            image_path = f"images/{crust}.jpg"
            image = Image.open(image_path)
            image = image.resize((125, 125))
            photo_image = ImageTk.PhotoImage(image)
            btn = tk.Button(master, image=photo_image, text=crust, compound=tk.TOP,
                            command=lambda c=crust: self.select_option("crust", c), font=("Helvetica", 16), width=218,
                            height=150)
            btn.image = photo_image
            btn.grid(row=len(self.size_options) + 3, column=i + 1, sticky="w")
            btn.config(bg="SystemButtonFace")
            btn.bind("<Button-1>",lambda event, b=btn: (reset_button_colors(self.buttons_crust), b.config(bg="green2")))
            self.buttons_crust.append(btn)

        # Quantity
        quantity_label = tk.Label(master,bg="white", text="Quantity:", font=("Helvetica", 16))
        quantity_label.grid(row=len(self.size_options) + 4, column=0, sticky="w",padx=25)

        self.quantity_entry = tk.Spinbox(master, textvariable=self.quantity_var, width=5,font=("Helvetica", 25), from_ = 0, to = 50, command=self.calculate_total)
        self.quantity_entry.grid(row=len(self.size_options) + 4, column=1, sticky="w")

        # Total price label
        self.total_price_label = tk.Label(master,bg="white", text="Total Price: $0.00", font=("Helvetica", 20))
        self.total_price_label.grid(row=len(self.size_options) + 3, column=5, columnspan=6, pady=10)

        # Sale button
        sale_button = tk.Button(master, text="Apply Sale (15% Off)", font=("Helvetica", 16), command=self.apply_sale_price, width=20, height=7, highlightbackground= "red", fg="red")
        sale_button.bind("<Button-1>", lambda event, b=sale_button: b.config(bg="green2"))
        sale_button.grid(row=len(self.size_options) + 2, column=5, sticky="w")


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

        # Cart label
        self.cart = tk.Label(master, bg="white",text="Cart:", font=("Helvetica", 16))
        self.cart.grid(row=len(self.size_options) + 6, column=2, columnspan=6, sticky="w",padx=25)

        # Cart items display
        self.cart_display = tk.Label(master, textvariable=self.cart_items_text, font=("Helvetica", 16), wraplength=600, justify="left")
        self.cart_display.grid(row=len(self.size_options) + 7, column=2, columnspan=6, sticky="w",padx=25, pady=15)


    def toggle_topping(self, idx):
        self.topping_vars[idx].set(1 if self.topping_vars[idx].get() == 0 else 0)
        self.calculate_total()
        self.update_selected_items()

    def get_db_options(self, collection_name, field_name):
        collection = self.db[collection_name]
        return [doc[field_name] for doc in collection.find({}, {field_name: 1})]

    def get_price(self, collection_name, condition_column, condition_value):
        collection = self.db[collection_name]
        result = collection.find_one({condition_column: condition_value})
        if result:
            return result["Price"]
        else:
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
        total_price = 0

        for item in self.cart_items:
            size_price = self.get_price("pizza_sizes", "SizeName", item["Size"])
            topping_prices = sum(self.get_price("toppings", "ToppingName", topping) for topping in item["Toppings"])
            style_price = self.get_price("pizza_styles", "StyleName", item["Style"])
            crust_price = self.get_price("crust_types", "CrustName", item["Crust"])
            item_total_price = (size_price + topping_prices + style_price + crust_price) * item["Quantity"]
            total_price += item_total_price

        self.total_price_label.config(text="Total Price: $%.2f" % total_price)

    def add_to_cart(self):
        size = self.size_var.get()
        toppings = [self.topping_options[i] for i, var in enumerate(self.topping_vars) if var.get() == 1]
        style = self.style_var.get()
        crust = self.crust_var.get()
        quantity = self.quantity_var.get()

        self.cart_items.append({"Size": size, "Toppings": toppings, "Style": style, "Crust": crust, "Quantity": quantity})

        self.update_cart_display()

    def place_order(self):
        ordered_items = []

        for item in self.cart_items:
            size = item["Size"]
            toppings = item["Toppings"]
            style = item["Style"]
            crust = item["Crust"]
            quantity = item["Quantity"]

            size_price = self.get_price("pizza_sizes", "SizeName", size)
            topping_prices = sum(self.get_price("toppings", "ToppingName", topping) for topping in toppings)
            style_price = self.get_price("pizza_styles", "StyleName", style)
            crust_price = self.get_price("crust_types", "CrustName", crust)

            total_price = (size_price + topping_prices + style_price + crust_price) * quantity

            pizza_id = self.insert_pizza(size, toppings, style, crust)

            sale_id = str(uuid.uuid4())

            sale_collection = self.db["sales"]
            sale_collection.insert_one({
                "SaleID": sale_id,
                "PizzaID": pizza_id,
                "Quantity": quantity,
                "TotalPrice": total_price
            })

            pizza_collection = self.db["pizzas"]
            pizza_collection.insert_one({
                "Size": size,
                "Toppings": toppings,
                "Style": style,
                "Crust": crust,
                "Quantity": quantity
            })

            ordered_items.append(
                f"Size: {size}, Toppings: {', '.join(toppings)}, Style: {style}, Crust: {crust}, Quantity: {quantity}")

        messagebox.showinfo("Order Placed", "\n".join(ordered_items))

        self.reset_ui()
        self.cart_items = []
        self.update_cart_display()

    def insert_pizza(self, size, toppings, style, crust):
        pizza_collection = self.db["pizza_database"]

        size_result = pizza_collection.find_one({"SizeName": size})
        style_result = pizza_collection.find_one({"StyleName": style})
        crust_result = pizza_collection.find_one({"CrustName": crust})

        pizza_id = None

        if size_result and style_result and crust_result:
            pizza = {
                "SizeID": size_result["_id"],
                "Toppings": [pizza_collection.find_one({"ToppingName": topping})["_id"] for topping in toppings],
                "StyleID": style_result["_id"],
                "CrustID": crust_result["_id"]
            }
            result = pizza_collection.insert_one(pizza)
            pizza_id = result.inserted_id

        return pizza_id

    def apply_sale_price(self):
        size_price = self.get_price("pizza_sizes", "SizeName", self.size_var.get())
        topping_prices = sum(self.get_price("toppings", "ToppingName", topping) for i, topping in enumerate(self.topping_options) if self.topping_vars[i].get() == 1)
        style_price = self.get_price("pizza_styles", "StyleName", self.style_var.get())
        crust_price = self.get_price("crust_types", "CrustName", self.crust_var.get())
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

    def update_cart_display(self):
        cart_display_text = ""
        for item in self.cart_items:
            cart_display_text += f"Size: {item['Size']}, Toppings: {', '.join(item['Toppings'])}, Style: {item['Style']}, Crust: {item['Crust']}, Quantity: {item['Quantity']}\n"
        self.cart_items_text.set(cart_display_text)
        self.reset_ui()
        self.calculate_total()

    def reset_ui(self):
        self.size_var.set("")
        for var in self.topping_vars:
            var.set(0)
        self.style_var.set("")
        self.crust_var.set("")
        self.selected_items_text.set("")
        self.quantity_var.set(1)

        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="SystemButtonFace")


if __name__ == "__main__":
    # Establishing MongoDB connection
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["pizza_database"]

    root = tk.Tk()
    app = PizzaOrderApp(root, db)
    root.mainloop()
