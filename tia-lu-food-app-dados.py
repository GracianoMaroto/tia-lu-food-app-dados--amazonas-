class Item:
    def __init__(self, code, name, description, price, stock):
        self.code = code
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        try:
            quantity = int(quantity)
        except ValueError:
            raise ValueError("Quantity must be a number.")
        if quantity < 0 and abs(quantity) > self.stock:
            raise ValueError("Insufficient stock to remove the requested quantity.")
        else: 
            self.stock += quantity

    def update_name(self):
        confirm = input(f"You are about to change the name of the product {self.name}\n(Confirm? 1. Yes / 2. No ) ")
        if confirm == "1":
            new_name = input("Type the new name: ").strip()
            self.name = new_name
            print(f"The name of the item code:{self.code} has changed to {self.name}")
        else:
            print("Operation canceled")
            return
    
    def update_description(self):
        print(f"Current description:\n{self.description}")
        new_description = input("Type a new description: ")
        confirm = input(f"You are about to change the description of the product {self.name}\n(Confirm? 1. Yes / 2. No ) ")
        if confirm == "1":
            self.description = new_description
            print(f"Description of the item {self.name} has changed")
        else:
            print("Operation canceled")
            return

    def update_price(self):
        print(f"Current price:\n{self.price}")  
        new_price = input("Type a new price: ")
        confirm = input(f"You are about to change the price of the product {self.name} to R${new_price}\n(Confirm? 1. Yes / 2. No ) ")
        if confirm == "1":
            self.price = new_price
            print(f"Price of the item {self.name} has changed to R${self.price}")
        else:
            print("Operation canceled")
            return

    def __repr__(self):
        return f"\nItem code: {self.code}\nname: {self.name}\ndescription: {self.description}\nprice: R${self.price}\nstock: {self.stock}\n"
    
class Order:
    def __init__(self, code, costumer, items_order=[], status="Pending", payment="Paid"):
        self.code = code 
        self.costumer = costumer
        self.items_order = items_order
        self.status = status
        self.payment = payment
        self.order_total_price = None

    def total_price(self):
        return sum(item.price for item in self.items_order)

    def apply_discount(self):
        if not self.items_order:
            raise ValueError("It's not possible to apply discount in a empty order.")
        discount_value = self.total_price() * (10 / 100)
        self.order_total_price = self.total_price() - discount_value
        return self.order_total_price

    def finalize(self):
        if self.order_total_price is None:
            self.order_total_price = self.total_price()
        return self.order_total_price
        
    def __repr__(self):
        total = self.order_total_price if self.order_total_price is not None else self.total_price()
        items_list = ", ".join(item.name for item in self.items_order) if self.items_order else "No items"
        return (
            f"\n📦 Order: {self.code}\n"
            f"👤 Costumer: {self.costumer}\n"
            f"🛒 Items: {items_list}\n"
            f"💰 Total: R${total:.2f}\n"
            f"📌 Status: {self.status}\n"
        )
   
