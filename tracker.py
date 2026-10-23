import json
import os
from datetime import date


class ExpenseError(ValueError):
    """Raised when an expense entry is not valid."""


def make_expense(amount, category, note=""):
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ExpenseError("amount must be a number")
    if amount <= 0:
        raise ExpenseError("amount must be greater than zero")

    category = str(category or "").strip().lower()
    if not category:
        raise ExpenseError("category cannot be empty")

    return {
        "amount": round(amount, 2),
        "category": category,
        "note": str(note or "").strip(),
        "date": date.today().isoformat(),
    }


def total_by_category(expenses):
    result = {}
    for e in expenses:
        result[e["category"]] = round(result.get(e["category"], 0) + e["amount"], 2)
    return result


def load(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)


def save(path, expenses):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w") as f:
        json.dump(expenses, f, indent=2)
