import os

from flask import Flask, jsonify, request

import tracker

app = Flask(__name__)


def data_file():
    # read on every call so tests and containers can change it through the environment
    return os.environ.get("DATA_FILE", "data/expenses.json")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/version")
def version():
    return jsonify(version=os.environ.get("APP_VERSION", "dev"))


@app.get("/expenses")
def list_expenses():
    return jsonify(tracker.load(data_file()))


@app.post("/expenses")
def add_expense():
    body = request.get_json(silent=True) or {}
    try:
        item = tracker.make_expense(body.get("amount"), body.get("category"), body.get("note", ""))
    except tracker.ExpenseError as err:
        return jsonify(error=str(err)), 400
    expenses = tracker.load(data_file())
    expenses.append(item)
    tracker.save(data_file(), expenses)
    return jsonify(item), 201


@app.get("/summary")
def summary():
    expenses = tracker.load(data_file())
    by_category = tracker.total_by_category(expenses)
    return jsonify(by_category=by_category, total=round(sum(by_category.values()), 2))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
