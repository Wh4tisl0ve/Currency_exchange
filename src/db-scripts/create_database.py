import sqlite3

conn = sqlite3.connect('../resources/currency_exchange.db')
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''CREATE TABLE IF NOT EXISTS Currencies 
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                 Code TEXT UNIQUE, 
                 FullName TEXT, 
                 Sign TEXT 
                CHECK(
                        typeof("Code") = "text" AND
                        length("Code") == 3 AND
                        "Code" == UPPER("CODE")
                ))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS ExchangeRates (
                   ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                   BaseCurrencyId INTEGER, 
                   TargetCurrencyId INTEGER,                
                   Rate DECIMAL(6,2), 
                   FOREIGN KEY(BaseCurrencyId) REFERENCES Currencies(ID),
                   FOREIGN KEY(TargetCurrencyId) REFERENCES Currencies(ID),
                   UNIQUE(BaseCurrencyId, TargetCurrencyId),
                   CHECK(
                        BaseCurrencyId != TargetCurrencyId
                )
                 )''')

# Вставка данных в таблицу
rows = [('AUD', 'Australian dollar', 'A$'),
        ('CNY', 'Yuan Renminbi', '¥'),
        ('EUR', 'Euro', '€'),
        ('JPY', 'Yen', '¥'),
        ('KZT', 'Tenge', '₸'),
        ('RUB', 'Russian Ruble', '₽'),
        ('USD', 'US Dollar', '$')
        ]
cursor.executemany("INSERT INTO Currencies (Code, FullName, Sign) VALUES (?,?,?)", rows)


rows = [(1, 2, 4.82),
        (1, 3, 0.606331),
        (1, 4, 97.48),
        (1, 5, 327.36),
        (1, 6, 62.19),
        (1, 7, 0.677479),
        (2, 1, 0.207472),
        (2, 3, 0.125797),
        (2, 4, 20.22),
        (2, 5, 67.92),
        (2, 6, 11.69),
        (2, 7, 0.140286),
        (3, 1, 1.65),
        (3, 2, 7.95),
        (3, 4, 161.27),
        (3, 5, 540.15),
        (3, 6, 102.49),
        (3, 7, 1.11),
        (4, 1, 0.010221),
        (4, 2, 0.049309),
        (4, 3, 0.006201),
        (4, 5, 3.35),
        (4, 6, 0.639544),
        (4, 7, 0.00692),
        (5, 1, 0.003052),
        (5, 2, 0.014722),
        (5, 3, 0.001851),
        (5, 4, 0.298573),
        (5, 6, 0.190096),
        (5, 7, 0.002078),
        (6, 1, 0.016081),
        (6, 2, 0.08557),
        (6, 3, 0.009757),
        (6, 4, 1.56),
        (6, 5, 5.26),
        (6, 7, 0.010593),
        (7, 1, 1.48),
        (7, 2, 7.13),
        (7, 3, 0.89963),
        (7, 4, 144.51),
        (7, 5, 481.23),
        (7, 6, 91.48)
        ]
cursor.executemany("INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?,?,?)", rows)


conn.commit()
conn.close()
