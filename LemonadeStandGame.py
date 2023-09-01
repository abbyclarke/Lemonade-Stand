from LemonadeStand import *


# setup
menu_items = {
    1 : "lemonade",
    2 : "chocolate chip cookie",
    3 : "strawberry lemonade"
}
menu = set()
StoreItem_lemon = StoreItem("lemons", 4.00, 9, 5, ["bag of lemons", "bags of lemons"], ["lemon", "lemons"])
StoreItem_sugar = StoreItem("sugar", 4.00, 14, 5, ["bag of sugar", "bags of sugar"], ["cup", "cups"])
StoreItem_strawberry = StoreItem("strawberries", 6.00, 4, 5, ["container of strawberries", "containers of strawberries"], ["cup", "cups"])
StoreItem_butter = StoreItem("butter", 5.00, 2, 5, ["stick of butter", "sticks of butter"], ["cup", "cups"])
StoreItem_vanilla = StoreItem("vanilla", 5.00, 12, 3, ["bottle of vanilla", "bottles of vanilla"], ["tsp", "tsp"])
StoreItem_egg = StoreItem("eggs", 2.00, 12, 5, ["carton of eggs", "cartons of eggs"], ["egg", "eggs"])
StoreItem_flour = StoreItem("flour", 5.00, 18, 3, ["bag of flour", "bags of flour"], ["cup", "cups"])
StoreItem_chocolatechips = StoreItem("chocolate chips", 3.00, 2, 3, ["bag of chocolate chips", "bags of chocolate chips"], ["cup", "cups"])
StoreItem_cup = StoreItem("cups", 10.00, 100, 5, ["pack of cups", "packs of cups"], ["cup", "cups"])
ingredients = {
    "lemons" : StoreItem_lemon,
    "sugar" : StoreItem_sugar,
    "strawberries" : StoreItem_strawberry,
    "butter" : StoreItem_butter,
    "vanilla" : StoreItem_vanilla,
    "eggs" : StoreItem_egg,
    "flour" : StoreItem_flour,
    "chocolate chips" : StoreItem_chocolatechips,
    "cups" : StoreItem_cup
}
bank = Bank(40.00)
store = Store()
store.add_item(StoreItem_lemon)
store.add_item(StoreItem_sugar)
store.add_item(StoreItem_strawberry)
store.add_item(StoreItem_butter)
store.add_item(StoreItem_vanilla)
store.add_item(StoreItem_egg)
store.add_item(StoreItem_flour)
store.add_item(StoreItem_chocolatechips)
store.add_item(StoreItem_cup)
supplies = Supplies(store, bank)


# first day setup
lemonade_stand_name = input("Welcome to the Lemonade Stand Game. Let's get started. What would you like to name your Lemonade Stand? ")
stand = LemonadeStand(lemonade_stand_name, supplies, bank)
print(f"What items would you like to sell at {lemonade_stand_name}?")
for num, item in menu_items.items():
    print(f"{num}: {item}")
menu_choices = input("Enter the numbers here: ")
for num in menu_choices:
    if num.isdigit():
        menu.add(int(num))

# pick prices and add to menu
for item in menu:
    price = float(input(f"What price would you like to make your {menu_items[item]}? "))
    if menu_items[item] == "lemonade":
        lemonade = Lemonade("lemonade", price)
        stand.add_menu_item(lemonade)
    elif menu_items[item] == "chocolate chip cookie":
        chocolate_chip_cookie = ChocolateChipCookie("chocolate chip cookie", price)
        stand.add_menu_item(chocolate_chip_cookie)
    elif menu_items[item] == "strawberry lemonade":
        strawberry_lemonade = StrawberryLemonade("strawberry lemonade", price)
        stand.add_menu_item(strawberry_lemonade)

# day starts
selection = -1
while selection != 7:
    print("""
1: See recipes
2: See store
3: See bank balance
4: Buy supplies from store
5: Check current supplies
6: Start day
7: Quit
    """)

    selection = input("\nWhat would you like to do today? ")
    # see recipes
    if selection == '1':
        menu = stand.get_menu()
        for name, item in menu.items():
            recipe = item.get_recipe()
            print(f"{name}: {recipe}")

    # see store        
    elif selection == '2':
        prices_with_quantities = store.get_prices_with_quantities()
        for item_name, (price, quantity) in prices_with_quantities.items():
            print(f"{item_name}: Price: ${price} Quantity: {quantity}")

    # see bank balance        
    elif selection == '3':
        balance = bank.get_balance()
        print(f"Balance: ${balance}")

    # buy supplies
    elif selection == '4':
        prices_with_quantities = store.get_prices_with_quantities()
        items = list(prices_with_quantities.items())
        store_choice = '0'
        while store_choice != '2':
            for index, (item_name, (price, quantity)) in enumerate(items):
                print(f"{index+1}: {item_name}: Price: ${price} Quantity: {quantity}")
        
            index = int(input("\nWhich item number would you like to buy? "))
            quantity = int(input("How many of that item? "))
            supplies.buy_item(items[index-1][0], quantity)
            store_choice = input("If you want to keep shopping type 1, to exit type 2: ")

    # check current supplies
    elif selection == '5':
        current_supplies = supplies.get_current_items()
        print(f"Current supplies: {current_supplies}")

    # start day
    elif selection == '6':
        weather = WeatherReport()
        weather_today = weather.get_weather()
        customers = Customers(0)
        customers.set_customers(weather_today)
        num_customers = customers.get_number_customers()
        menu = stand.get_menu()
        sales = {item_name: 0 for item_name in menu.keys()}
        sales_keys = list(sales.keys())
        
        # check what each customer is ordering
        for customer in range(num_customers):
            order = random.randint(0, len(menu)-1)
            menu_items = list(menu.keys())
            item_name = menu_items[order]
            menu_item = menu[item_name]

            # see if we already have the item prepared
            if menu_item.get_quantity() > 0:
                menu_item.remove_quantity(1)
                price = menu_item.get_selling_price()
                bank.record_sales(price)
                sales_item_name = sales_keys[order]
                sales[item_name] += 1
            else:
                # see if we can make the item with ingredients
                if stand.make_item(item_name):
                    menu_item.remove_quantity(1)
                    price = menu_item.get_selling_price()
                    bank.record_sales(price)
                    sales_item_name = sales_keys[order]
                    sales[item_name] += 1
                # customer didn't get their order and is unhappy
                else:
                    customers.set_unhappy_customers(1)

        day = stand.get_day()
        stand.enter_sales_for_today(sales)

        print(f"""
              Today is day {day}. It is {weather_today}.
              You had {customers.get_number_customers()} customers! 
              {customers.get_unhappy_customers()} were unhappy because they didn't get their order.
              Total income today: {stand.get_daily_income(sales)} Total profit today: {stand.get_daily_profit(sales, ingredients)}
              Current balance: {bank.get_balance()}
              Current supplies: {supplies.get_current_items()}
              """)

        # refill store
        if day % 2 == 0:
            store_items = store.get_all_items()
            for item_name, item_object in store_items.items():
                num = random.randint(1, 5)
                item_object.restock(num)

       
    elif selection == '7':
        print("Thanks for playing!")
        break
    else:
        print("Please select from choices 1-7")





