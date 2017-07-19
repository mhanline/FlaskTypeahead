from flask import Flask, Response, render_template, request
import json
from wtforms import TextField, Form
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'readentries'
app.config['MYSQL_PASSWORD'] = 'G00gl3ro'
app.config['MYSQL_DB'] = 'PRODUCTS'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_UNIX_SOCKET'] = '/cloudsql/hopeful-20630:us-west1:typeahead-pri'

mysql = MySQL(app)

class SearchForm(Form):
    autocomp = TextField('Insert City', id='city_autocomplete')


@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    searchquery = request.args.get('q')
    cur = mysql.connection.cursor()
    query = "select DISTINCT productname from entries where productname LIKE '%%%s%%'"  % searchquery
    result = cur.execute(query)
    productlist = []
    for row in cur.fetchall() : 
        productlist.append(row[0])
    return Response(json.dumps(productlist), mimetype='application/json')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    return render_template("index.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
