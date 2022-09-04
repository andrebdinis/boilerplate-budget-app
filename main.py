# This entrypoint file to be used in development. Start by reading README.md
import budget
from budget import create_spend_chart
from unittest import main

# input
food = budget.Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = budget.Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = budget.Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

# output
print(food, "\n")
print(clothing, "\n")
print(auto, "\n")
chart = create_spend_chart([food, clothing, auto])
print(chart)
#print(chart.__repr__())

# Run unit tests automatically
main(module='test_module', exit=False)