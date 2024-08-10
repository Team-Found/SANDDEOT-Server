import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('./server.db')
cur = conn.cursor()

# 데이터 조회
cur.execute('SELECT * FROM RSS')
rows = cur.fetchall()
for row in rows:
    print(row)

# 연결 종료
conn.close()