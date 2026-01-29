import mysql.connector

# Database Connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4442",   # change if needed
    database="general_store"
)

cur = con.cursor()

# ---------------- CHATBOT FUNCTION ----------------
def chat_bot():
    print("\n--- Welcome to General Store Chat Bot ---")
    print("Type 'bye' to exit chat\n")

    while True:
        question = input("You: ").lower()

        # Greetings
        if question == "hi":
            print("Bot: Hello! Welcome to the General Store 😊")

        elif question == "hello":
            print("Bot: Hi there! How can I help you today?")

        elif question == "good morning":
            print("Bot: Good morning! What would you like to do?")

        elif question == "bye":
            print("Bot: Thank you for visiting. Have a nice day!")
            break

        # Store timing
        elif "timing" in question:
            print("Bot: Our store is open from 9 AM to 9 PM.")

        # What items do you sell?
        elif "items" in question:
            cur.execute("SELECT product_name FROM Products")
            data = cur.fetchall()
            print("Bot: We sell the following items:")
            for i in data:
                print("-", i[0])

        # Price of product
        elif "price" in question:
            pname = input("Enter product name: ").lower()
            cur.execute("SELECT price FROM Products WHERE product_name=%s", (pname,))
            result = cur.fetchone()
            if result:
                print("Bot: Price of", pname, "is ₹", result[0])
            else:
                print("Bot: Product not found.")

        # Availability check
        elif "available" in question or "sell" in question:
            pname = input("Enter product name: ").lower()
            cur.execute("SELECT quantity FROM Products WHERE product_name=%s", (pname,))
            result = cur.fetchone()
            if result and result[0] > 0:
                print("Bot: Yeah,", pname, "is available.")
            else:
                print("Bot:","We are So sorry", pname, "is not available.")

        else:
            print("Bot: Sorry, I didn't understand your question.")

# ---------------- STORE FUNCTIONS ----------------
def add_product():
    pid = int(input("Product ID: "))
    name = input("Product Name: ").lower()
    price = float(input("Price: "))
    qty = int(input("Quantity: "))
    cur.execute("INSERT INTO Products VALUES (%s,%s,%s,%s)", (pid, name, price, qty))
    con.commit()
    print("Product added successfully.")

def view_products():
    cur.execute("SELECT * FROM Products")
    data = cur.fetchall()
    print("\nID  Name   Price   Quantity")
    for i in data:
        print(i)

def update_stock():
    pid = int(input("Enter Product ID: "))
    qty = int(input("Enter new quantity: "))
    cur.execute("UPDATE Products SET quantity=%s WHERE product_id=%s", (qty, pid))
    con.commit()
    print("Stock updated.")

def generate_bill():
    bill = int(input("Bill No: "))
    cid = int(input("Customer ID: "))
    pid = int(input("Product ID: "))
    qty = int(input("Quantity Sold: "))

    cur.execute("SELECT price FROM Products WHERE product_id=%s", (pid,))
    price = cur.fetchone()[0]
    total = price * qty

    cur.execute("INSERT INTO Sales VALUES (%s,%s,%s,%s,%s)",
                (bill, cid, pid, qty, total))
    con.commit()
    print("Bill Generated. Total Amount = ₹", total)

def view_sales():
    cur.execute("SELECT * FROM Sales")
    data = cur.fetchall()
    print("\nBill  CustID  ProdID  Qty  Total")
    for i in data:
        print(i)

# ---------------- MAIN MENU ----------------
while True:
    print("\n===== GENERAL STORE BOT MENU =====")
    print("1. Chat with Store Bot")
    print("2. Add New Product")
    print("3. View Products")
    print("4. Update Stock")
    print("5. Generate Bill")
    print("6. View Sales")
    print("7. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        chat_bot()
    elif choice == 2:
        add_product()
    elif choice == 3:
        view_products()
    elif choice == 4:
        update_stock()
    elif choice == 5:
        generate_bill()
    elif choice == 6:
        view_sales()
    elif choice == 7:
        print("Thank you for using General Store Bot!")
        break
    else:
        print("Invalid choice.")

