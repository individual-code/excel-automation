import pandas as pd
import re

# 1. Читаем
df = pd.read_excel("clients_dirty.xlsx")
original_count = len(df)
print(f"Строк на входе: {original_count}")

# 2. Убираем пробелы по краям во всех текстовых колонках
for col in ["Имя", "Email", "Телефон", "Город"]:
    df[col] = df[col].astype(str).str.strip()

# 3. Нормализуем имена: каждое слово с заглавной
df["Имя"] = df["Имя"].str.title()

# 4. Нормализуем email: нижний регистр, без пробелов
df["Email"] = df["Email"].str.lower().str.replace(r"\s+", "", regex=True)

# 5. Телефоны: только цифры, приводим к +7XXXXXXXXXX
def normalize_phone(p):
    digits = re.sub(r"\D", "", str(p))
    if len(digits) == 11 and digits[0] == "8":
        digits = "7" + digits[1:]
    if len(digits) == 10:
        digits = "7" + digits
    if len(digits) == 11 and digits[0] == "7":
        return f"+{digits}"
    return ""

df["Телефон"] = df["Телефон"].apply(normalize_phone)

# 6. Убираем пустые контакты (нет ни email, ни телефона)
before_empty = len(df)
df = df[(df["Email"] != "") | (df["Телефон"] != "")]
print(f"Удалено пустых: {before_empty - len(df)}")

# 7. Убираем дубли
before_dedup = len(df)
df = df.drop_duplicates(subset=["Email"], keep="first")
df = df[df["Email"] != ""].drop_duplicates(subset=["Телефон"], keep="first")
print(f"Удалено дублей: {before_dedup - len(df)}")

# 8. Сохраняем чистую базу
df.to_excel("clients_clean.xlsx", index=False)
print(f"\nСтрок на выходе: {len(df)}")
print(f"Итого удалено: {original_count - len(df)}")

# 9. Отчёт
report = pd.DataFrame({
    "Метрика": ["Строк на входе", "Строк на выходе",
                "Удалено пустых", "Удалено дублей"],
    "Значение": [original_count, len(df),
                 before_empty - len(df) + 1 if before_empty == len(df) else original_count - before_empty,
                 before_dedup - len(df)],
})
report.to_excel("clean_report.xlsx", index=False)
print("Отчёт: clean_report.xlsx")