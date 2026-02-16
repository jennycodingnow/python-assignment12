import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.data as pldata


with sqlite3.connect("../db/lesson.db") as conn: 
    print("Database connected successfully.")

# Task 2: A Line Plot with Pandas
    sql_query = """
    SELECT o.order_id, SUM(p.price * l.quantity) 
    AS total_price FROM orders o
    JOIN line_items l ON o.order_id = l.order_id
    JOIN products p ON l.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id;

    """
    df = pd.read_sql_query(sql_query, conn)
    print("Data retrieved successfully.")
    print(df.head())


    def cumulative(row):
        totals_above = df['total_price'][0:row.name+1]
        return totals_above.sum()

    df['cumulative'] = df.apply(cumulative, axis=1)   
    df['cumulative'] = df['total_price'].cumsum()

    df.plot(
        kind="line", 
        x="order_id", 
        y="cumulative", 
        title="Cumulative Revenue vs Order ID",
        color="green",
        marker="o",
        linestyle="-",
        markersize=4,
        legend=False,
        linewidth=0.5,
        figsize=(10, 6)
    )

    plt.title("Cumulative Revenue vs Order ID", fontsize=14, fontweight="bold")
    plt.xlabel("Order ID", fontsize=12, fontweight="bold")
    plt.ylabel("Cumulative Revenue ($)", fontsize=12, fontweight="bold")
    plt.grid(axis="y", linestyle="--", linewidth=0.5)

    plt.tight_layout() #auto spacing
    plt.show()

conn.close()
print("Database closed successfully.")


# Task 3: Interactive Visualizations with Plotly
df = pldata.wind(return_type="pandas")
print("Plotly data loaded successfully.")
print("First ten lines Plotly wind dataset:")
print(df.head(10))
print("Last ten lines of Plotly wind dataset:")
print(df.tail(10))

df["strength"] = df["strength"].str.replace(r'[^\d.]', '', regex=True).astype(float)

fig = px.scatter(df, x="strength", y="frequency", color="direction", title="Wind Data, Strength vs. Frequency", hover_data=["frequency"])
fig.write_html("wind.html", auto_open=True)
