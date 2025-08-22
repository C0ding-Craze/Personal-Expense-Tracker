import json
from datetime import datetime
import csv
import os

def load_expenses():
    try:
        with open("My_Expenses.json", "r") as f:
            return json.load(f) 
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_expenses(expenses):
    with open("My_Expenses.json", "w") as f:
        json.dump(expenses, f, indent=4)

def add_expenses(expenses):
    try: 
        amount = float(input("\nEnter the amount: "))
        category = input("Enter the category (e.g., 'Groceries', 'Rent'): ")
        date = input("Enter the date (YYYY-MM-DD): ")
        description = input("Enter a description (optional): ")

        if amount<=0:
            print("Please enter a valid amount.")
            add_expenses(expenses)

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("\nInvalid date format. Please use YYYY-MM-DD.")
            return ""

        expense = {
                    "amount": amount,
                    "category": category,
                    "date": date,
                    "description": description
                }
        
        expenses.append(expense)
        save_expenses(expenses)
        print("\nExpense added successfully!")

    except Exception as e:
        print(e)

def view_expenses(expenses):
    if not expenses:
        print("\nThere are no expenses recorded yet.")
        return ""
   
    filter_choice = input("\nFilter by (1) Category, (2) Date Range or (3) for no filter: ")

    if filter_choice == "1":
        category = input("\n\tSelect the category to filter: ")
        filtered_expenses = [exp for exp in expenses if exp["category"].lower() == category.lower()]

    elif filter_choice == "2":
        start_date = input("\tEnter the satrting date (YYYY-MM-DD): ")
        end_date = input("\tEnter the ending date (YYYY-MM-DD): ")

        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("\nInvalid date format. Please use YYYY-MM-DD.")
            return ""

        filtered_expenses = [exp for exp in expenses if  start_date <= exp["date"] <= end_date ]

    elif filter_choice == "3":
            filtered_expenses = expenses

    else:
        print("\nInvalid choice. Please choose a valid option.")
        return ""

    if not filtered_expenses:
        print("\nThere is no such expenses that matches the specified filter.")

    else:
        for exp in filtered_expenses:
            print(f"\n Amount: Rs.{exp["amount"]}\n Category: {exp["category"]}\n Date: {exp["date"]}\n Description: {exp["description"]}")
        
def analyze_expense(expenses):
    if not expenses:
        print("\nThere aren't any expenses to analyze.")
        return ""

    total_spent = sum(exp["amount"] for exp in expenses)
    print(f"\nTotal amount spent: Rs. {total_spent}")

    category_spending = {} 

    for exp in expenses:
        category = exp["category"]
        category_spending[category] = category_spending.get(category, 0) + exp["amount"]

    print("Total spending by category:")
    for category, amount in category_spending.items():
        print(f"{category}: Rs. {amount}")

    if category_spending:
        highest_category = max(category_spending, key=category_spending.get) # type: ignore
        print(f"\nThe highest spending category is: {highest_category}, with amount : {category_spending[highest_category]}")

def export_csv(expenses):
    filename = input("\nChoose a filename for the CSV (without extension): ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return ""

    filename += ".csv"

    if os.path.exists(filename):
        confirm = input(f"\n{filename} already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if confirm != "y":
            print("Export cancelled.")
            return ""

    try:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Amount", "Category", "DAte", "Description"])
            for exp in expenses:
                writer.writerow([exp.get("amount"), exp.get("category"), exp.get("date"), exp.get("description")])
        print(f"Expenses exported successfully to {filename}")   
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    expenses = load_expenses()

    while True:
        print("\n\t-----------Expense Tracker Menu-----------\n")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Analyze expenses")
        print("4. Export to CSV")
        print("5. Exit")
        choice = input("\nChoose an option from above (1,2,3 or 4): ")

        if choice == "1":
            add_expenses(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            analyze_expense(expenses)
        elif choice == "4":
            export_csv(expenses)
        elif choice == "5":
            print("\nExiting Expense Tracker....\n")
            break
        else:
            print("\nInvalid choice. Please choose a valid option.")


if __name__=="__main__": 
    main() 