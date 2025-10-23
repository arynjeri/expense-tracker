import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
import random
import json
from flask import jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY", "dev-secret-key")

PORT = int(os.environ.get("PORT",5000))

FILE_NAME = "expenses.xlsx"


# ✅ Seed demo data
def seed_demo_data():
    """Generate a month of demo data for testing"""
    start_date = datetime(2025, 9, 1)
    days = [start_date + timedelta(days=i) for i in range(30)]

    income_sources = ["Salary", "Freelance", "Gift", "Investment", "Bonus"]
    expense_categories = ["Food", "Transport", "Rent", "Shopping", "Entertainment", "Bills"]

    income_data = []
    expense_data = []

    for day in days:
        for _ in range(random.randint(1, 3)):
            income_data.append({
                "Amount": round(random.uniform(2000, 8000), 2),
                "Source": random.choice(income_sources),
                "Date": day.strftime("%Y-%m-%d")
            })

        for _ in range(random.randint(2, 5)):
            expense_data.append({
                "Amount": round(random.uniform(500, 5000), 2),
                "Category": random.choice(expense_categories),
                "Date": day.strftime("%Y-%m-%d")
            })

    df_income = pd.DataFrame(income_data)
    df_expense = pd.DataFrame(expense_data)

    with pd.ExcelWriter(FILE_NAME, engine="openpyxl") as writer:
        df_income.to_excel(writer, sheet_name="Income", index=False)
        df_expense.to_excel(writer, sheet_name="Expense", index=False)

    print("✅ Demo data seeded successfully!")


# ✅ Initialize Excel file if not found or empty
def init_excel():
    if not os.path.exists(FILE_NAME):
        seed_demo_data()
    else:
        try:
            df_income = pd.read_excel(FILE_NAME, sheet_name="Income")
            df_expense = pd.read_excel(FILE_NAME, sheet_name="Expense")
            if df_income.empty and df_expense.empty:
                seed_demo_data()
        except Exception:
            seed_demo_data()


init_excel()


# ✅ Dashboard
@app.route("/")
def dashboard():
    df_income = pd.read_excel(FILE_NAME, sheet_name="Income")
    df_expense = pd.read_excel(FILE_NAME, sheet_name="Expense")

    df_income["Amount"] = df_income["Amount"].round(2)
    df_expense["Amount"] = df_expense["Amount"].round(2)

    total_income = round(df_income["Amount"].sum(), 2)
    total_expense = round(df_expense["Amount"].sum(), 2)
    balance = round(total_income - total_expense, 2)

    income_data = df_income.groupby("Date")["Amount"].sum().reset_index()
    expense_data = df_expense.groupby("Date")["Amount"].sum().reset_index()

    return render_template(
        "dashboard.html",
        total_income=f"{total_income:.2f}",
        total_expense=f"{total_expense:.2f}",
        balance=f"{balance:.2f}",
        income_data=income_data.to_dict(orient="records"),
        expense_data=expense_data.to_dict(orient="records"),
        has_data=not df_income.empty or not df_expense.empty
    )

# ✅ Income Page (Charts + Table)
@app.route("/income", methods=["GET", "POST"])
def income():
    if request.method == "POST":
        amount = round(float(request.form["amount"]), 2)
        source = request.form["source"]
        date = request.form["date"]

        df_income = pd.read_excel(FILE_NAME, sheet_name="Income")
        new_row = pd.DataFrame({"Amount": [amount], "Source": [source], "Date": [date]})
        df_income = pd.concat([df_income, new_row], ignore_index=True)

        with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df_income.to_excel(writer, sheet_name="Income", index=False)

        flash("Income added successfully!", "success")
        return redirect(url_for("income"))

    df_income = pd.read_excel(FILE_NAME, sheet_name="Income")
    df_income["Amount"] = df_income["Amount"].round(2)

    income_line = df_income.groupby("Date")["Amount"].sum().reset_index()
    income_bar = df_income.groupby("Source")["Amount"].sum().reset_index()

    # show only first 5 records initially
    limit = 5
    data_to_show = df_income.head(limit)

    return render_template(
        "income.html",
        data={"line": income_line.to_dict(orient="records"),
              "bar": income_bar.to_dict(orient="records")},
        df_income=data_to_show,
        total=len(df_income),
        limit=limit
    )

