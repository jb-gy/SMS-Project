"""STORE MANAGEMENT SYSTEM V1"""
import os


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @classmethod
    def invalid(cls):
        print(
            "\n\n\n                   INVALID INPUT                            \n\n\n"
        )


class StockManager:
    def __init__(self, u, p):
        self.username = u
        self.password = p

    @classmethod
    def load_stock(cls):
        content = {}
        if os.path.isfile("./stock.txt"):
            with open("./stock.txt") as file:
                data = file.read()
            return eval(data)
        return None

    def save_stock(self, stock):
        with open("./stock.txt", "w") as file:
            file.write(str(stock))
            return True
        return False

    def view(self, stock):
        print(
            "\n\nID\t  Name    \t Price\t  Qty\n==========================================="
        )
        for i in stock:
            print(f"{i}:\t{stock[i]['name']}\t{stock[i]['price']}\t{stock[i]['qty']}")

    # ===============================================================================================================================================
    # MANAGER INTERFACE
    def process(self, s):
        if self.username == "admin":
            if self.password == "manager":
                while True:
                    admin_option = input(
                        "SELECT ADMIN OPTION\n(1) Add new items to stock\n(2) Edit existing stock\n(3) View stock\n(4) Delete item from stock\n(#) Return to main menu\n\n Enter option: "
                    )
                    if admin_option == "1":
                        self.add(s)
                        self.save_stock(s)
                    elif admin_option == "2":
                        self.edit(s)
                        self.save_stock(s)
                    elif admin_option == "3":
                        self.view(s)
                    elif admin_option == "4":
                        self.delete(s)
                        self.save_stock(s)
                    elif admin_option == "#":
                        break
                    else:
                        Product.invalid()

            else:
                print(
                    "\n\n\n                   ERROR:INVALID PASSWORD!!                            \n\n\n"
                )

        else:
            print(
                "\n\n\n                   ERROR:INVALID PASSWORD!!                            \n\n\n"
            )

    # ===========================================================================================================================================================

    def add(self, s):
        self.view(s)
        name = input("Enter name: ")
        price = eval(input("Enter price: "))
        qty = int(input("Enter qty: "))
        item = {"name": name, "price": price, "qty": qty}
        proc = int(list(s)[-1])
        newnum = proc + 1
        s[str(newnum)] = item
        self.save_stock(s)

    def delete(self, s):
        self.view(s)
        id = input("item id: ")
        del s[id]
        self.save_stock(s)

    def edit(self, s):
        def edit_qty(s):
            while True:
                option = input(
                    "1: Add to qty\n2: Remove from qty"
                    + "\n#: previous menu\nEnter option: "
                )

                if option == "1":
                    qty = int(input("Enter qty: "))
                    s[id]["qty"] += qty
                    break
                elif option == "2":
                    qty = int(input("Enter qty: "))
                    s[id]["qty"] -= qty
                    break
                elif option == "#":
                    break
                else:
                    Product.invalid()
                    break

        while True:
            self.view(s)

            option = input(
                "1: Edit name\n2: Edit price\n3: Edit qty"
                + "\n#: previous menu\nEnter option:  "
            )
            id = input("Enter item id: ")
            if option == "1":
                name = input("Enter new name: ")
                s[id]["name"] = name
                self.save_stock(s)
            elif option == "2":
                price = input("Enter new price: ")
                s[id]["price"] = eval(price)
                self.save_stock(s)
            elif option == "3":
                edit_qty(s)
                self.save_stock(s)
            elif option == "#":
                break
            else:
                Product.invalid()


