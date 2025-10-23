-- Transactions table stores both incomes and expenses
CREATE TABLE IF NOT EXISTS transactions (
id INTEGER PRIMARY KEY AUTOINCREMENT,
amount REAL NOT NULL,
type TEXT NOT NULL CHECK(type IN ('income','expense')),
category TEXT NOT NULL,
description TEXT,
created_at TEXT NOT NULL
);