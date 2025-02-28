from datetime import datetime
import json
import argparse
import csv

EXPENSE_FILE = "expenselist.json"
CSV_FILE = "expenses.csv"

try:
    with open(EXPENSE_FILE, "r") as f:
        elist = json.load(f)
except (json.decoder.JSONDecodeError, FileNotFoundError):
    with open(EXPENSE_FILE, "w") as f:
        elist = {}
        json.dump(elist, f)

id_num = max(map(int, elist.keys()), default=-1) + 1 if elist else 0

parser = argparse.ArgumentParser(description="Expense Tracker")

parser.add_argument("act")
parser.add_argument("-d", "--description")
parser.add_argument("-a", "--amount", type=int)
parser.add_argument("-id", "--id")
parser.add_argument("-c", "--category")
parser.add_argument("-m", "--month", type=int)
parser.add_argument("-y", "--year", type=int)

cmd = parser.parse_args()

action = cmd.act


def add(desc, amt):
    if not desc or not amt:
        print("Not entered required arguments")
    else:
        elist[id_num] = {"description": desc,
                         "amount": amt,
                         "date": str(datetime.today()).split(" ")[0],
                         "category": "All" if not cmd.category else cmd.category}
        print("Expense have been added")


def update(ex_id):
    if ex_id not in elist.keys():
        print("No such ID")
    else:
        if not cmd.description and not cmd.amount:
            print("Not entered anything")
        else:
            for key in ["description", "amount"]:
                if getattr(cmd, key):
                    elist[cmd.id][key] = getattr(cmd, key)
                    elist[cmd.id]["date of update"] = str(datetime.today()).split(" ")[0]
                    print("Expense have been updated")


def delete(ex_id):
    if cmd.id not in elist.keys():
        print("No such ID")
        exit()
    del elist[ex_id]
    print("Expense have been deleted")


def exp_list():
    print(f'{"ID":<5} {"Date":<15} {"Description":<15} {"Category":<15} {"Amount"}')
    for key, val in elist.items():
        if key == "-1":
            continue
        exp_text = val['description'][:12] + "..." if len(val['description']) > 15 else val['description']
        category_text = val['category'][:12] + "..." if len(val['category']) > 15 else val['category']
        amt_text = "$" + str(val['amount'])[:7] + f" * 10^{len(str(val['amount']))-7}" if len(str(val['amount'])) > 15 else val['amount']
        print(f"{key:<5} {val['date']:<15} {exp_text:<15} {category_text:<15} {amt_text:<15}")


def list_by_category(category):
    print(f'{"ID":<5} {"Date":<15} {"Description":<15} {"Category":<15} {"Amount"}')
    for key, val in elist.items():
        if key == "-1":
            continue
        if val['category'] == category:
            exp_text = val['description'][:12] + "..." if len(val['description']) > 15 else val['description']
            category_text = val['category'][:12] + "..." if len(val['category']) > 15 else val['category']
            amt_text = "$" + str(val['amount'])[:7] + f" * 10^{len(str(val['amount'])) - 7}" if len(str(val['amount'])) > 15 else \
            val['amount']
            print(f"{key:<5} {val['date']:<15} {exp_text:<15} {category_text:<15} {amt_text:<15}")


def summary():
    sum = 0
    for key in elist.keys():
        sum += elist[key]['amount']
    print(f"Total expenses: ${sum}")


def summary_month(m, y):
    sum = 0
    if 0 < m <= 12:
        for key, val in elist.items():
            if key == "-1":
                continue
            if val["date"].split("-")[0] == str(y):
                if val["date"].split("-")[1] == f"{m:02}":
                    sum += elist[key]["amount"]
        return sum
    else:
        print("Incorrect month")


def summary_year(y):
    sum = 0
    for key, val in elist.items():
        if key == "-1":
            continue
        if val["date"].split("-")[0] == f"{y}":
            sum += elist[key]["amount"]
    print(f"Total expenses in {y}: ${sum}")


def list_categories():
    ct = []
    print(f"Categories:")
    for key, val in elist.items():
        if key == "-1":
            continue
        ct.append(val['category'])
    print(set(ct))


def budget():
    if cmd.amount is not None:
        if cmd.amount == 0:
            del elist['-1']
            print("The budget has been removed")
        elif cmd.amount > 0:
            elist['-1'] = cmd.amount
            print(f"The budget is set at {cmd.amount}")
        else:
            print("Incorrect budget")
    else:
        if "-1" not in elist.keys():
            print("The budget is not set")
        else:
            print(f"Budget is {elist['-1']}")


def show_exp(id):
    if id not in elist.keys():
        print("No such ID")
    else:
        print(f"Description: {elist[cmd.id]['description']}\n"
              f"Amount: {elist[cmd.id]['amount']}\n"
              f"Date: {elist[cmd.id]['date']}")


def export_to_csv():
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["description", "date", "category",  "amount"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(elist.values())
        print("Expense list has been exported to csv file")


def clear():
    global elist
    elist = {}
    print("Expense list cleared")


if action == "add":
    add(cmd.description, cmd.amount)

elif action == "update":
    update(cmd.id)

elif action == "delete":
    delete(cmd.id)

elif action == "list":
    if cmd.category:
        list_by_category(cmd.category)
    else:
        exp_list()

elif action == "budget":
    budget()

elif action == "allct":
    list_categories()

elif action == "showexp":
    show_exp(cmd.id)

elif action == "summary":
    if cmd.year and not cmd.month:
        summary_year(cmd.year)
    elif cmd.month and cmd.year:
        print(f"Total expenses in {datetime(cmd.year, cmd.month, 1).strftime('%B')}: ${summary_month(cmd.month, cmd.year)}")
    else:
        summary()

elif action == "csv":
    export_to_csv()

elif action == "clear":
    clear()

else:
    print("Incorrect command")

if "-1" in elist.keys():
    if summary_month(datetime.today().month, datetime.today().year) > elist["-1"]:
        print(f"! Budget exceeded by {summary_month(datetime.today().month, datetime.today().year) - elist['-1']}")
    elif summary_month(datetime.today().month, datetime.today().year) >= (elist['-1']/100) * 80:
        print(f"! {elist['-1'] - summary_month(datetime.today().month, datetime.today().year)} left before budget exceeded")

with open(EXPENSE_FILE, "w") as f:
    json.dump(elist, f, indent=4)
