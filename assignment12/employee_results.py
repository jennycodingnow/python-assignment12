# Task 1: Plotting with Pandas

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to a new SQLite database
with sqlite3.connect("../db/lesson.db") as conn: 
    print("Database connected successfully.")

    sql_query = """
    SELECT last_name, SUM(price * quantity) 
    AS revenue FROM employees e 
    JOIN orders o ON e.employee_id = o.employee_id 
    JOIN line_items l ON o.order_id = l.order_id 
    JOIN products p ON l.product_id = p.product_id 
    GROUP BY e.employee_id;
    """

    df = pd.read_sql_query(sql_query, conn)
    df = df.sort_values(by="revenue", ascending=True)
    print(df.head())


    df.plot(
        kind="bar", 
        x="last_name", 
        y="revenue", 
        title="Revenue by Employee",
        color="skyblue", 
        edgecolor="black",
        legend=False,
        figsize=(10, 6)
    )

    plt.title("Revenue by Employee", fontsize=14, fontweight="bold")
    plt.xlabel("Employee Last Name", fontsize=12, fontweight="bold")
    plt.ylabel("Revenue ($)", fontsize=12, fontweight="bold")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis="y", linestyle="--", linewidth=0.5)

    plt.tight_layout() #auto spacing
    plt.show()


conn.close()
print("Database closed successfully.")
