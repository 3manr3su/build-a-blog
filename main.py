from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:asdf@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(120))
    

    def __init__(self, name, body):
        self.name = name
        self.body = body

        


@app.route('/newpost', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('new-post.html', title="Add a Blog Post!")
    else:
        name = request.form['name']
        body = request.form['body']
        name_error = ""
        body_error = ""

    if name == "":
        name_error = "Enter a name for your blog post"
    if "Enter blog text here" in body:
        body_error = "Enter text to add a new post"

    if body_error or name_error:
        return render_template('new-post.html', title="Add a Blog Post!", name=name, body=body, name_error=name_error, body_error=body_error)

    else:
        new_post = Blog(name, body)
        name = request.form['name']
        body = request.form['body']
        db.session.add(new_post)
        db.session.commit()
        posts = Blog.query.filter_by(name=name).first()
        return render_template('single-blog.html', posts=posts)

@app.route('/blog')
def posts():

    id_exists = request.args.get('id')
    if id_exists:
        title = request.args.get('name')
        posts = Blog.query.filter_by(id=id_exists).first() 
        return render_template('single-blog.html', title=title, posts=posts)

    else:
        posts = Blog.query.all()
        title = "My Blog Posts!"
        return render_template('blogs.html', title=title, posts=posts)




if __name__ == '__main__':
    app.run()