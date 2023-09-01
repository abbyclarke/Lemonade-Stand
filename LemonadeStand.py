import random

class Store:
    """Class for keeping track of items in store"""
    def __init__(self):
        self._items = {}
    
    def add_item(self, store_item):
        self._items[store_item.get_name()] = store_item
    
    def get_item(self, item_name):
        return self._items.get(item_name)
    
    def get_all_items(self):
        return self._items
    
    def buy_item(self, item_name, quantity):
        if item_name in self._items and self._items[item_name].get_quantity() >= quantity:
            self._items[item_name].reduce_quantity(quantity)
            return True
        else:
            container = self._items[item_name].get_container_plural()
            print(f"Not enough ${container} in store")
            return False
    
    def get_prices_with_quantities(self):
        return {item_name: (item.get_price(), item.get_quantity()) for item_name, item in self._items.items()}
    

class StoreItem:
    """Class for keeping track of prices of supplies in store"""
    def __init__(self, name, price, amount_per_container, quantity, container, unit):
        self._name = name
        self._price = price
        self._quantity = quantity
        self._amount_per_container = amount_per_container
        self._container = container
        self._unit = unit
    
    def get_name(self):
        return self._name
    
    def get_price(self):
        return self._price

    def get_quantity(self):
        return self._quantity
    
    def reduce_quantity(self, amount):
        self._quantity -= amount
    
    def restock(self, amount):
        self._quantity += amount
    
    def get_amount_per_container(self):
        return self._amount_per_container
    
    def get_container(self):
        return self._container[0]

    def get_container_plural(self):
        return self._container[1]
    
    def get_unit(self):
        return self._unit[0]

    def get_unit_plural(self):
        return self._unit[1]
    
    def get_unit_price(self):
        return round(self._price / self._amount_per_container, 2)
    
    def update_price(self, new_price):
        self._price = new_price

class Supplies:
    """Class for keeping track of supplies on hand"""
    def __init__(self, store, bank):
        self._items = {}
        self._store = store
        self._bank = bank
    
    def get_amount_per_container(self, item_name):
        store_item = self._store.get_item(item_name)
        if store_item:
            return store_item.get_amount_per_container()
        return None
    
    def get_current_items(self):
        return self._items
    
    def get_total_price(self, item_name, quantity):
        store_item = self._store.get_item(item_name)
        if store_item:
            return store_item.get_price() * quantity
        return None
    
    def buy_item(self, item_name, quantity):
        # for example, 9 lemons per bag
        amount_per_container = self.get_amount_per_container(item_name)
        total_unit_quantity = amount_per_container * quantity
        if amount_per_container:
            total_amount = self.get_total_price(item_name, quantity)
            if total_amount:
                if self._store.buy_item(item_name, quantity):
                    self._bank.record_expense(total_amount)
                    if item_name in self._items:
                        self._items[item_name] += total_unit_quantity
                    else:
                        self._items[item_name] = total_unit_quantity

    def make_menu_item(self, menu_item):
        recipe = menu_item.get_recipe()
        for ingredient, quantity in recipe.items():
            if ingredient in self._items and self._items[ingredient] < quantity:
                print(f"Not enough {ingredient}! ")
                return False
        for ingredient, quantity in recipe.items():
            self._items[ingredient] -= quantity
        return True


class MenuItem:
    """Class that represents menu item to be offered for sale at lemonade stand"""
    def __init__(self, name, selling_price):
        """initializes name and selling price"""
        self._name = name
        self._recipe = {}
        self._selling_price = selling_price
        self._quantity = 0
        self._servings = 0

    def get_name(self):
        """get method for MenuItem name"""
        return self._name

    def get_selling_price(self):
        """get method for MenuItem's selling price"""
        return self._selling_price
    
    def get_servings(self):
        return self._servings
    
    def get_recipe(self):
        return self._recipe
    
    def get_quantity(self):
        return self._quantity
    
    def add_quantity(self, num):
        self._quantity += num
    
    def remove_quantity(self, num):
        if self._quantity - num >= 0:
            self._quantity -= num
    

class Lemonade(MenuItem):
    def __init__(self, name, selling_price):
        super().__init__(name, selling_price)
        self._recipe = {
            "lemons" : 7,
            "sugar" : 2,
            "cups" : 7
        }
        self._servings = 7
    
    def get_wholesale_cost(self, ingredients):
        total_cost = 0
        for ingredient, quantity in self._recipe.items():
            unit_price = ingredients[ingredient].get_unit_price()
            ingredient_cost = round(unit_price * quantity, 2)
            total_cost += ingredient_cost
        return round(total_cost/ self._servings, 2)


class StrawberryLemonade(Lemonade):
    def __init__(self, name, selling_price):
        super().__init__(name, selling_price)
        self._recipe = {
            "lemons": 6,
            "sugar": 2,
            "strawberries": 1.5,
            "cups": 7
        }
        

class ChocolateChipCookie(MenuItem):
    def __init__(self, name, selling_price):
        super().__init__(name, selling_price)
        self._recipe = {
            "butter" : 1,
            "sugar" : 2,
            "vanilla" : 2,
            "eggs" : 2,
            "flour" : 3,
            "chocolate chips" : 2
        }
        self._servings = 30
    
    def get_wholesale_cost(self, ingredients):
        total_cost = 0
        for ingredient, quantity in self._recipe.items():
            unit_price = ingredients[ingredient].get_unit_price()
            ingredient_cost = round(unit_price * quantity, 2)
            total_cost += ingredient_cost
        return round(total_cost/ self._servings, 2)
        

