import sqlalchemy as db
from flask import *

app = Flask(__name__)
engine = db.create_engine('mysql+pymysql://root:rootpassword@localhost/db1')
connection = engine.connect()
metadata = db.MetaData()
census = db.Table('blog_table', metadata, autoload=True, autoload_with=engine)


@app.route("/")
def home():
    return render_template('adduser.html')


@app.route("/GET")
def get():
    query = db.select([census])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    l1=[]
    for e in ResultSet:
        user_dict= {"name" : e[1], "email" : e[2],'blog': e[3]}
        l1.append(user_dict)

    return {"UserInfo": l1}


@app.route("/POST", methods=['POST'])
def post_user():
    name = request.form['uname']
    email = request.form['email']
    blog = request.form['blog']
    query = db.insert(census).values(username=name, email=email, blog=blog)
    ResultProxy = connection.execute(query)
    return {
            "status" : 200,
            }


@app.route("/DELETE/<string:name>")
def delete_user(name):
    query = db.delete(census)
    query = query.where(census.columns.username == name)
    results = connection.execute(query)

    return {"Status": 200
            }



if __name__=="__main__":
    app.run(debug=True)


