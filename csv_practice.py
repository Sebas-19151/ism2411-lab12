# Reflection
# 1. In Excel, I could add a formula for the order total, filter the rows, and
#    export the results as a CSV. Python lets me rerun those steps on another
#    file with one command. Excel makes it easy to inspect individual rows
#    and change the filter while viewing the data.
#
# 2. A store could log the time and total revenue whenever its nightly sales
#    report runs. Append mode adds each run to the end of the log, so staff
#    can look back at earlier totals and see when each report ran.

import csv
from datetime import datetime
from decimal import Decimal

# --- Exercise 1 ---
sales_path = "data/sales.csv"
cleaned_path = "data/cleaned.csv"
log_path = "data/run_log.txt"

# --- Exercise 2 ---
print("\nExercise 2: Raw rows")
with open(sales_path, "r", encoding="utf-8-sig", newline="") as sales_file:
    reader = csv.reader(sales_file)
    for row in reader:
        print(row)

# --- Exercise 3 ---
print("\nExercise 3: Header and data rows")
sales_rows = []
with open(sales_path, "r", encoding="utf-8-sig", newline="") as sales_file:
    reader = csv.reader(sales_file)
    header = next(reader)
    print(f"Header: {header}")
    for row in reader:
        if row:
            print(row)
            sales_rows.append(row)
print(f"Data rows: {len(sales_rows)}")

# --- Exercise 4 ---
print("\nExercise 4: Order totals")
orders = []
total_revenue = Decimal("0.00")
for product, price_text, quantity_text in sales_rows:
    price = Decimal(price_text)
    quantity = int(quantity_text)
    order_total = price * quantity
    total_revenue += order_total
    orders.append((product, price, quantity, order_total))
    print(f"{product}: {quantity} units x ${price:.2f} = ${order_total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")

# --- Exercise 5 ---
print("\nExercise 5: Cleaned report")
rows_written = 0
with open(cleaned_path, "w", encoding="utf-8", newline="") as cleaned_file:
    writer = csv.writer(cleaned_file)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for product, price, quantity, order_total in orders:
        if order_total > 100:
            writer.writerow([product, f"{price:.2f}", quantity, f"{order_total:.2f}"])
            rows_written += 1
print(f"Wrote {rows_written} of {len(sales_rows)} data rows to {cleaned_path}.")

# --- Exercise 6 ---
print("\nExercise 6: DictReader totals")
dict_order_totals = []
dict_revenue = Decimal("0.00")
with open(sales_path, "r", encoding="utf-8-sig", newline="") as sales_file:
    reader = csv.DictReader(sales_file)
    for row in reader:
        product = row["product"]
        price = Decimal(row["price"])
        quantity = int(row["quantity"])
        order_total = price * quantity
        dict_order_totals.append((product, order_total))
        dict_revenue += order_total
        print(f"{product}: {quantity} units x ${price:.2f} = ${order_total:.2f}")
print(f"Total revenue with DictReader: ${dict_revenue:.2f}")
print(f"Matches Exercise 4: {dict_revenue == total_revenue}")

# --- Exercise 7 ---
print("\nExercise 7: Revenue by product")
revenue_by_product = {}
for product, order_total in dict_order_totals:
    revenue_by_product[product] = revenue_by_product.get(product, 0) + order_total

for product in sorted(revenue_by_product):
    print(f"{product}: ${revenue_by_product[product]:.2f}")

# --- Exercise 8 ---
print("\nExercise 8: Run log")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_path, "a", encoding="utf-8") as log_file:
    log_file.write(f"{timestamp} | Total revenue: ${total_revenue:.2f}\n")
print(f"Added one entry to {log_path}.")
