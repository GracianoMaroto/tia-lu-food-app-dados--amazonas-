import json
#-----------------------------------------------AVL classes-------------------------------------------------#
class Node:
    def __init__(self, key, value):
        self.key = key       # Ex: item['code']. Usado para comparação.
        self.value = value   # O dicionário completo do Item/Pedido.
        self.height = 1      # Altura do nó.
        self.left = None     # Filho esquerdo.
        self.right = None    # Filho direito.

class AVLTree:
    def __init__(self):
        self.root = None # A raiz da árvore

    def __len__(self):
        return len(self.inorder_traversal_list(self.root))
    
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_height(self, node):
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    # --- Rotations ---
    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        self._update_height(z)
        self._update_height(y)
        return y

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self._update_height(z)
        self._update_height(y)
        return y

    # --- Insert ---
    def insert(self, root, key, value):
        if not root:
            return Node(key, value)
        
        if key < root.key:
            root.left = self.insert(root.left, key, value)
        elif key > root.key:
            root.right = self.insert(root.right, key, value)
        else:
            # Chaves duplicadas (Códigos de item) não permitidas
            return root 

        self._update_height(root)
        balance = self._get_balance(root)

        # 4 Casos de Rotação
        if balance > 1: # Desbalanceamento à esquerda
            if key < root.left.key: # Esquerda-Esquerda
                return self._rotate_right(root)
            else: # Esquerda-Direita
                root.left = self._rotate_left(root.left)
                return self._rotate_right(root)
        
        if balance < -1: # Desbalanceamento à direita
            if key > root.right.key: # Direita-Direita
                return self._rotate_left(root)
            else: # Direita-Esquerda
                root.right = self._rotate_right(root.right)
                return self._rotate_left(root)

        return root
    
    # --- Search (O(log n)) ---
    def search(self, root, key):
        if root is None or root.key == key:
            # Retorna o dicionário (o valor) ou None
            return root.value if root else None
        
        if key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    # --- Save and show ---
    def inorder_traversal_list(self, root):
        """Retorna uma lista de dicionários ordenada pela chave (code)"""
        result = []
        if root:
            result.extend(self.inorder_traversal_list(root.left))
            result.append(root.value)
            result.extend(self.inorder_traversal_list(root.right))
        return result

#-----------------------------------------------item's functions-------------------------------------------------#

def create_item(code, name, description, price, stock):
    return {
        "code":code, 
        "name":name, 
        "description": description,
        "price": price, 
        "stock": stock
        }

def update_stock(item, quantity):
    try:
        quantity = int(quantity)
    except ValueError:
        raise ValueError("Quantity must be a number.")
    if quantity < 0 and abs(quantity) > item['stock']:
        raise ValueError("Insufficient stock to remove the requested quantity.")
    else: 
        item['stock'] += quantity

def update_name(item):
    confirm = input(f"You are about to change the name of the product {item['name']}\n(Confirm? 1. Yes / 2. No ) ")
    if confirm == "1":
        new_name = input("Type the new name: ").strip()
        item['name'] = new_name
        print(f"The name of the item code:{item['code']} has changed to {item['name']}")
    else:
        print("Operation canceled")
        return

def update_description(item):
    print(f"Current description:\n{item['description']}")
    new_description = input("Type a new description: ")
    confirm = input(f"You are about to change the description of the product {item['name']}\n(Confirm? 1. Yes / 2. No ) ")
    if confirm == "1":
        item['description'] = new_description
        print(f"Description of the item {item['name']} has changed")
    else:
        print("Operation canceled")
        return

def update_price(item):
    print(f"Current price:\n{item['price']}")  
    new_price_input = input("Type a new price: ")
    new_price = float(new_price_input)
    confirm = input(f"You are about to change the price of the product {item['name']} to R${new_price}\n(Confirm? 1. Yes / 2. No ) ")
    if confirm == "1":
        item['price'] = new_price
        print(f"Price of the item {item['name']} has changed to R${item['price']}")
    else:
        print("Operation canceled")
        return

#-----------------------------------------------order's functions-------------------------------------------------#
def create_order(code,costumer_data, items_order, status='Pending', payment='Paid'):
    total = sum(item["price"] * item["quantity"] for item in items_order)
    
    return {
        "code": code, 
        "costumer": costumer_data,
        "items_order": items_order, 
        "status": status,
        "payment": payment,
        "order_total_price": total 
    }