catalog = []
costumers = []
def consults(all_orders, costumers):

    choice = ""
    width = 60
    while choice != "5":
        print("\n📋 Consult's menu:")
        print("-" * 40)
        print("[1] View All Orders".center(width))
        print("[2] Filter by status".center(width))
        print("[3] Sales Report".center(width))
        print("[4] See all costumers".center(width))
        print("[5] Back to Main Menu".center(width))
        choice = input("Choose an option (1 / 2 / 3 / 4 / 5): ".center(width))

        match choice:
            case "1":
                if not all_orders:
                    print("⚠️ There's no orders to show.")
                    continue

                print("\n📋 List of orders:")
                print("-" * 40)
                for o in all_orders:
                    print(f"Code: {o.code}")
                    print(f"Costumer: {o.costumer}")
                    print(f"Items: {', '.join([item.name for item in o.items_order])}")
                    print(f"Status: {o.status}")
                    print(f"Total: R${o.order_total_price:.2f}")
                    print("-" * 40)
            case "2":
                print("\n📋 Consult's order by status:")
                print("-" * 40)
                print("[1] Making".center(width))
                print("[2] Ready".center(width))
                print("[3] Waiting Delivery".center(width))
                print("[4] Delivering".center(width))
                print("[5] Delivered".center(width))
                print("[6] Canceled".center(width))
                print("[7] Rejected".center(width))
                print("[8] Back to Main Menu".center(width))
                status = input("Choose an option (1 / 2 / 3 / 4 / 5 / 6 / 7 / 8): ".center(width))

                match status:
                    case "1":
                        print("\n📋 List of orders:")
                        print("-" * 40)
                        list = get_orders_by_status("Making")
                        if len(list) > 0:
                            for order in list:
                                print(f"📦 Code: {order.code}")
                                print(f"👤 Costumer: {order.costumer}")
                                print(f"🛒 Items: {', '.join([item.name for item in order.items_order])}")
                                print(f"💰 Price: R${order.order_total_price:.2f}")
                                print("-" * 40)
                            print(f"\n📋 Number of registers: {len(list)}")
                        else:
                            print("\nThere's no orders with  current status")
                    case "2":
                        print("\n📋 List of orders:")
                        print("-" * 40)
                        list = get_orders_by_status("Ready")
                        if len(list) > 0:
                            for order in list:
                                print(f"📦 Code: {order.code}")
                                print(f"👤 Costumer: {order.costumer}")
                                print(f"🛒 Items: {', '.join([item.name for item in order.items_order])}")
                                print(f"💰 Price: R${order.order_total_price:.2f}")
                                print("-" * 40)
                            print(f"\n📋 Number of registers: {len(list)}")
                        else:
                            print("\nThere's no orders with  current status".center(width))
                    case "3":
                        print("\n📋 List of orders:")
                        print("-" * 40)
                        list = get_orders_by_status("Waiting Delivery")
                        if len(list) > 0:
                            for order in list:
                                print(f"📦 Code: {order.code}")
                                print(f"👤 Costumer: {order.costumer}")
                                print(f"🛒 Items: {', '.join([item.name for item in order.items_order])}")
                                print(f"💰 Price: R${order.order_total_price:.2f}")
                                print("-" * 40)
                            print(f"\n📋 Number of registers: {len(list)}")
                        else:
                            print("\nThere's no orders with  current status".center(width))
                    case "4":
                        print("\n📋 List of orders:")
                        print("-" * 40)
                        list = get_orders_by_status("Delivering")
                        if len(list) > 0:
                            for order in list:
                                print(f"📦 Code: {order.code}")
                                print(f"👤 Costumer: {order.costumer}")
                                print(f"🛒 Items: {', '.join([item.name for item in order.items_order])}")
                                print(f"💰 Price: R${order.order_total_price:.2f}")
                                print("-" * 40)
                            print(f"\n📋 Number of registers: {len(list)}")
                        else:
                            print("\nThere's no orders with  current status".center(width))
                    case "5":
                        print("\n📋 List of orders:")
                        print("-" * 40)
                        list = get_orders_by_status("Delivered")
                        if len(list) > 0:
                            for order in list:
                                print(f"📦 Code: {order.code}")
                                print(f"👤 Costumer: {order.costumer}")
                                print(f"🛒 Items: {', '.join([item.name for item in order.items_order])}")
                                print(f"💰 Price: R${order.order_total_price:.2f}")
                                print("-" * 40)
                            print(f"\n📋 Number of registers: {len(list)}")
                        else:
                            print("\nThere's no orders with  current status".center(width))
                    case "6":
                        print("\n📋 List of orders:")
                        print("-" * 40)
                        list = get_orders_by_status("Canceled")
                        if len(list) > 0:
                            for order in list:
                                print(f"📦 Code: {order.code}")
                                print(f"👤 Costumer: {order.costumer}")
                                print(f"🛒 Items: {', '.join([item.name for item in order.items_order])}")
                                print(f"💰 Price: R${order.order_total_price:.2f}")
                                print("-" * 40)
                            print(f"\n📋 Number of registers: {len(list)}")
                        else:
                            print("\nThere's no orders with  current status".center(width))
                    case "7":
                        print("\n📋 List of orders:")
                        print("-" * 40)
                        list = get_orders_by_status("Rejected")
                        if len(list) > 0:
                            for order in list:
                                print(f"📦 Code: {order.code}")
                                print(f"👤 Costumer: {order.costumer}")
                                print(f"🛒 Items: {', '.join([item.name for item in order.items_order])}")
                                print(f"💰 Price: R${order.order_total_price:.2f}")
                                print("-" * 40)
                            print(f"\n📋 Number of registers: {len(list)}")
                        else:
                            print("\nThere's no orders with  current status".center(width))
                    case "8":
                        print("🔙Returning to Main Menu.".center(width))
                        return
                    case _:
                        print("Invalid option. Please try again.".center(width))
            case "3":
                print("\n📋 Sales reports:".center(width))
                print("-" * 40)
                print("[1] All registers".center(width))
                print("[2] Closed sales".center(width))
                print("[3] Back to Main Menu".center(width))
                report = input("Choose an option (1 / 2 / 3): ".center(width))

                match report:
                    case "1":
                        total_price = 0
                        acc_price = 0
                        for o in all_orders:
                            acc_price = o.order_total_price 
                            total_price = total_price + acc_price   
                        print(f"\n📋 Number of registers: {len(all_orders)}")                    
                        print(f"💰 Total value registered: R${total_price}")
                    case "2":
                        total_price = 0
                        acc_price = 0
                        delivered_orders = get_orders_by_status("Delivered")
                        for o in delivered_orders:
                            acc_price = o.order_total_price 
                            total_price = total_price + acc_price
                        print(f"\n📋 Number of registers: {len(delivered_orders)}")                    
                        print(f"💰 Total value registered: R${total_price}")                        
                    case "3":
                        print("🔙Returning to previous Menu.".center(width))
                        return
                    case _:
                        print("Invalid option. Please try again.".center(width))
            case "4":
                for c in costumers:
                    print("Active costumers:")
                    print(c)
            case "5":
                print("🔙Returning to Main Menu.".center(width))
                return
            case _:
                print("Invalid option. Please try again.".center(width))

