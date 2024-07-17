import sqlite3

# 连接到SQLite数据库（如果不存在，则会自动创建）
conn = sqlite3.connect(r'D:\Python\message_board\instance\messages.db')

# 创建一个游标对象
cursor = conn.cursor()

# 创建一个表
# cursor.execute('''CREATE TABLE IF NOT EXISTS users
#                 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
#
# # 插入数据
# cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 30))
# cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 25))
#
# # 提交更改
# conn.commit()

# 查询数据
cursor.execute("SELECT * FROM Message")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 关闭游标和连接
cursor.close()
conn.close()
