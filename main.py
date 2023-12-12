from flask import Flask, request, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect('attendance.db', check_same_thread=False)
c = conn.cursor()


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
          
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            
            c.execute('INSERT INTO attendance VALUES (?, ?, ?)', (request.form['name'], now, request.form['type']))

            
            conn.commit()

            return f'{request.form["name"]} {request.form["type"]} at {now}'
        elif 'delete' in request.form:
            
            c.execute('DELETE FROM attendance WHERE name = ?', (request.form['name'],))

            
            conn.commit()

            return f'{request.form["name"]} data deleted.'
    else:
        
        c.execute('SELECT * FROM attendance')
        data = c.fetchall()

        return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