class Bank:
    def __init__(self, starting_balance):
        self._balance = starting_balance
        self._sales = 0
    
    def record_sales(self, amount):
        self._sales += amount
        self._balance += amount
    
    def record_expense(self, amount):
        self._balance -= amount
    
    def get_balance(self):
        return self._balance

    def get_sales(self):
        return self._sales

class WeatherReport:
    def __init__(self):
        self._weather = ["sunny", "sunny", "sunny", "cloudy", "cloudy", "rainy", "hot"]
    
    def get_weather(self):
        num = random.randint(0,6)
        return self._weather[num]

class Customers:
    def __init__(self, day):
        self._day = day
        self._number_customers = 0
        self._unhappy_customers = 0
    
    def get_number_customers(self):
        return self._number_customers
    
    def set_customers(self, weather):
        if weather == "sunny":
            num = random.randint(10, 50) 
        elif weather == "cloudy":
            num = random.randint(5, 40) 
        elif weather == "rainy":
            num = random.randint(0, 20)
        else:
            num = random.randint(20, 60)
        self._number_customers += num
    
    def set_unhappy_customers(self, num):
        self._unhappy_customers += num
    
    def get_unhappy_customers(self):
        return self._unhappy_customers


class SalesForDay:
    """Class that represents the sales for a particular day"""
    def __init__(self, day, sales_dict):
        self._day = day
        self._sales_dict = sales_dict

    def get_day(self):
        """get method for SalesForDay day"""
        return self._day

    def get_sales_dict(self):
        """get method for SalesForDay dictionary, including  food item name and number sold"""
        return self._sales_dict

class LemonadeStand:
    """represents the Lemonade Stand, contains 4 data members: string for name of stand, integer representing
    current day, dictionary of MenuItem objects, and list of SalesForDay objects
    """
    def __init__(self, stand_name, supplies, bank):
        """initializes Lemonade Stand name, sets current day to 0, creates empty dictionary for menu,
        and empty list for sales
        """
        self._stand_name = stand_name
        self._current_day = 0
        self._menu = {}
        self._sales = []
        self._supplies = supplies
        self._bank = bank

    def get_name(self):
        """get method for lemonade stand name"""
        return self._stand_name
    
    def get_day(self):
        return self._current_day

    def add_menu_item(self, menu_item_obj):
        """takes a MenuItem object and adds it to the menu dictionary"""
        menu_item_name = menu_item_obj.get_name()
        self._menu[menu_item_name] = menu_item_obj
    
    def get_menu(self):
        return self._menu
    
    def make_item(self, menu_item_name):
        if menu_item_name in self._menu:
            menu_item = self._menu[menu_item_name]
            if self._supplies.make_menu_item(menu_item):
                serving = menu_item.get_servings()
                menu_item.add_quantity(serving)
                return True


    def enter_sales_for_today(self, items_dict):
        """takes a dictionary where the keys are the names of items sold and corresponding values are how many
        items are sold. Creates new SalesForDay object using current day and given dictionary, 
        adds it to sales list, increments day"""
        if all(key in self._menu for key in items_dict):
            new_sales_obj = SalesForDay(self._current_day, items_dict)
            self._sales.append(new_sales_obj)
            self._current_day += 1
        

    def get_sales_dict_for_day(self, day_number):
        """takes an integer representing a particular day, returns the dictionary of sales for that day"""
        for day in self._sales:
            if day.get_day() == day_number:
                return day.get_sales_dict()
    

    def get_daily_income(self, daily_sales):
        """returns the daily income"""
        total_income = 0
        for item in self._menu.keys():
            if item in daily_sales:
                sales = daily_sales[item]
                price = self._menu[item].get_selling_price()
                total_income += (sales * price)
        return round(total_income, 2)
    
    def get_daily_profit(self, daily_sales, ingredients):
        """returns the profit for the day selling_price - wholesale_cost"""
        total_profit = 0
        for item in self._menu.keys():
            if item in daily_sales:
                sales = daily_sales[item]
                price = self._menu[item].get_selling_price()
                wholesale_cost = self._menu[item].get_wholesale_cost(ingredients)
                total_profit += (sales * (price - wholesale_cost))
        return round(total_profit, 2)

    def total_sales_for_menu_item(self, menu_item):
        """takes the name of a menu item and returns the total number of that item sold over history of stand"""
        total_sales = 0
        for day in self._sales:
            daily_sales = day.get_sales_dict()
            if menu_item in daily_sales:
                total_sales += daily_sales[menu_item]
        return total_sales

    def total_profit_for_menu_item(self, menu_item, ingredients):
        """takes the name of a menu item and returns the total profit on that item over history of stand"""
        total_sales = self.total_sales_for_menu_item(menu_item)
        selling_price = self._menu[menu_item].get_selling_price()
        wholesale_cost = self._menu[menu_item].get_wholesale_cost(ingredients)
        return round((selling_price - wholesale_cost)*total_sales , 2)

    def total_profit_for_stand(self):
        """takes no parameters and returns total profit on all items sold over history of the stand"""
        total_profit = 0
        for key in self._menu:
            total_profit += self.total_profit_for_menu_item(key)
        return round(total_profit, 2)