def manage_menu_items(catalog):
    choice = ""
    width = 60

    while choice != "4":
        print("=" * width)
        print("🍽️  Item Management Menu".center(width))
        print("=" * width)

        print("[1] Add Item".center(width))
        print("[2] Update Item".center(width))
        print("[3] View All Items".center(width))
        print("[4] Back to Main Menu\n".center(width))
        choice = input("Choose an option (1 / 2 / 3 / 4):".center(width))

        match choice:
            case "1":
                code = len(catalog) + 1
                width = 60
                print("=" * width)
                print("➕ Add New Item".center(width))
                print("=" * width)                
                name = input("Type a new item name:\n")
                description = input("Type a description:\n")
                valid_price = False
                while not valid_price:
                    try:
                        price = input("Type the new item`s price: \nEx: 8.00 / 12.50\n")
                        price = float(price)
                        valid_price = True
                    except ValueError:
                        print("Price must be a positive number")
                stock = int(input("How many items will be add:\n"))
                new_item = Item(code, name, description, price, stock)
                catalog.append(new_item)
                print('Item added with sucess')

            case "2":
                width = 60
                item = input("Type the name of the item:\n".center(width))                
                for i in catalog:
                    if i.name == item:
                        update_type = ""
                        while update_type != "5":
                            print("=" * width)
                            print("🛠️ Update Item".center(width))
                            print("=" * width)
                            print("[1] Update item’s name".center(width))
                            print("[2] Update item’s description".center(width))
                            print("[3] Update item’s price".center(width))
                            print("[4] Update item’s quantity".center(width))
                            print("[5] Back to Previous Menu\n".center(width))

                            update_type = input("Choose an option (1 / 2 / 3 / 4 / 5):".center(width))
                        
                            match update_type:
                                case "1":
                                    i.update_name()
                                case "2":
                                    i.update_description()
                                case "3":
                                    i.update_price()
                                case "4":
                                    print(f"The item {i.name} has {i.stock} units in stock.".center(width))
                                    quantity = input("Type the new quantity you want to add or take from stock:\nUse a minus sign (-) to decrease stock\n".center(width))
                                    try:
                                        quantity = quantity.strip()
                                        i.update_stock(quantity)
                                        print(f"Stock updated. New stock for {i.name}: {i.stock}".center(width))
                                    except ValueError as e:
                                        print(e)
                                case "5":
                                    return
                                case _:
                                    print("❌ Invalid option. Please try again.".center(width))
                else:
                    print("⚠️ Item not found. Please try again.".center(width))

            case "3":
                width = 60
                if not catalog:
                    print("⚠️ No items on the menu.".center(width))
                    continue

                print("=" * width)
                print("📋 Menu List of Items".center(width))
                print("=" * width)

                for item in catalog:
                    print(f"📦 Code: {item.code}".center(width))
                    print(f"📝 Name: {item.name}".center(width))
                    print(f"🖊️ Description: {item.description}".center(width))
                    print(f"💰 Price: R${item.price}".center(width))
                    print(f"📦 Stock: {item.stock}".center(width))
                    print("-" * width)
                    
            case "4":
                width = 60
                print("↩️ Returning to Main Menu.".center(width))
                return

            case _:
                width = 60
                print("❌ Invalid option. Please try again.".center(width))

