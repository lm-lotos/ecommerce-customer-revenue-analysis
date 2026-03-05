import pandas as pd
import statsmodels.api as sm

# читаю файл
df = pd.read_csv("project1_df.csv")

# приблизний вік з Age Group
age_map = {
    "under 18": 15,
    "18-25": 21.5,
    "25-45": 35,
    "45-60": 52.5,
    "60 and above": 65
}

df["Age"] = df["Age Group"].map(age_map)

# прибираю порожні значення
df2 = df.dropna(subset=["Age", "Gross Amount"])

# X і y
y = df2["Gross Amount"]
X = df2["Age"]
X = sm.add_constant(X)

# модель
reg = sm.OLS(y, X).fit()

print(reg.summary())

# ефект +10 років
print(reg.params["Age"] * 10)