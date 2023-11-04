import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("stats_2023_11.csv")

df = df[df["country_name"].str.isnumeric() == False]
df.loc[df["country_name"] == "Other", "country_name"] = "rest"
df = df.dropna()
df = df.reset_index(drop=True)

# Plotting total articles by country
plt.figure(figsize=(12, 6))
plt.bar(df["country_name"], df["total_articles"])
plt.xlabel("Country")
plt.ylabel("Total Articles")
plt.title("Total Articles by Country")
plt.xticks(rotation=90)
plt.show()

# Plotting average comments by country
plt.figure(figsize=(12, 6))
plt.bar(df["country_name"], df["avg_comments"])
plt.xlabel("Country")
plt.ylabel("Average Comments")
plt.title("Average Comments by Country")
plt.xticks(rotation=90)
plt.show()

# Plotting maximum comments by country
plt.figure(figsize=(12, 6))
plt.bar(df["country_name"], df["max_comments"])
plt.xlabel("Country")
plt.ylabel("Maximum Comments")
plt.title("Maximum Comments by Country")
plt.xticks(rotation=90)
plt.show()

# Summary statistics
summary_stats = df.describe()

print("Summary Statistics:")
print(summary_stats)

# Top 5 countries with the most total articles
top_5_countries = df.nlargest(5, "total_articles")
print("\nTop 5 Countries with the Most Total Articles:")
print(top_5_countries[["country_name", "total_articles"]])

# Country with the highest average comments
highest_avg_comments = df[df["avg_comments"] == df["avg_comments"].max()]
print("\nCountry with the Highest Average Comments:")
print(highest_avg_comments[["country_name", "avg_comments"]])

# Country with the highest maximum comments
highest_max_comments = df[df["max_comments"] == df["max_comments"].max()]
print("\nCountry with the Highest Maximum Comments:")
print(highest_max_comments[["country_name", "max_comments"]])