def apply_order_discount(order):
    current_total = order['order_total_price']
    if current_total is None or len(order['items_order']) == 0:
        raise ValueError("It's not possible to apply discount in a empty order.")
    discount_value = current_total * (10 / 100)
    order['order_total_price'] = current_total - discount_value
    return order['order_total_price']

#-----------------------------------------------Aux functions-------------------------------------------------#
def get_orders_by_status(status):
    lista_pedidos = orders_tree.inorder_traversal_list(orders_tree.root)
    return [o for o in lista_pedidos if o["status"] == status]

def get_things_sorted(things):
    n = len(things)
    for i in range(n - 1):
        menor = i
        # Encontra o índice do menor código a partir de i
        for j in range(i + 1, n):
            if things[j]["code"] < things[menor]["code"]:
                menor = j
        # Troca os elementos, se necessário
        if menor != i:
            things[i], things[menor] = things[menor], things[i]
    return things

def save_data():
    # Usa o percurso em ordem da AVL para obter os dados em formato de lista (e ordenados)
    dados = {
        "all_orders": orders_tree.inorder_traversal_list(orders_tree.root),
        "catalog": catalog_tree.inorder_traversal_list(catalog_tree.root),
        "costumers": costumers # Continua sendo lista
    } 
    with open("dados.json", "w", encoding="utf-8") as arq:
        json.dump(dados, arq, indent=4, ensure_ascii=False)
