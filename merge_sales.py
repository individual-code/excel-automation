import pandas as pd

# 1. Читаем все файлы
files = ["sales_january.xlsx", "sales_february.xlsx", "sales_march.xlsx"]
dfs = [pd.read_excel(f) for f in files]

# 2. Объединяем в один
df = pd.concat(dfs, ignore_index=True)
print(f"Всего строк: {len(df)}")

# 3. Итоги по товарам
summary = df.groupby("Товар").agg(
    Количество=("Количество", "sum"),
    Сумма=("Сумма", "sum"),
    Средняя_цена=("Цена", "mean"),
).reset_index()

# 4. Сортируем по сумме вниз
summary = summary.sort_values("Сумма", ascending=False)

# 5. Сохраняем всё в один файл, три листа
with pd.ExcelWriter("Итог_Q1.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Все продажи", index=False)
    summary.to_excel(writer, sheet_name="Сводка по товарам", index=False)
    summary.head(10).to_excel(writer, sheet_name="Топ-10", index=False)

print("\nГотово: Итог_Q1.xlsx")
print("\nСводка:")
print(summary.to_string(index=False))