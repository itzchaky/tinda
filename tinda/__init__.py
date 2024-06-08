from flask import Flask
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#from flask import session
#from flask_session import Session


app = Flask(__name__)

app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'

# set your own database
#db = "dbname='bank' user='postgres' host='127.0.0.1' password = 'UIS'"
db = "dbname='mvq' user='mvq' host='127.0.0.1' password = 'immvplol100'"
conn = psycopg2.connect(db)

# create cursor object
cur = conn.cursor()

cur.execute(open("tinda/tinda_schema.sql", "r").read())

conn.commit()

bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Check Configuration section for more details
#SESSION_TYPE = 'filesystem'


roles = ["ingen","employee","customer"]
print(roles)
mysession = {"id": 0, "name": "", "email": "", "description": "", "location": "", "birth" : ""}
print(mysession)

from tinda.Login.routes import Login
from tinda.Main.routes import Main
app.register_blueprint(Login)
app.register_blueprint(Main)
