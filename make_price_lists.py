import pandas as pd
import random

products = ["Ноутбук Lenovo", "Мышь Logitech", "Клавиатура Razer",
            "Монитор Samsung", "Наушники Sony", "Кабель USB-C",
            "Веб-камера Logitech", "Микрофон HyperX", "Коврик SteelSeries",
            "Подставка для ноутбука"]

# Старый прайс
old = pd.DataFrame({
    "Товар": products,
    "Цена": [55000, 2500, 8000, 22000, 15000, 500, 7000, 9000, 1500, 2000],
    "Артикул": [f"ART-{i:03d}" for i in range(1, 11)],
})

# Новый прайс: часть цен изменилась, пара товаров исчезла, пара новых
new_rows = []
for _, row in old.iterrows():
    if random.random() < 0.3:  # 30% цен изменилось
        new_price = int(row["Цена"] * random.uniform(0.85, 1.15))
    else:
        new_price = row["Цена"]
    new_rows.append({
        "Товар": row["Товар"],
        "Цена": new_price,
        "Артикул": row["Артикул"],
    })

# Удаляем 1 товар из нового
new_rows = new_rows[:-1]

# Добавляем 2 новых товара
new_rows.append({"Товар": "SSD Samsung 1TB", "Цена": 12000, "Артикул": "ART-011"})
new_rows.append({"Товар": "Корпус NZXT", "Цена": 8500, "Артикул": "ART-012"})

new = pd.DataFrame(new_rows)

old.to_excel("price_old.xlsx", index=False)
new.to_excel("price_new.xlsx", index=False)
print(f"Создано: price_old.xlsx ({len(old)} товаров), price_new.xlsx ({len(new)} товаров)")