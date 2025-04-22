from flask import Flask
from flask_mysqldb import MySQL
import yaml
from flask_smorest import Api
from flask import render_template
from posts_routes import create_post_blueprint

app = Flask(__name__)

db_info = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] = db_info['mysql_host']
app.config["MYSQL_USER"] = db_info['mysql_user']
app.config["MYSQL_PASSWORD"] = db_info['mysql_password']
app.config["MYSQL_DB"] = db_info['mysql_db']

mysql = MySQL(app)

#blueprint
app.config['API_TITLE'] = 'Blog API List'
app.config['API_VERSION'] = '1.0'
app.config['OPENAPI_VERSION'] = '3.1.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'http://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)
posts_blp = create_post_blueprint(mysql)
api.register_blueprint(posts_blp)

@app.route('/blogs')
def manage_blogs():
    return render_template("posts.html")

if __name__ == "__main__":
    app.run(debug=True)
