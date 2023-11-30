from flask import Flask, render_template
import pandas as pd
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "jail"


mysql = MySQL(app)

def runstatement(statement):
    cursor = mysql.connection.cursor()
    cursor.execute(statement)
    results = cursor.fetchall()
    mysql.connection.commit()
    #convert into a panda dataframe
    df = ""
    if (cursor.description):
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=column_names)
    cursor.close()
    return df

@app.route('/')
def index():
    example = runstatement("SELECT * FROM officers")
    #print(example)
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)