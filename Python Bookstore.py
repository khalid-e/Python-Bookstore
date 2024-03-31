from abc import ABC, abstractmethod
import uuid  # Import the UUID module for generating unique IDs
class Book:
    def __init__(self, isbn, title, authors, overview):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.overview = overview

class User(ABC):
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

class RegisteredUser(User):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email, password)
        self.order_history = []
        self.itemAvailableDict = {}
        self.shoppingDict = {}

    @staticmethod
    def read_existing_users():
        try:
            with open("registeredpeople.txt", "r") as file:
                read = file.readlines()
            existing_users = [line.strip().split(",")[2] for line in read]
            return existing_users
        except FileNotFoundError:
            return []
    # Method to register a new user
    def register(self):
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")

        # Validate email
        while "@" not in email or "." not in email or len(email) <= 6:
            print("Invalid email. Please enter a valid email address.")
            email = input("Enter your email: ")

        # Check if the email already exists
        existing_users = self.read_existing_users()
        while email in existing_users:
            print("Email already exists. Please choose a different email.")
            email = input("Enter your email: ")

        password = input("Enter your password: ")

        with open("registeredpeople.txt", "a") as file:
            file.write(f"\n{first_name},{last_name},{email},{password}")
        print("Registration successful.")

        # Return the created RegisteredUser instance
        return RegisteredUser(first_name, last_name, email, password)
    # Method to register a new user
    def user_login(self, email):
        try:
            password = input("Enter password: ")
            with open("registeredpeople.txt", "r") as file:
                read = file.readlines()
            user_info = []

            for line in read:
                elements = line.strip().split(",")
                user_info.append(elements)

            for elements in user_info:
                if email == elements[2]:
                    if password == elements[3]:
                        print('Login successful')
                        return True
                    else:
                        print('Invalid login')
                        break
        except:
            print('Invalid login')
    # Method to modify user account details
    def modify_account_details(self):
        self.first_name = input("Enter new first name: ")
        self.last_name = input("Enter new last name: ")
        self.password = input("Enter new password: ")
        self.save_details()
    
    def save_details(self):
        with open("registeredpeople.txt", "r") as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if self.email in line:
                elements = line.strip().split(",")
                elements[0] = self.first_name
                elements[1] = self.last_name
                elements[3] = self.password
                lines[i] = ",".join(elements) + "\n"

        with open("registeredpeople.txt", "w") as file:
            file.writelines(lines)

        print("Account details modified successfully.")
    # Method to view book details from a given file 
    def view_book_details(self, file_path):
        with open(file_path, 'r') as file:
            contents = file.read()
            print(contents)
    # Method to display available books and their prices
    def available_books(self):
        with open("Bookdataset.txt") as my_file:
            itemsAvailable = my_file.readlines()

        for item in itemsAvailable:
            fields = [field.strip().strip('"') for field in item.strip().split('" "')]
            if len(fields) >= 3:
                item_title = fields[1]
                item_price = fields[-1]
                print(f"{item_title}: {item_price}")
                self.itemAvailableDict.update({item_title: float(item_price)})
    # Method for Adding or Removing Book from basket
    def add_book_basket(self):
        proceed_shopping = input('Do you wish to continue shopping (yes/no): ')

        while proceed_shopping.lower() == 'yes':
            action = input('Do you want to add or remove a book? Enter "add" or "remove": ')

            if action.lower() == 'add':
                item_added = input('Add a book: ').lower()
                matching_books = [key for key in self.itemAvailableDict if key.lower() == item_added]

                if matching_books:
                    item_qty = int(input('Add quantity: '))
                    if type(item_qty) == int and item_qty > 0:
                        self.shoppingDict[item_added] = {'quantity': item_qty, 'subtotal': self.itemAvailableDict[matching_books[0]] * item_qty}
                        print(f"{item_qty} {item_added}(s) added to the basket.")
                    else:
                        print("Invalid quantity. Please enter a positive integer.")
                else:
                    print('Unable to add unavailable book')

            elif action.lower() == 'remove':
                item_to_remove = input('Remove a book from the basket: ').lower()
                if item_to_remove in self.shoppingDict:
                    del self.shoppingDict[item_to_remove]
                    print(f"{item_to_remove} removed from the basket.")
                else:
                    print(f"{item_to_remove} not found in the basket.")

            else:
                print("Invalid action. Please enter 'add' or 'remove'.")

            proceed_shopping = input('Do you wish to add more items or remove any (yes/no): ')

        
    # Method for Adding or Removing Book from basket
    def add_book_basket_guest(self):
        proceed_shopping = input('Do you wish to continue shopping (yes/no): ')

        while proceed_shopping.lower() == 'yes':
            action = input('Do you want to add or remove a book? Enter "add" or "remove": ')

            if action.lower() == 'add':
                item_added = input('Add a book: ').lower()
                matching_books = [key for key in self.itemAvailableDict if key.lower() == item_added]

                if matching_books:
                    item_qty = int(input('Add quantity: '))
                    if type(item_qty) == int and item_qty > 0:
                        self.shoppingDict[item_added] = {'quantity': item_qty, 'subtotal': self.itemAvailableDict[matching_books[0]] * item_qty}
                        print(f"{item_qty} {item_added}(s) added to the basket.")
                    else:
                        print("Invalid quantity. Please enter a positive integer.")
                else:
                    print('Unable to add unavailable book')

            elif action.lower() == 'remove':
                item_to_remove = input('Remove a book from the basket: ').lower()
                if item_to_remove in self.shoppingDict:
                    del self.shoppingDict[item_to_remove]
                    print(f"{item_to_remove} removed from the basket.")
                else:
                    print(f"{item_to_remove} not found in the basket.")

            else:
                print("Invalid action. Please enter 'add' or 'remove'.")

            proceed_shopping = input('Do you wish to add more items or remove any (yes/no): ')

        print('You are not signed into an account, Register or Login to complete the purchase')
    # Method to display a bill summary and complete the checkout process   
    def checkout(self):
        print("\n-----Bill Summary-----")
        print("Item     Quantity      SubTotal")
        total = 0
        for key in self.shoppingDict:
            print(f"{key}         {self.shoppingDict[key]['quantity']}       {self.shoppingDict[key]['subtotal']}")
            total += self.shoppingDict[key]['subtotal']
        print(f'Total: {total}')
        print('Thank You\nHope to see you soon')

        # Generate a unique order ID using uuid
        order_id = str(uuid.uuid4())

        # Save the order details to the order history
        order_details = {
            'order_id': order_id,
            'items': self.shoppingDict,
            'total': total
        }

        # Append the order details to the order history list
        self.order_history.append(order_details)

        # Save the order history to a file
        with open("orderhistory.txt", "a") as order_file:
            order_file.write(f"{self.email}, {order_details}\n")

        # Clear the shopping cart after checkout
        self.shoppingDict = {}
    # Method to display user order history
    def view_order_history(self):
        print("\n-----Order History-----")
        for order in self.order_history:
            print(f"Order ID: {order['order_id']}")
            print("Item     Quantity      SubTotal")
            for key in order['items']:
                print(f"{key}         {order['items'][key]['quantity']}       {order['items'][key]['subtotal']}")
            print(f'Total: {order["total"]}\n')
        
    # View Account Details
    def view_account_details(self):
        print("\n-----Account Details-----")
        print(f"First Name: {self.first_name}")
        print(f"Last Name: {self.last_name}")
        print(f"Email: {self.email}")
        print(f"Password: {self.password}")
        
    def remove_book_basket(self):
        pass