class Customer:
    def __init__(self, name):
        self.name = name

    # ===============================================================================================================
    # CUSTOMER INTERFACE
    def operation(self, stock):
        self.wallet = float(input("Enter your budget: "))
        print(f"Welcome {self.name}, you have N{self.wallet} to shop with us ")
        cart = {}
        total = 0
        while True:
            total = 0
            option = input(
                "1: shopping\n2: edit cart\n3: show cart\n4: checkout\n#: Exit\nEnter option:  "
            )
            if option == "1":
                self.shopping(stock, cart)

            elif option == "2":
                self.editcart(cart, stock)

            elif option == "3":
                self.showcart(cart)

            elif option == "4":
                self.checkout(cart, stock)
            elif option == "#":
                print(f"Till next time {self.name} ..............")
                break
            else:
                Product.invalid()

    # =============================================================================================================================#

    def shopping(self, stock, cart):
        print("\nItem in stock...\n=====================================")
        print("ID\tName    \tPrice\tQty\n=====================================")
        for i in stock:
            print(f"{i}:\t{stock[i]['name']}\t{stock[i]['price']}\t{stock[i]['qty']}")
        print("=====================================")
        id = input("Enter item no: ")
        if id in stock:
            if id in cart:
                print("item already added")

            else:
                qty = int(input("Enter quantity: "))
                if qty <= stock[id]["qty"]:
                    item = {
                        "name": stock[id]["name"],
                        "price": stock[id]["price"],
                        "qty": qty,
                    }
                    stock[id]["qty"] -= qty
                    cart[id] = item

        else:
            print("Item not in stock")

    def editcart(self, cart, stock):
        while True:
            total = 0
            print("\nItem in cart...\n=====================================")
            print("ID\tName    \tPrice\tQty\n=====================================")
            for i in cart:
                print(f"{i}:\t{cart[i]['name']}\t{cart[i]['price']}\t{cart[i]['qty']}")
                total += cart[i]["qty"] * cart[i]["price"]
            print("=====================================")
            print(f"Total: {total}\n")
            id = input("Enter item id: ")
            if id in cart:
                option = input(
                    "1: Add to quantity\n2: Remove from quantity\n3: Delete Item from cart\n\nEnter option: "
                )
                if option == "1":
                    qty = int(input("Enter value: "))
                    if qty <= stock[id]["qty"]:
                        cart[id]["qty"] += qty
                        stock[id]["qty"] -= qty

                    else:
                        print(f"{stock[id]['name']} not enough in stock")
                elif option == "2":
                    qty = int(input("Enter value: "))
                    if qty <= cart[id]["qty"]:
                        stock[id]["qty"] += qty
                        cart[id]["qty"] -= qty
                    else:
                        print("\n\n    invalid qty value    \n\n")

                elif option == "3":
                    del cart[id]
                    print("Item deleted from cart")

                else:
                    Product.invalid()
                    break
                if cart[id]["qty"] == 0:
                    del cart[id]

            else:
                print("\n\n    INVALID ID    \n\n")
                continue
            ans = input(
                "Done editing? Press # to go to previous menu or any other key to continue editing\n "
            )
            if ans != "#":
                continue
            else:
                break

    def showcart(self, cart):
        total = 0
        print("\nItem in cart...\n=====================================")
        print("ID\tName    \tPrice\tQty\n=====================================")
        for i in cart:
            print(f"{i}:\t{cart[i]['name']}\t{cart[i]['price']}\t{cart[i]['qty']}")
            total += cart[i]["qty"] * cart[i]["price"]
        print("=====================================")
        print(f"Total: {total}")
        print("=====================================")

    def checkout(self, cart, stock):
        if len(cart) > 0:
            total = 0
            print("\nItem in cart...\n=====================================")
            print("ID\tName    \tPrice\tQty\n=====================================")
            for i in cart:
                print(f"{i}:\t{cart[i]['name']}\t{cart[i]['price']}\t{cart[i]['qty']}")
                total += cart[i]["qty"] * cart[i]["price"]
            print("=====================================")
            print(f"Total: {total}\n")
            print("=====================================")
            balance = self.wallet - total
            print(f"balance: {balance}\n")
            print("=====================================")
            if balance < 0:
                print("insufficient funds\npls, drop some items")
            else:
                self.save_stock(stock)
                self.save_order(cart, total)
                cart.clear()
                print(f"Thanks for patronage {self.name},\nSee you very soon")
        else:
            print("No item in shopping cart...")

    def save_stock(self, stock):
        with open("./stock.txt", "w") as file:
            file.write(str(stock))
            file.close()
            return True
        return False

    def save_order(self, order, total):
        with open("./cart.txt", "a") as file:
            file.write(f"\n\nCustomer: {self.name}\n\t{str(order)}\nTotal: {total}\n\n")
            file.close()
            return True
        return False


class App:
    @classmethod
    def interface(cls):
        stock = StockManager.load_stock()
        if not stock:
            print("File does not exist........")
        # ========================================================================================================================================================================
        # MAIN INTERFACE
        while True:
            choice = input(
                "Welcome to JB's fruit store......\nYou are logging in as:\n(1) A Customer\n(2) The Store Manager\n(#) Exit\n\nPick option:   "
            )
            if choice == "1":
                cusname = input("Enter your name:  ")
                Customer1 = Customer(cusname)
                Customer1.operation(stock)

            elif choice == "2":
                user = input("Enter username: ")
                password = input("Enter password: ")
                manager1 = StockManager(user, password)
                manager1.process(stock)

            elif choice == "#":
                break

            else:
                Product.invalid()


# ==================================================================================================================================================================================


if __name__ == "__main__":
    App.interface()
