import pandas as pd

old = pd.read_excel("price_old.xlsx")
new = pd.read_excel("price_new.xlsx")

# 1. Объединяем по артикулу (полное внешнее соединение)
merged = old.merge(new, on="Артикул", how="outer", suffixes=("_старая", "_новая"))

# 2. Определяем, что изменилось
def status(row):
    if pd.isna(row["Цена_старая"]):
        return "Новый товар"
    if pd.isna(row["Цена_новая"]):
        return "Удалён"
    if row["Цена_старая"] == row["Цена_новая"]:
        return "Без изменений"
    if row["Цена_новая"] > row["Цена_старая"]:
        return "Подорожал"
    return "Подешевел"

merged["Статус"] = merged.apply(status, axis=1)

# 3. Считаем разницу
merged["Разница"] = merged["Цена_новая"] - merged["Цена_старая"]
merged["Разница_%"] = (merged["Разница"] / merged["Цена_старая"] * 100).round(1)

# 4. Выбираем финальный вид
# Для удалённых/новых — берём название из той колонки, где оно есть
merged["Товар"] = merged["Товар_старая"].fillna(merged["Товар_новая"])

result = merged[["Артикул", "Товар", "Цена_старая", "Цена_новая",
                 "Разница", "Разница_%", "Статус"]].copy()

# Сортируем: сначала изменённые, потом новые/удалённые, потом без изменений
result["_order"] = result["Статус"].map({
    "Подорожал": 1, "Подешевел": 1,
    "Новый товар": 2, "Удалён": 2,
    "Без изменений": 3,
})
result = result.sort_values(["_order", "Разница_%"], ascending=[True, False])
result = result.drop(columns=["_order"])

# 5. Сохраняем с двумя листами: всё + только изменения
with pd.ExcelWriter("price_diff.xlsx", engine="openpyxl") as writer:
    result.to_excel(writer, sheet_name="Все товары", index=False)
    changes = result[result["Статус"].isin(["Подорожал", "Подешевел", "Новый товар", "Удалён"])]
    changes.to_excel(writer, sheet_name="Изменения", index=False)

# 6. Итоговая статистика
print(f"Всего товаров в отчёте: {len(result)}")
print(f"Подорожало: {len(result[result['Статус'] == 'Подорожал'])}")
print(f"Подешевело: {len(result[result['Статус'] == 'Подешевел'])}")
print(f"Новых: {len(result[result['Статус'] == 'Новый товар'])}")
print(f"Удалено: {len(result[result['Статус'] == 'Удалён'])}")
print(f"Без изменений: {len(result[result['Статус'] == 'Без изменений'])}")
print("\nФайл: price_diff.xlsx")