# program will calculate how the required savings rate via a bisection search

import numpy # allows us to use the sign function

print('Enter the starting salary: ', end = '')
annual_salary = float(input())

semi_annual_raise = .07
r = 0.04
portion_down_payment = 0.25
total_cost = 1000000
need_to_save = portion_down_payment * total_cost
years = 3
months = years * 12

# If saving 100% of our salary doesn't get us to the down payment, then it's impossible and we exit
if years * annual_salary < need_to_save:
    print('It is not possible to pay the down payment in three years.', end = '')
    sys.exit()

def f(rate):
    rate = rate / 10000 # must divide by 10000 to convert to float for rate
    monthly_salary = annual_salary / 12
    current_savings = 0
    for month in range(1, months + 1):
        current_savings += current_savings*r/12
        current_savings += rate * monthly_salary
        if month%6 == 0:
            monthly_salary += monthly_salary * semi_annual_raise
    return current_savings - need_to_save # need to return the difference to compare against the tolerance

a = 0 # min rate
b = 10000 # max rate
tolerance = 100 # $100 tolerance

i = 1
while i <= 100:
    c = int((a + b) / 2) # compute midpoint each iteration
    fa = f(a) # compute function with min rate input
    fc = f(c) # compute function with midpoint rate input
    if fc == 0 or abs(fc) < tolerance: # we finish and exit when we achieve a rate that puts us within $100 dollars of the down payment
        print('Best savings rate: ' + str(c / 10000))
        print('Steps in bisection search:​' + str(i), end = '')
        break
    i += 1
    if numpy.sign(fc) == numpy.sign(fa): # if both the min and midpoint are on the same side, then the min becomes the old midpoint
        a = c
    else: # otherwise, the max becomes the old midpoint
        b = c
    
