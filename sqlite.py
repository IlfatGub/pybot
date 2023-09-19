# import sqlite3 as sql

# conn  = sql.connect("my_database.db")

# with conn:
#     # conn.row_factory = sql.Row
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM Users')
#     rows = cursor.fetchall()
#     users_list = []
#     for user in rows:
#         user_dict = {
#             'id': user[0],
#             'username': user[1],
#             'email': user[2],
#             'age': user[3]
#         }
#         users_list.append(user_dict)
#     print(users_list)




# cursor = conn.cursor()

# Создаем таблицу Users
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Users (
# id INTEGER PRIMARY KEY,
# username TEXT NOT NULL,
# email TEXT NOT NULL,
# age INTEGER
# )
# ''')




# # Создаем индекс для столбца "email"
# cursor.execute('CREATE INDEX IF NOT EXISTS  idx_email ON Users (email)')

# Добавляем нового пользователя
# cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', ('newuser', 'newuser@example.com', 28))

# # Обновляем возраст пользователя "newuser"
# cursor.execute('UPDATE Users SET age = ? WHERE username = ?', (29, 'newuser'))

# # Удаляем пользователя "newuser"
# cursor.execute('DELETE FROM Users WHERE username = ?', ('newuser',))

# cursor.execute('SELECT * FROM Users')
# users = cursor.fetchall()
# print(users)
# Преобразуем результаты в список словарей
# users_list = []
# for user in users:
#   user_dict = {
#     'id': user[0],
#     'username': user[1],
#     'email': user[2],
#     'age': user[3]
#   }
#   users_list.append(user_dict)

# Выводим результаты
# for user in users_list:
#   print(user.id)
# Сохраняем изменения и закрываем соединение
# connection.commit()
# conn.close()
from datetime import datetime


data = "2023-09-18 13:31:15"
print(data[0:10])

