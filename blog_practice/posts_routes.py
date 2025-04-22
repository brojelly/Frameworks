from flask import request, jsonify
from flask_smorest import Blueprint, abort

def create_post_blueprint(mysql):
    posts_blp = Blueprint("post", __name__, description = 'posts api', url_prefix ='/posts')

    @posts_blp.route("/", methods=['GET', 'POST'])
    def posts():
        cursor = mysql.connection.cursor()
        #게시글 조회
        if request.method == 'GET':
            sql= "SELECT * FROM posts"
            cursor.execute(sql)

            posts = cursor.fetchall()
            cursor.close()

            post_list = []

            for post in posts:
                post_list.append({
                    'id': post[0],
                    'title': post[1],
                    'content': post[2]
                })
            
            return jsonify(post_list)
        # 게시글 생성
        elif request.method == 'POST':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, message='Title or content cannot be empty')

            sql = 'INSERT INTO posts(title, content) VALUES(%s, %s)'
            cursor.execute(sql, (title, content))
            mysql.connection.commit()

            return jsonify({'msg':"successfully created post data", "title":title, "content":content}), 201
        
    @posts_blp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def post(id):
        cursor = mysql.connection.cursor()
        sql = 'SELECT * FROM posts WHERE id = {id}'
        cursor.execute(sql)
        post = cursor.fetchone()

        if request.method == 'GET':

            if not post:
                abort(404, "Not Found Post")
            return ({
                    'id': post[0],
                    'title': post[1],
                    'content': post[2]
                    })
        
        elif request.method == 'PUT':

            # data = request.json
            # title = data['title']

            title = request.json.get('title')
            content = request.json.get('content')
            
            if not title or not content:
                abort(400, "Not Found title, content.")
            
            if not post:
                abort(404, "Not Found post.")


            sql = f"UPDATE posts SET title={title}, content={content} WHERE id = {id}"
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({"msg":"Successfully update title & content."})
        
        elif request.method == 'DELETE':
            if not post:
                abort(400, "Not Found post.")

            sql = f"DELETE FROM posts WHERE id ={id}"
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({"msg":"Successfully deleted title & content."})
    
    return posts_blp
#API CRUD