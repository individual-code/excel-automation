import pandas as pd
import random

def make_phone():
    """Генерирует случайный номер в случайном формате."""
    digits = "9" + "".join(str(random.randint(0, 9)) for _ in range(9))
    formats = [
        f"+7 {digits[:3]} {digits[3:6]}-{digits[6:8]}-{digits[8:]}",
        f"8{digits}",
        f"8 ({digits[:3]}) {digits[3:]}",
        f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}",
        f"8-{digits[:3]}-{digits[3:6]}-{digits[6:]}",
        f"+7{digits}",
    ]
    return random.choice(formats)

def make_email(name):
    """Email из имени + случайный домен."""
    translit = {"Иван": "ivan", "Мария": "maria", "Пётр": "petr", "Анна": "anna",
                "Олег": "oleg", "Елена": "elena"}
    base = translit.get(name.split()[0], "user")
    return f"{base}{random.randint(1, 99999)}@{random.choice(['mail.ru', 'gmail.com', 'yandex.ru'])}"

first_names = ["Иван", "Мария", "Пётр", "Анна", "Олег", "Елена",
               "Дмитрий", "Ольга", "Сергей", "Татьяна"]
last_names = ["Петров", "Сидорова", "Иванов", "Смирнова", "Кузнецов",
              "Попова", "Соколов", "Морозова", "Волков", "Зайцева"]

rows = []
for _ in range(5000):
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"

    # 10% шанс испортить имя пробелами или регистром
    if random.random() < 0.1:
        name = name.lower()
    elif random.random() < 0.1:
        name = " " + name + "  "

    email = make_email(name)
    # 5% шанс пустого email
    if random.random() < 0.05:
        email = ""

    phone = make_phone()
    # 5% шанс пустого телефона
    if random.random() < 0.05:
        phone = ""

    rows.append({
        "Имя": name,
        "Email": email,
        "Телефон": phone,
        "Город": random.choice(["Москва", "СПб", "Казань", "Новосибирск"]),
    })

# Искусственно добавим 200 дублей, чтобы скрипт их нашёл
for _ in range(200):
    rows.append(random.choice(rows))

df = pd.DataFrame(rows)
df.to_excel("clients_dirty.xlsx", index=False)
print(f"Создан clients_dirty.xlsx — {len(df)} строк")
print(f"Из них ~200 — дубли")