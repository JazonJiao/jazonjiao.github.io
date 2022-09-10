"""
220907: my financial health prospects
All money is denoted in thousands
"""

# starting money at the end of 2022
_401k = 6
money = 100

# assumptions on annual earning and spending
spending = 60
_401k_contrib = 20
_401k_match = 10
pretax_return = 1.03
aftertax_return = (pretax_return-1) * 0.8 + 1
tax_rate = 0.45

salary = {2023: 190,  # L3
          2024: 270,  # L4
          2025: 280,  # L4
          2026: 350,  # L5
          2027: 360,  # L5
          2028: 370,  # L5
          2029: 490   # L6
          }

print(f"2022 Year-end Asset: {money:.1f}k + {_401k:.1f}k")
for yr, earn in salary.items():
    pretax = earn - _401k_contrib
    aftertax = pretax * (1-tax_rate)
    _401k *= pretax_return
    _401k += (_401k_contrib + _401k_match) * (pretax_return / 2 + 0.5)
    money -= spending
    money *= aftertax_return
    money += earn * tax_rate * (aftertax_return / 2 + 0.5)
    print(f"{yr} Year-end Asset: {money:.1f}k + {_401k:.1f}k = {int(money+_401k)}k")














