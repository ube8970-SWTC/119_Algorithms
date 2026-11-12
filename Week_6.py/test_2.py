# Program is from Week 1 Task 1 of the python course.

tires_purchased = 5
price_each = 129
#Price is the cost of one new tire for my plow truck
# changed items_purchased to tires_purchased to narrow down what I'm representing

subtotal = tires_purchased * price_each
tax_rate = 0.05
# input Wisconsin tax rate 

tax_amount = subtotal * tax_rate
total = subtotal + tax_amount

print("tires purchased: ", tires_purchased)
print("price each: ", price_each)

# Where the error was that I'm using for Week 4 Assignment 1
# print("tax rate: ", subtotal)
# Instead of it reading as the subtotal, it was reading as the tax rate, which is incorrect.
# The solution was to change the subtotal to tax rate in the print statement, which is what I needed to use in the total equation.
print("subtotal: ", subtotal)

#put tax rate in place of subtotal, has been corrected
print("tax rate: ", tax_rate)
print("tax amount: ", tax_amount)
print("total: ", total)