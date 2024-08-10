import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('/Users/asdf/Documents/Project_Unit/sanddeot/SANDDEOT-Server/db/server.db')
db = conn.cursor()

# 데이터 조회
# cur.execute('SELECT * FROM RSS')
# rows = cur.fetchall()

# for row in rows:
#     print(row)

# # 연결 종료
# conn.close()
