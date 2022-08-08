from datetime import datetime


from flask import Flask, render_template, abort, url_for, Markup
from flask_admin import Admin, form

from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__, static_url_path="/static")
app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
app.config["SECRET_KEY"] = "anykey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/blog.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['STORAGE'] = "static/storage/post_img"
db = SQLAlchemy(app)


class Post(db.Model):
    # __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(), nullable=False)
    image = db.Column(db.String())
    create_date = db.Column(db.DateTime(), default=datetime.now)
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}," \
               f" create_date={self.create_date})>"




@app.get("/")
def index():
    return render_template("index.html")


admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Post, db.session, name="Posts"))



@app.route("/posts")
def posts():
    posts_qry = db.session.query(Post).all()
    return render_template("blog.html", posts=posts_qry)


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    posts_qry = db.session.query(Post).all()
    post = next(filter(lambda p: p.id == post_id, posts_qry), None)
    if post is None:
        abort(404)
    return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
