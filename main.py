from flask import Flask, request, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)

# データベースに接続
conn = sqlite3.connect('attendance.db', check_same_thread=False)
c = conn.cursor()

# 勤怠テーブルを作成（すでに存在する場合は何もしない）
c.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        name TEXT,
        time TEXT,
        type TEXT
    )
''')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'submit' in request.form:
            # 現在の日時を取得
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 勤怠データをデータベースに保存
            c.execute('INSERT INTO attendance VALUES (?, ?, ?)', (request.form['name'], now, request.form['type']))

            # 変更をコミット
            conn.commit()

            return f'{request.form["name"]} {request.form["type"]} at {now}'
        elif 'delete' in request.form:
            # 勤怠データをデータベースから削除
            c.execute('DELETE FROM attendance WHERE name = ?', (request.form['name'],))

            # 変更をコミット
            conn.commit()

            return f'{request.form["name"]} data deleted.'
    else:
        # 勤怠データをデータベースから取得
        c.execute('SELECT * FROM attendance')
        data = c.fetchall()

        return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
