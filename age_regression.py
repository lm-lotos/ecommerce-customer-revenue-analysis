import sys
import pandas as pd

# Спробуємо statsmodels; якщо його нема — дам інструкцію нижче
try:
    import statsmodels.api as sm
except ImportError:
    print("❌ Не знайдено бібліотеку statsmodels.")
    print("✅ Встанови так: pip install statsmodels")
    sys.exit(1)


print("\n" + "="*60)
print("БЛОК 1. Завантаження даних")
print("="*60)

CSV_PATH = "project1_df.csv"  # якщо файл в іншій папці — вкажи шлях

df = pd.read_csv(CSV_PATH)
print("✅ Файл завантажено.")
print("Розмір:", df.shape)
print("Перші 3 рядки:")
print(df.head(3))

# Перевірка колонок
required_cols = ["Age Group", "Gross Amount"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    print("\n❌ Немає потрібних колонок:", missing)
    print("✅ Є такі колонки:", list(df.columns))
    sys.exit(1)


print("\n" + "="*60)
print("БЛОК 2. Підготовка змінних (Age Group → Age)")
print("="*60)

# Мапа груп у приблизний вік (midpoint). Це наближення — чесно пишемо в висновку.
age_map = {
    "under 18": 15,
    "18-25": 21.5,
    "25-45": 35,
    "45-60": 52.5,
    "60 and above": 65
}

df["Age"] = df["Age Group"].map(age_map)

# Подивимось, чи всі групи замапились
unmapped = df.loc[df["Age"].isna(), "Age Group"].dropna().unique()
if len(unmapped) > 0:
    print("⚠️ Увага: є вікові групи, яких нема в age_map:", unmapped)
    print("✅ Додай їх у age_map (якщо це просто інші назви).")

data = df[["Age", "Gross Amount"]].dropna()

print("✅ Після очищення (без пропусків) рядків:", len(data))
if len(data) < 30:
    print("⚠️ Дуже мало даних для регресії — результат може бути нестабільний.")


print("\n" + "="*60)
print("БЛОК 3. Лінійна регресія: Gross Amount ~ Age")
print("="*60)

X = sm.add_constant(data["Age"])      # додаємо константу (intercept)
y = data["Gross Amount"]

model = sm.OLS(y, X).fit()

print(model.summary())


print("\n" + "="*60)
print("БЛОК 4. Інтерпретація коефіцієнта")
print("="*60)

coef = float(model.params["Age"])
effect_10y = coef * 10
r2 = float(model.rsquared)
pval = float(model.pvalues["Age"])

print(f"Коефіцієнт (Age): {coef:.4f}")
print(f"Зміна при +10 роках: {effect_10y:.2f}")
print(f"R²: {r2:.6f}")
print(f"p-value (Age): {pval:.4f}")

# Простий висновок
if r2 < 0.05:
    strength = "зв'язок слабкий (Age майже не пояснює витрати)"
elif r2 < 0.2:
    strength = "зв'язок помірний"
else:
    strength = "зв'язок відносно сильний"

sig = "статистично значущий" if pval < 0.05 else "статистично НЕзначущий"

print("\nВисновок:")
print(f"- При збільшенні віку на 10 років сума покупки змінюється приблизно на {effect_10y:.2f}.")
print(f"- {strength}.")
print(f"- Коефіцієнт {sig} (p-value={pval:.4f}).")
print("\nПримітка:")
print("- Age взято як наближення з Age Group (midpoint), тому інтерпретація приблизна.")