# manage orders atualizado  #############################################################################
all_orders = []

def get_orders_by_status(status):
    return [o for o in all_orders if o.status == status]

def manage_orders(all_orders, catalog):
    choice = ""
    width = 60

    while choice != "5":
        print("=" * width)
        print("📦 Orders Management Menu".center(width))
        print("=" * width)

        print("[1] Create a new Order".center(width))
        print("[2] Manage Pending Orders".center(width))
        print("[3] Update Orders Status".center(width))
        print("[4] Cancel Order".center(width))
        print("[5] Return to Main Menu\n".center(width))

        choice = input("Choose an option (1 / 2 / 3 / 4 / 5):".center(width))
        
        match choice:
# case 1 atualizado #############################################################################
            case "1":
                name_costumer = input("What is the name of the costumer? ")
                number_costumer = input("What is the cellphone number of the costumer? ")
                code_costumer = len(costumers) +1
                costumer = [code_costumer, name_costumer, number_costumer]

                code = len(all_orders) + 1
                items_order = []
                status = "" 
                payment = 'Paid'
                order = Order(code, costumer, items_order, status, payment)
                choice = ""
                while choice != "3":
                    print('1. Insert a new item')
                    print('2. Finish order')
                    print('3. Cancell order creation')
                    choice = input('\nChoose an option (1 / 2 / 3): ')

                    match choice:
                        case "1":
                            if catalog == []:
                                print('The menu is empty, please add some items to proceed.')
                                return
                            
                            print("\n📋 Menu list of items:")
                            print("-" * 40)
                            for item in catalog:
                                print(f"📦 Code: {item.code}")
                                print(f"📝 Name: {item.name}")
                                print(f"🖊️ Description: {item.description}")
                                print(f"💰 Price: R${item.price:.2f}")
                                print(f"📦 Stock: {item.stock}")
                                print("-" * 40)
                            catalog_code = int(input('Choose a item by code: '))
                            found = False

                            for item in catalog:
                                if item.code ==catalog_code:
                                    found = True
                                    if item.stock > 0:
                                        print(f"\nItem {catalog_code} added with success")
                                        items_order.append(item)
                                        print(f"\n{costumer}'s order items are: {[i.name for i in items_order]}")
                                        item.update_stock(-1)
                                        print(f"The current stock for this item is: {item.stock}")
                                    else:
                                        print("Stock insuficiente")
                                        print(f"The current stock for this item is: {item.stock}\n")
                                        break
                                if not found:
                                    print("Item not found")
                            
                        case "2":
                            if len(items_order) == 0:
                                print("Order must have at least one item!")
                                continue

                            print(f"The current value of the order is: R${order.total_price():.2f}")

                            discount_choice = input("Would you like to apply a discount coupon of 10%? (1. Yes / 2. No): ")

                            match discount_choice:
                                case "1":
                                    order.apply_discount() 
                                    print(f"\nCoupon applied successfully. New total: R${order.order_total_price:.2f}")
                                case "2":
                                    order.finalize()  
                                    print(f"\nNo discount applied. Total: R${order.order_total_price:.2f}")
                                case _:
                                    print("Invalid option. Proceeding without discount.")
                                    order.finalize()

                            order.status = "Pending"
                            all_orders.append(order)
                            costumers.append(costumer)

                            print("\n✅ Order added with sucess!")
                            print("-" * 40)
                            print(f"Code: {order.code}")
                            print(f"Costumer: {order.costumer}")
                            print(f"Items: {', '.join([item.name for item in order.items_order])}")
                            print(f"Status: {order.status}")
                            print(f"Total: R${order.order_total_price:.2f}")
                            print("-" * 40)
                            print("\nReturning to manage orders.\n")
                            break 
                        
                        case "3":
                            print("Cancelling order creation.")
                            break
                            
                        case _:
                            print("Invalid option. Please try again.")
                            continue

            case "2":
                pending_orders = get_orders_by_status("Pending")
                if not pending_orders:
                    print("⚠️ No pending orders.".center(width))
                    continue

                order = pending_orders[0]
                print("=" * width)
                print("📦 Pending Order".center(width))
                print("=" * width)
                print(str(order).center(width))

                print("[1] Accept order".center(width))
                print("[2] Reject order".center(width))
                print("[3] Return to Manage Orders\n".center(width))
                choice = input("Choose an option (1 / 2 / 3):".center(width))

                if choice == "1":
                    order.status = "Accepted"
                    print("✅ Order accepted with success!".center(width))
                elif choice == "2":
                    order.status = "Rejected"
                    for item in order: 
                        item.update_stock(+1)
                    print("❌ Order rejected.".center(width))
                elif choice == "3":
                    print("🔙 Returning to Manage Orders...".center(width))
                else:
                    print("⚠️ Invalid option.".center(width))
                            
            case "3":
                if not all_orders:
                    print("⚠️ No available orders to update.".center(width))
                    continue

                print("=" * width)
                print("📋 Orders Available".center(width))
                print("=" * width)

                for idx, order in enumerate(all_orders, start=1):
                    print(f"{idx}. Code: {order.code} | Costumer: {order.costumer} | Status: {order.status}".center(width))

                try:
                    order_index = int(input("Select an order by code:".center(width))) - 1
                    order = all_orders[order_index]
                except (ValueError, IndexError):
                    print("❌ Invalid selection.".center(width))
                    continue

                print("📦 Selected Order".center(width))
                print(str(order).center(width))

                print("🔄 Choose new status:".center(width))
                print("[1] Making".center(width))
                print("[2] Ready".center(width))
                print("[3] Waiting Delivery".center(width))
                print("[4] Delivering".center(width))
                print("[5] Delivered".center(width))

                status_choice = input("Choose an option (1-5):".center(width))

                match status_choice:
                    case "1": order.status = "Making"
                    case "2": order.status = "Ready"
                    case "3": order.status = "Waiting Delivery"
                    case "4": order.status = "Delivering"
                    case "5": order.status = "Delivered"
                    case _: 
                        print("❌ Invalid option.".center(width))
                        continue

                print("✅ Order updated with success!".center(width))

            case "4":
                if not all_orders:
                    print("⚠️ No orders available.".center(width))
                    continue

                cancellable_orders = [o for o in all_orders if o.status in ("Pending", "Accepted")]
                if not cancellable_orders:
                    print("⚠️ No cancellable orders available.".center(width))
                    continue

                print("=" * width)
                print("📋 Orders Available for Cancelling".center(width))
                print("=" * width)

                for idx, order in enumerate(cancellable_orders, start=1):
                    print(f"{idx}. Code: {order.code} | Costumer: {order.costumer} | Status: {order.status}".center(width))

                try:
                    order_index = int(input("Select an order by code:".center(width))) - 1
                    order = cancellable_orders[order_index]
                except (ValueError, IndexError):
                    print("❌ Invalid selection.".center(width))
                    continue

                print("📦 Selected Order".center(width))
                print(str(order).center(width))

                print("❗ Choose action:".center(width))
                print("[1] Cancel order".center(width))
                print("[2] Exit\n".center(width))

                cancel_choice = input("Choose an option (1 / 2):".center(width))
                match cancel_choice:
                    case "1":
                        order.status = "Canceled"
                        for item in order.items_order:
                            item.update_stock(+1)
                        print(f"✅ Order {order.code} canceled with success!".center(width))
                    case "2":
                        print("🔙 Returning to Orders Menu...".center(width))
                    case _:
                        print("❌ Invalid option.".center(width))

            case "5":
                print("🔙 Returning to Main Menu...".center(width))
                return
            case _:
                print("❌ Invalid option. Please try again.".center(width))

def main_menu():
    choice = ""
    width = 60

    while choice != "4":
        print("=" * width)
        print("🍔 Food Delivery Ordering System 🍕".center(width))
        print("=" * width)

        print("[1] Manage Menu Items".center(width))
        print("[2] Manage Orders".center(width))
        print("[3] Consults".center(width))
        print("[4] Exit".center(width))

        choice = input("Choose an option (1 / 2 / 3 / 4):".center(width))

        match choice:
            case "1":
                manage_menu_items(catalog)
            case "2":
                manage_orders(all_orders, catalog)
            case "3":
                consults(all_orders, costumers)
            case "4":
                print("\nExiting the system. Goodbye!\n".center(width))
                return
            case _:
                print("Invalid option. Please try again.".center(width))

main_menu()