# Expense Tracker CLI

## Description

Expense Tracker CLI is a command-line application for managing personal finances. It allows users to add, delete, update, and analyze expenses, as well as set a budget.  
Made for roadmap.sh project -- https://roadmap.sh/projects/expense-tracker

## Installation

1. Make sure you have **Python 3.x** installed.
2. Clone the repository or download the source code:
   ```sh
   git clone https://github.com/your-repo/ExpenseTracker.git
   cd ExpenseTracker
   ```
3. Install dependencies (if any):
   ```sh
   pip install -r requirements.txt
   ```

## Usage

The program accepts commands via command-line arguments.

### Adding an Expense
```sh
python main.py add -d "Description" -a AMOUNT [-c "Category"]
```
- `-d`, `--description` — expense description (**required**).
- `-a`, `--amount` — expense amount (**required**).
- `-c`, `--category` — expense category (default: "All").

### Updating an Expense
```sh
python main.py update -id ID [-d "New Description"] [-a NEW_AMOUNT]
```
- `-id`, `--id` — expense ID (**required**).
- `-d`, `--description` — new description.
- `-a`, `--amount` — new amount.

### Deleting an Expense
```sh
python main.py delete -id ID
```

### Listing All Expenses
```sh
python main.py list
```

### Listing Expenses by Category
```sh
python main.py list -c "Category"
```

### Setting or Viewing Budget
```sh
python main.py budget -a AMOUNT
```
- If `-a 0` is specified, the budget will be removed.
- If run without `-a`, the program will display the current budget.

### Displaying All Categories
```sh
python main.py allct
```

### Showing a Specific Expense
```sh
python main.py showexp -id ID
```

### Displaying Expense Summary
```sh
python main.py summary [-m MONTH] [-y YEAR]
```
- `-y` — total expenses for a year.
- `-m` and `-y` — total expenses for a specific month.
- Without arguments — total expenses overall.

### Exporting to CSV
```sh
python main.py csv
```

### Clearing Expense List
```sh
python main.py clear
```

## Usage Examples
```sh
python main.py add -d "Coffee" -a 300 -c "Food"
python main.py list
python main.py summary -m 2 -y 2025
python main.py budget -a 10000
python main.py csv
```

## Data Storage Format

All data is stored in the `expenselist.json` file in the following format:
```json
{
    "0": {
        "description": "Coffee",
        "amount": 300,
        "date": "2025-02-28",
        "category": "Food"
    }
}
```

## License

This project is distributed under the **MIT** license.

