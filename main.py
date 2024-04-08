import tkinter as tk
import uuid
from tkinter import messagebox
import mysql.connector

class PizzaOrderApp:
    def __init__(self, master, connection):
        self.master = master
        self.connection = connection
        self.master.title("Pizza Ordering System")

        self.size_var = tk.StringVar()
        self.topping_vars = []
        self.style_var = tk.StringVar()
        self.crust_var = tk.StringVar()
        self.quantity_var = tk.IntVar(value=1)

        # Pizza size
        size_label = tk.Label(master, text="Select Size:")
        size_label.grid(row=0, column=0, sticky="w")

        # Fetch sizes from the database
        self.size_options = self.get_db_options("PizzaSizes", "SizeName")
        for i, size in enumerate(self.size_options):
            btn = tk.Button(master, text=size, command=lambda s=size: self.size_var.set(s))
            btn.grid(row=0, column=i+1, sticky="w")

        # Toppings
        topping_label = tk.Label(master, text="Select Toppings:")
        topping_label.grid(row=1, column=0, sticky="w")

        # Fetch toppings from the database
        self.topping_options = self.get_db_options("Toppings", "ToppingName")
        for i, option in enumerate(self.topping_options):
            var = tk.IntVar(value=0)
            cb = tk.Checkbutton(master, text=option, variable=var)
            cb.grid(row=i + 1, column=1, sticky="w")
            self.topping_vars.append(var)

        # Pizza style
        style_label = tk.Label(master, text="Select Style:")
        style_label.grid(row=len(self.topping_options) + 2, column=0, sticky="w")

        # Fetch styles from the database
        self.style_options = self.get_db_options("PizzaStyles", "StyleName")
        for i, style in enumerate(self.style_options):
            btn = tk.Button(master, text=style, command=lambda s=style: self.style_var.set(s))
            btn.grid(row=len(self.topping_options) + 2, column=i+1, sticky="w")

        # Crust type
        crust_label = tk.Label(master, text="Select Crust:")
        crust_label.grid(row=len(self.topping_options) + 2, column=0, sticky="w")

        # Fetch crusts from the database
        self.crust_options = self.get_db_options("CrustTypes", "CrustName")
        for i, crust in enumerate(self.crust_options):
            btn = tk.Button(master, text=crust, command=lambda c=crust: self.crust_var.set(c))
            btn.grid(row=len(self.topping_options) + 3, column=i+1, sticky="w")

        # Quantity
        quantity_label = tk.Label(master, text="Quantity:")
        quantity_label.grid(row=len(self.topping_options) + 3, column=0, sticky="w")

        self.quantity_entry = tk.Entry(master, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=len(self.topping_options) + 3, column=1, sticky="w")

        # Order button
        order_button = tk.Button(master, text="Place Order", command=self.place_order)
        order_button.grid(row=len(self.topping_options) + 4, columnspan=2, pady=10)

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


    def place_order(self):
        # Get selected options
        size = self.size_var.get()
        toppings = [self.topping_options[i] for i, var in enumerate(self.topping_vars) if var.get() == 1]
        style = self.style_var.get()
        crust = self.crust_var.get()
        quantity = self.quantity_var.get()

        # Fetch prices for selected options
        size_price = self.get_price("PizzaSizes", "Price", "SizeName", size)
        topping_prices = sum(self.get_price("Toppings", "Price", "ToppingName", topping) for topping in toppings)
        style_price = self.get_price("PizzaStyles", "Price", "StyleName", style)
        crust_price = self.get_price("CrustTypes", "Price", "CrustName", crust)

        total_price = (size_price + topping_prices + style_price + crust_price) * quantity

        # Insert the pizza into the Pizzas table
        pizza_id = self.insert_pizza(size, toppings, style, crust)

        # Generate a unique sale ID
        sale_id = str(uuid.uuid4())

        # Insert the sale into the Sales table
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO Sales (SaleID, PizzaID, Quantity, TotalPrice, SaleDate) VALUES (%s, %s, %s, %s, NOW())",
            (sale_id, pizza_id, quantity, total_price))
        self.connection.commit()
        cursor.close()
        messagebox.showinfo("Order Placed", "Your order has been placed.")

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


if __name__ == "__main__":
    # Creating connection object
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="cytyttyn2",
        database="Pizza"  # Change this to your database name
    )

    root = tk.Tk()
    app = PizzaOrderApp(root, mydb)
    root.mainloop()
