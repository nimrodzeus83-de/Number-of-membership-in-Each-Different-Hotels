import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv(
    r"C:\Users\MySQLAdmin\Documents\Transactions.csv",
    encoding="cp1252"
    )

df.columns = (
    df.columns 
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
    .str.replace("(", "")
    .str.replace(")","")
)

for cols in df.select_dtypes(include="object"):
    df[cols] = df[cols].astype(str).str.strip()
    
df = df.replace(["", "-", " - "],pd.NA)

money_cols = [
    "price", "package_", "gross",
    "disc_amt", "sales", "dep"
]

for cols in money_cols:
    df[cols] = (
       df[cols]
       .astype(str)
       .str.replace(",", "",regex=False) 
    )
    df[cols] = pd.to_numeric(df[cols], errors="coerce")

df["customer_rating"] = pd.to_numeric(
    df["customer_rating"], 
    errors="coerce"
)

date_cols = ["arrival_date", "depature_date"]

for cols in date_cols:
    df[cols] = pd.to_datetime(
        df[cols],
        errors = "coerce",
        dayfirst=True
    )
    
for cols in date_cols:
    df[cols] = df[cols].dt.strftime("%Y-%m-%d")
    
df["membership"] = df["membership"].fillna("Unknown")

df = df.drop_duplicates()

df.to_csv("new_data.csv", index=False)

print("Data cleaned successfully")





dff = pd.read_csv("new_data.csv")
print(dff[["hotel_name","membership"]])

membership_counts = pd.crosstab(dff["hotel_name"], dff["membership"])

ax = membership_counts.plot(
    kind="bar",
    figsize=(12,8)
)

for container in ax.containers:
    ax.bar_label(container,
                 fmt="%d",
                 fontsize=8,
                 fontweight="bold",
                 color="blue", 
                 padding = 3
                 )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    
plt.legend(title="Customer's Membership Types", 
           bbox_to_anchor=(0.90,1),
           loc="upper left"
           )

plt.style.use("ggplot")

plt.style.use("bmh")

plt.xticks(rotation=0)
plt.ylim(0, 1150)

plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.title("Number of Memberships in each different hotels", 
          fontsize=10, 
          fontweight="bold", 
          pad=20
          )

plt.xlabel("Hotel Name", fontweight="bold", fontsize="14")
plt.ylabel("Number of Customers", fontweight="bold", fontsize="14")
plt.show()