# Function to read user account information from a file based on the email
def readAccount(email):
    while True:
        try:
            with open("registeredpeople.txt", "r") as file:
                for x in file:
                    info = x.strip().split(",")
                    user = RegisteredUser(info[0], info[1], info[2], info[3])
                    if email == info[2]:
                        return user
        except FileNotFoundError:
            print('File not Found')
            file = open("registeredpeople.txt", "w")

def main():
    books = [
        Book("9781234567890", "The Great Gatsby", ["F. Scott Fitzgerald"], "Classic novel set in the Jazz Age."),
    ]

    registered_user = None      # Initialize the registered user variable

    while True:
        print('*********************Welcome to the Book Store***************************')
        print("\n1. Register\n2. Login\n3. Continue as Guest\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            registered_user = RegisteredUser('first_name', 'last_name', 'email', 'password')         # Create and register a new user
            registered_user = registered_user.register()

            while True:
                print("\n1. View Book Details\n2. Check Books Available\n3. Modify Account Details\n4. View Order History\n5. View Account Details\n6. Logout")
                user_choice = input("Enter your choice: ")

                if user_choice == "1":
                    file_path = "Bookdataset.txt"
                    registered_user.view_book_details(file_path)     # View Books

                elif user_choice == "2":
                    print('-----Books Available-------')
                    registered_user.available_books()

                    registered_user.add_book_basket()           # Add books to the basket
                    check_out = input('Do you want to checkout (yes/no): ')     # Prompt for checkout
                    if check_out.lower() == 'yes':
                        registered_user.checkout()
                    else:
                        break

                elif user_choice == "3":
                    registered_user.modify_account_details()
                    print("Modified Details:")                              # Printing modified details
                    print(f"First Name: {registered_user.first_name}")
                    print(f"Last Name: {registered_user.last_name}")
                    print(f"Email: {registered_user.email}")
                    print(f"Password: {registered_user.password}")
                    
                elif user_choice == "4":
                    registered_user.view_order_history()
                    
                elif user_choice == "5":
                    registered_user.view_account_details()

                elif user_choice == "6":
                    registered_user = None
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "2":
            registered_user = RegisteredUser("first_name", "last_name", "email", "password")        # Login process for existing user
            email = input("Enter email: ")
            login_success = registered_user.user_login(email)
            if login_success:
                registered_user = readAccount(email)             # If login is successful, read the account information and proceed
                while True:
                    print("\n1. View Book Details\n2. Check Books Available\n3. Modify Account Details\n4. View Order History\n5. View Account Details\n6. Logout")
                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        file_path = "Bookdataset.txt"
                        registered_user.view_book_details(file_path)

                    elif user_choice == "2":
                        print('-----Books Available-------')
                        registered_user.available_books()
                        registered_user.add_book_basket()
                        check_out = input('Do you want to checkout (yes/no): ')
                        if check_out.lower() == 'yes':
                            registered_user.checkout()
                        else:
                            break

                    elif user_choice == "3":
                        registered_user.modify_account_details()
                        print("Modified Details:")
                        print(f"First Name: {registered_user.first_name}")
                        print(f"Last Name: {registered_user.last_name}")
                        print(f"Email: {registered_user.email}")
                        print(f"Password: {registered_user.password}")
                        
                    elif user_choice == "4":
                        registered_user.view_order_history()
                        
                    elif user_choice == "5":
                        registered_user.view_account_details()

                    elif user_choice == "6":
                        registered_user = None
                        break
                    else:
                        print("Invalid choice. Please try again.")
                        user_choice

        elif choice == "3":
            user = None
            print("Continuing as Guest.")

            while True:
                print("\n1. View Book Details\n2. Check Books Available")
                user_choice = input("Enter your choice: ")

                if user_choice == "1":
                    registered_user = RegisteredUser("John", "Doe", "john@example.com", "password123")
                    file_path = "Bookdataset.txt"

                    registered_user.view_book_details(file_path)

                elif user_choice == "2":
                    print('-----Books Available-------')
                    registered_user.available_books()
                    registered_user.add_book_basket_guest()
                    break

                else:
                    print('Invalid choice, Try again')

        elif choice == "4":
            print("Exiting the Bookstore.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
