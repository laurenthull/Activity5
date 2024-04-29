import pymongo
from datetime import datetime

# MongoDB connection details
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["pizza_database"]

# Data to insert into collections
pizza_sizes = [
    {"SizeID": 1, "SizeName": "Small", "Price": 8.99},
    {"SizeID": 2, "SizeName": "Medium", "Price": 10.99},
    {"SizeID": 3, "SizeName": "Large", "Price": 12.99},
    {"SizeID": 4, "SizeName": "Extra Large", "Price": 14.99}
]

toppings = [
    {"ToppingID": 1, "ToppingName": "Pepperoni", "Price": 1.50},
    {"ToppingID": 2, "ToppingName": "Sausage", "Price": 1.50},
    {"ToppingID": 3, "ToppingName": "Peppers", "Price": 1.00},
    {"ToppingID": 4, "ToppingName": "Onions", "Price": 1.00},
    {"ToppingID": 5, "ToppingName": "Chicken", "Price": 2.00}
]

pizza_styles = [
    {"StyleID": 1, "StyleName": "New York", "Price": 0.00},
    {"StyleID": 2, "StyleName": "Chicago", "Price": 0.00},
    {"StyleID": 3, "StyleName": "Flatbread", "Price": 0.00}
]

crust_types = [
    {"CrustID": 1, "CrustName": "Plain", "Price": 0.00},
    {"CrustID": 2, "CrustName": "Stuffed", "Price": 2.00}
]

pizzas = [
    {
        "PizzaID": 1,
        "SizeID": 1,
        "Toppings": [
            {"ToppingName": "Pepperoni", "Price": 1.50},
            {"ToppingName": "Sausage", "Price": 1.50},
            {"ToppingName": "Peppers", "Price": 1.00},
            {"ToppingName": "Onions", "Price": 1.00}
        ],
        "StyleID": 1,
        "CrustID": 1
    }
]

sales = [
    {"SaleID": 1, "PizzaID": 1, "Quantity": 2, "TotalPrice": 17.98, "SaleDate": datetime.now()}
]

# Insert data into MongoDB collections
db.pizza_sizes.insert_many(pizza_sizes)
db.toppings.insert_many(toppings)
db.pizza_styles.insert_many(pizza_styles)
db.crust_types.insert_many(crust_types)
db.pizzas.insert_many(pizzas)
db.sales.insert_many(sales)

print("Data inserted successfully into MongoDB.")