#----------------------------------------------- Data implementation -------------------------------------------------#
def load_data():
    global catalog_tree, orders_tree, costumers # Indica que essas variáveis globais serão modificadas
    
    try:
        with open('dados.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    except FileNotFoundError:
        print("⚠️ Arquivo 'dados.json' não encontrado. Iniciando com dados vazios.")
        dados = {"all_orders": [], "catalog": [], "costumers": []}
    except json.JSONDecodeError:
        print("❌ Erro ao decodificar JSON. Iniciando com dados vazios.")
        dados = {"all_orders": [], "catalog": [], "costumers": []}

    # Carrega Catálogo (Reconstrói a AVL)
    catalog_tree = AVLTree()
    for item in dados['catalog']:
        catalog_tree.root = catalog_tree.insert(catalog_tree.root, item['code'], item)
    
    # Carrega Pedidos (Reconstrói a AVL - Usando a mesma chave 'code')
    orders_tree = AVLTree()
    for order in dados['all_orders']:
        orders_tree.root = orders_tree.insert(orders_tree.root, order['code'], order)

    # Carrega Clientes (Continua sendo Lista de Dicionários)
    costumers = dados['costumers']

    print("✅ Dados carregados e árvores AVL montadas.")


catalog_tree = AVLTree()  # Agora é uma árvore AVL
orders_tree = AVLTree()   # Agora é uma árvore AVL
#-----------------------------------------------Menu's functions-------------------------------------------------#

def consults(orders_tree, costumers):

    choice = ""
    width = 60
    while choice != "5":
        print("\n📋 Consult's menu:")
        print("-" * 40)
        print("[1] View All Orders".center(width))
        print("[2] Filter by status".center(width))
        print("[3] See all costumers".center(width))
        print("[4] Sales Report".center(width))
        print("[5] Back to Main Menu".center(width))
        choice = input("Choose an option (1 / 2 / 3 / 4 / 5): ".center(width))

        match choice:
            case "1":
                if not orders_tree:
                    print("⚠️ There's no orders to show.")
                    continue

                print("\n📋 List of orders:")
                print("-" * 40)
                lista_pedidos = orders_tree.inorder_traversal_list(orders_tree.root)
                for o in lista_pedidos:
                    items_names = [item['name'] for item in o['items_order']]
                    print(f"📦 Code: {o['code']}")
                    print(f"👤 Costumer: {o['costumer']}")
                    print(f"🛒 Items: {', '.join(items_names)}")
                    print(f"🗃️ Status: {o['status']}")
                    print(f"💰 Total: R${o['order_total_price']:.2f}")
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
                                items_names = [item['name'] for item in o['items_order']]
                                print(f"📦 Code: {order['code']}")
                                print(f"👤 Costumer: {order['costumer']}")
                                print(f"🛒 Items: {', '.join(items_names)}")
                                print(f"💰 Price: R${order['order_total_price']:.2f}")
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
                                items_names = [item['name'] for item in o['items_order']]
                                print(f"📦 Code: {order['code']}")
                                print(f"👤 Costumer: {order['costumer']}")
                                print(f"🛒 Items: {', '.join(items_names)}")
                                print(f"💰 Price: R${order['order_total_price']:.2f}")
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
                                items_names = [item['name'] for item in o['items_order']]
                                print(f"📦 Code: {order['code']}")
                                print(f"👤 Costumer: {order['costumer']}")
                                print(f"🛒 Items: {', '.join(items_names)}")
                                print(f"💰 Price: R${order['order_total_price']:.2f}")
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
                                items_names = [item['name'] for item in o['items_order']]
                                print(f"📦 Code: {order['code']}")
                                print(f"👤 Costumer: {order['costumer']}")
                                print(f"🛒 Items: {', '.join(items_names)}")
                                print(f"💰 Price: R${order['order_total_price']:.2f}")
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
                                items_names = [item['name'] for item in o['items_order']]
                                print(f"📦 Code: {order['code']}")
                                print(f"👤 Costumer: {order['costumer']}")
                                print(f"🛒 Items: {', '.join(items_names)}")
                                print(f"💰 Price: R${order['order_total_price']:.2f}")
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
                                items_names = [item['name'] for item in o['items_order']]
                                print(f"📦 Code: {order['code']}")
                                print(f"👤 Costumer: {order['costumer']}")
                                print(f"🛒 Items: {', '.join(items_names)}")
                                print(f"💰 Price: R${order['order_total_price']:.2f}")
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
                                items_names = [item['name'] for item in o['items_order']]
                                print(f"📦 Code: {order['code']}")
                                print(f"👤 Costumer: {order['costumer']}")
                                print(f"🛒 Items: {', '.join(items_names)}")
                                print(f"💰 Price: R${order['order_total_price']:.2f}")
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
                print("Active costumers:")
                for c in get_things_sorted(costumers.copy()):
                    print("-" * 30)
                    print(f"Code: {c['code']}")
                    print(f"Name: {c['name']}")
                    print(f"Cellphone: {c['cellphone']}")
                    print("-" * 30)
            case "4":
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
                        lista_pedidos = orders_tree.inorder_traversal_list(orders_tree.root)
                        for o in lista_pedidos:
                            acc_price = o['order_total_price'] 
                            total_price = total_price + acc_price   
                        print(f"\n📋 Number of registers: {len(orders_tree)}")                    
                        print(f"💰 Total value registered: R${total_price}")
                    case "2":
                        total_price = 0
                        acc_price = 0
                        delivered_orders = get_orders_by_status("Delivered")
                        for o in delivered_orders:
                            acc_price = o['order_total_price'] 
                            total_price = total_price + acc_price
                        print(f"\n📋 Number of registers: {len(delivered_orders)}")                    
                        print(f"💰 Total value registered: R${total_price}")                        
                    case "3":
                        print("🔙Returning to previous Menu.".center(width))
                        return
                    case _:
                        print("Invalid option. Please try again.".center(width))
            case "5":
                print("🔙Returning to Main Menu.".center(width))
                return
            case _:
                print("Invalid option. Please try again.".center(width))

def manage_menu_items(catalog_tree):
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
                code = len(catalog_tree) + 1
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
                new_item = create_item(code, name, description, price, stock)
                catalog_tree.root = catalog_tree.insert(catalog_tree.root, new_item['code'], new_item)
                save_data()
                print('Item added with sucess')

            case "2":
                width = 60
                catalog_code = int(input("Type the CODE of the item:\n".center(width))) 
                item_to_update = catalog_tree.search(catalog_tree.root, catalog_code) # Busca O(log n)               
                if item_to_update:
                        i = item_to_update
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
                                    update_name(i)
                                    save_data()
                                case "2":
                                    update_description(i)
                                    save_data()
                                case "3":
                                    update_price(i)
                                    save_data()
                                case "4":
                                    print(f"The item {i['name']} has {i['stock']} units in stock.".center(width))
                                    quantity = input("Type the new quantity you want to add or take from stock:\nUse a minus sign (-) to decrease stock\n".center(width))
                                    try:
                                        update_stock(i, quantity)
                                        save_data()
                                        print(f"Stock updated. New stock for {i['name']}: {i['stock']}".center(width))
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
                if not catalog_tree:
                    print("⚠️ No items on the menu.".center(width))
                    continue

                print("=" * width)
                print("📋 Menu List of Items".center(width))
                print("=" * width)

                items_to_display = catalog_tree.inorder_traversal_list(catalog_tree.root)
                for item in items_to_display:
                    print(f"📦 Code: {item['code']}".center(width))
                    print(f"📝 Name: {item['name']}".center(width))
                    print(f"🖊️ Description: {item['description']}".center(width))
                    print(f"💰 Price: R${item['price']}".center(width))
                    print(f"📦 Stock: {item['stock']}".center(width))
                    print("-" * width)
                    
            case "4":
                width = 60
                print("↩️ Returning to Main Menu.".center(width))
                return

            case _:
                width = 60
                print("❌ Invalid option. Please try again.".center(width))


def manage_orders(orders_tree, catalog_tree):
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
            case "1":
                name_costumer = input("What is the name of the costumer? ")
                number_costumer = input("What is the cellphone number of the costumer? ")
                code_costumer = len(costumers) +1
                new_costumer = {
                    "code": code_costumer,
                    "name": name_costumer,
                    "cellphone": number_costumer
                }

                code = len(orders_tree) + 1
                items_order = []
                payment = 'Paid'
                choice = ""
                while choice != "3":
                    print('1. Insert a new item')
                    print('2. Finish order')
                    print('3. Cancell order creation')
                    choice = input('\nChoose an option (1 / 2 / 3): ')

                    match choice:
                        case "1":
                            if catalog_tree == []:
                                print('The menu is empty, please add some items to proceed.')
                                return
                            
                            print("\n📋 Menu list of items:")
                            print("-" * 40)
                            items_to_display = catalog_tree.inorder_traversal_list(catalog_tree.root)
                            for item in items_to_display:
                                print(f"📦 Code: {item['code']}")
                                print(f"📝 Name: {item['name']}")
                                print(f"🖊️ Description: {item['description']}")
                                print(f"💰 Price: R${item['price']:.2f}")
                                print(f"📦 Stock: {item['stock']}")
                                print("-" * 40)
                            catalog_code = None
                            while catalog_code is None:
                                user_input = input('Choose a item by code: ').strip()
                                
                                if not user_input:
                                    print("⚠️ Entrada vazia. Por favor, digite o código do item.")
                                    continue
                                
                                try:
                                    catalog_code = int(user_input)
                                except ValueError:
                                    print("❌ Entrada inválida. Por favor, digite um número inteiro.")
                                    catalog_code = None
                                    continue
                            # Busca do Item (usando a AVL)
                            found_item = catalog_tree.search(catalog_tree.root, catalog_code)

                            if found_item:
                                if found_item['stock'] > 0:
                                    print(f"\nItem {catalog_code} added with success")
                                    item_for_order = found_item.copy()
                                    item_for_order['quantity'] = 1
                                    items_order.append(item_for_order)
                                    print(f"\n{name_costumer}'s order items are: {[i['name'] for i in items_order]}")
                                    update_stock(found_item, -1)
                                    save_data()
                                    print(f"The current stock for this item is: {found_item['stock']}")
                                else:
                                    print("Stock insuficiente")
                                    print(f"The current stock for this item is: {found_item['stock']}\n")
                                    break
                            if not found_item:
                                print("Item not found")
                            
                        case "2":
                            if len(items_order) == 0:
                                print("Order must have at least one item!")
                                continue

                            order = create_order(
                                code = code, 
                                costumer_data = new_costumer, 
                                items_order = items_order, 
                                status = "Pending", 
                                payment = payment
                            )

                            print(f"The current value of the order is: R${order['order_total_price']:.2f}")

                            discount_choice = input("Would you like to apply a discount coupon of 10%? (1. Yes / 2. No): ")

                            match discount_choice:
                                case "1":
                                    apply_order_discount(order) 
                                    print(f"\nCoupon applied successfully. New total: R${order['order_total_price']:.2f}")
                                case "2": 
                                    print(f"\nNo discount applied. Total: R${order['order_total_price']:.2f}")
                                case _:
                                    print("Invalid option. Proceeding without discount.")

                            order['status'] = "Pending"
                            orders_tree.root = orders_tree.insert(orders_tree.root, order['code'], order)
                            costumers.append(new_costumer)
                            save_data()

                            print("\n✅ Order added with sucess!")
                            print("-" * 40)
                            print(f"Code: {order['code']}")
                            print(f"Costumer: {order['costumer']}")
                            print(f"Items: {', '.join([item['name'] for item in order['items_order']])}")
                            print(f"Status: {order['status']}")
                            print(f"Total: R${order['order_total_price']:.2f}")
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
                items_names = [item['name'] for item in order['items_order']]
                items_display = ', '.join(items_names)
                print(f"Code: {order['code']}")
                print(f"Costumer: {order['costumer']}")
                print(f"Items: {items_display}")
                print(f"Total: R${order['order_total_price']:.2f}")
                print(f"Status: {order['status']}")
                print("=" * width)

                print("[1] Accept order".center(width))
                print("[2] Reject order".center(width))
                print("[3] Return to Manage Orders\n".center(width))
                choice = input("Choose an option (1 / 2 / 3):".center(width))

                if choice == "1":
                    order['status'] = "Accepted"
                    save_data()
                    print("✅ Order accepted with success!".center(width))
                elif choice == "2":
                    order['status'] = "Rejected"
                    save_data()
                    for item in order['items_order']: 
                        lista_catalogo = catalog_tree.inorder_traversal_list(catalog_tree.root)
                        original_item = next((i for i in lista_catalogo if i["name"] == item["name"]), None)
                        if original_item:
                            update_stock(original_item, item["quantity"])
                            save_data()
                    print("❌ Order rejected.".center(width))
                elif choice == "3":
                    print("🔙 Returning to Manage Orders...".center(width))
                else:
                    print("⚠️ Invalid option.".center(width))
                            
            case "3":
                if not orders_tree:
                    print("⚠️ No available orders to update.".center(width))
                    continue

                print("=" * width)
                print("📋 Orders Available".center(width))
                print("=" * width)

                lista_pedidos = orders_tree.inorder_traversal_list(orders_tree.root)
                for idx, order in enumerate(lista_pedidos, start=1):
                    print(f"{idx}. Code: {order['code']} | Costumer: {order['costumer']['name']} | Status: {order['status']}".center(width))

                try:
                    order_index = int(input("Select an order by code:".center(width))) - 1
                    order = lista_pedidos[order_index]
                except (ValueError, IndexError):
                    print("❌ Invalid selection.".center(width))
                    continue

                print("=" * width)
                print("📦 Selected Order".center(width))
                print("=" * width)

                items_names = [item['name'] for item in order['items_order']]
                items_display = ', '.join(items_names)

                print(f"Code: {order['code']}")
                print(f"Costumer: {order['costumer']}")
                print(f"Items: {items_display}")
                print(f"Total: R${order['order_total_price']:.2f}")
                print(f"Status: {order['status']}")
                print("=" * width)

                print("=" * width)
                print("🔄 Choose new status:".center(width))
                print("=" * width)
                print("[1] Making".center(width))
                print("[2] Ready".center(width))
                print("[3] Waiting Delivery".center(width))
                print("[4] Delivering".center(width))
                print("[5] Delivered".center(width))

                status_choice = input("Choose an option (1-5):".center(width))

                match status_choice:
                    case "1": order['status'] = "Making"
                    case "2": order['status'] = "Ready"
                    case "3": order['status'] = "Waiting Delivery"
                    case "4": order['status'] = "Delivering"
                    case "5": order['status'] = "Delivered"
                    case _: 
                        print("❌ Invalid option.".center(width))
                        continue
                save_data()

                print("✅ Order updated with success!".center(width))

            case "4":
                if not orders_tree:
                    print("⚠️ No orders available.".center(width))
                    continue

                lista_pedidos = orders_tree.inorder_traversal_list(orders_tree.root)
                cancellable_orders = [o for o in lista_pedidos if o['status'] in ("Pending", "Accepted")]
                if not cancellable_orders:
                    print("⚠️ No cancellable orders available.".center(width))
                    continue

                print("=" * width)
                print("📋 Orders Available for Cancelling".center(width))
                print("=" * width)

                for idx, order in enumerate(cancellable_orders, start=1):
                    print(f"{idx}. Code: {order['code']} | Costumer: {order['costumer']['name']} | Status: {order['status']}".center(width))

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
                        order['status'] = "Canceled"
                        save_data()
                        for item in order['items_order']:
                            lista_catalogo = catalog_tree.inorder_traversal_list(catalog_tree.root)
                            original_item = next((i for i in lista_catalogo if i["name"] == item["name"]), None)
                            if original_item:
                                update_stock(original_item, item["quantity"])
                                save_data()
                        print(f"✅ Order {order['code']} canceled with success!".center(width))
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
                manage_menu_items(catalog_tree)
            case "2":
                manage_orders(orders_tree, catalog_tree)
            case "3":
                consults(orders_tree, costumers)
            case "4":
                print("\nExiting the system. Goodbye!\n".center(width))
                return
            case _:
                print("Invalid option. Please try again.".center(width))

load_data()
main_menu()