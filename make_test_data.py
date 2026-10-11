import pandas as pd
import random

products = ["Ноутбук", "Мышь", "Клавиатура", "Монитор", "Наушники", "Кабель", "Веб-камера"]
months = [("january", 1), ("february", 2), ("march", 3)]

for name, num in months:
    rows = []
    for _ in range(50):
        rows.append({
            "Товар": random.choice(products),
            "Количество": random.randint(1, 20),
            "Цена": random.choice([500, 1500, 3000, 8000, 12000, 25000]),
            "Дата": f"2026-{num:02d}-{random.randint(1, 28):02d}",
        })
    df = pd.DataFrame(rows)
    df["Сумма"] = df["Количество"] * df["Цена"]
    df.to_excel(f"sales_{name}.xlsx", index=False)
    print(f"Создан sales_{name}.xlsx — {len(df)} строк")

print("\nГотово. Три файла в папке.")