# ✅ Expense Page (Charts + Table)
@app.route("/expense", methods=["GET", "POST"])
def expense():
    if request.method == "POST":
        amount = round(float(request.form["amount"]), 2)
        category = request.form["category"]
        date = request.form["date"]

        df_expense = pd.read_excel(FILE_NAME, sheet_name="Expense")
        new_row = pd.DataFrame({"Amount": [amount], "Category": [category], "Date": [date]})
        df_expense = pd.concat([df_expense, new_row], ignore_index=True)

        with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df_expense.to_excel(writer, sheet_name="Expense", index=False)

        flash("Expense added successfully!", "success")
        return redirect(url_for("expense"))

    df_expense = pd.read_excel(FILE_NAME, sheet_name="Expense")
    df_expense["Amount"] = df_expense["Amount"].round(2)

    expense_line = df_expense.groupby("Date")["Amount"].sum().reset_index()
    expense_bar = df_expense.groupby("Category")["Amount"].sum().reset_index()

    limit = 5
    data_to_show = df_expense.head(limit)

    return render_template(
        "expense.html",
        data={"line": expense_line.to_dict(orient="records"),
              "bar": expense_bar.to_dict(orient="records")},
        df_expense=data_to_show,
        total=len(df_expense),
        limit=limit
    )

# ✅ Route to handle "Load More" requests dynamically
@app.route("/load_more")
def load_more():
    record_type = request.args.get("type")
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 5))

    if record_type == "income":
        df = pd.read_excel(FILE_NAME, sheet_name="Income")
        df = df.round(2)
        rows = df.iloc[offset:offset+limit].to_dict(orient="records")
        return jsonify(rows)

    elif record_type == "expense":
        df = pd.read_excel(FILE_NAME, sheet_name="Expense")
        df = df.round(2)
        rows = df.iloc[offset:offset+limit].to_dict(orient="records")
        return jsonify(rows)

    return jsonify([])


# ✅ Delete Income Entry
@app.route("/delete_income/<int:index>", methods=["POST"])
def delete_income(index):
    df_income = pd.read_excel(FILE_NAME, sheet_name="Income")
    if 0 <= index < len(df_income):
        df_income = df_income.drop(index).reset_index(drop=True)
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df_income.to_excel(writer, sheet_name="Income", index=False)
        flash("Income deleted successfully!", "success")
    else:
        flash("Invalid income entry selected.", "danger")
    return redirect(url_for("income"))


# ✅ Delete Expense Entry
@app.route("/delete_expense/<int:index>", methods=["POST"])
def delete_expense(index):
    df_expense = pd.read_excel(FILE_NAME, sheet_name="Expense")
    if 0 <= index < len(df_expense):
        df_expense = df_expense.drop(index).reset_index(drop=True)
        with pd.ExcelWriter(FILE_NAME, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df_expense.to_excel(writer, sheet_name="Expense", index=False)
        flash("Expense deleted successfully!", "success")
    else:
        flash("Invalid expense entry selected.", "danger")
    return redirect(url_for("expense"))


# ✅ Download both sheets
@app.route("/download")
def download():
    if not os.path.exists(FILE_NAME):
        flash("No data to download!", "warning")
        return redirect(url_for("dashboard"))

    df_income = pd.read_excel(FILE_NAME, sheet_name="Income")
    df_expense = pd.read_excel(FILE_NAME, sheet_name="Expense")

    if df_income.empty and df_expense.empty:
        flash("No data to download!", "warning")
        return redirect(url_for("dashboard"))

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_income.to_excel(writer, sheet_name="Income", index=False)
        df_expense.to_excel(writer, sheet_name="Expense", index=False)
    output.seek(0)

    filename = f"Income_Expense_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(output, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=PORT)

