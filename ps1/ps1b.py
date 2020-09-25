# program will calculate how many months
# it will take to save enough money for the down payment

print('Enter your annual salary:', end = '')
annual_salary = float(input())
print('Enter the percent of your salary to save, as a decimal:', end = '')
portion_saved = float(input())
print('Enter the cost of your dream home:', end = '')
total_cost = float(input())
print('Enter the semi­annual raise, as a decimal:', end = '')
semi_annual_raise = float(input())

portion_down_payment = 0.25 # down payment for the dream home
current_savings = 0 # savings when the home is purchased
r = 0.04 # annual rate for investments
monthly_salary = annual_salary / 12

need_to_save = portion_down_payment * total_cost
months = 0
while current_savings < need_to_save:
    current_savings += current_savings*r/12
    current_savings += portion_saved * monthly_salary
    months += 1
    if months%6 == 0:
        monthly_salary += monthly_salary * semi_annual_raise

print('Number of months:' + str(months), end = '')
