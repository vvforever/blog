"""
The module in which they are implemented
    pages for post administration (creation, editing, deletion)
    post list page
    post details page
"""

from datetime import datetime

from flask import Flask, render_template, abort, url_for, Markup
from flask_admin import Admin, form

from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__, static_url_path="/static")
app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
app.config["SECRET_KEY"] = "anykey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/blog.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['STORAGE'] = "static/storage/post_img"
db = SQLAlchemy(app)


class Post(db.Model):
    """
        A class of Post

        ORM class of db

        Attributes
        -------
         id : Integer
            id of record
        title : String(100)
            title of post
        content : String
            content of post
        image : String
            the path to the saved image
        create_date : DateTime
            date and time of post creation
        is_active : Boolean
            a sign of active post

        Methods
        -------
        __repr__(self)
            Representative of post record

        """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(), nullable=False)
    image = db.Column(db.String())
    create_date = db.Column(db.DateTime(), default=datetime.now)
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}," \
               f" create_date={self.create_date})>"


file_path = os.path.abspath(os.path.dirname(__name__))


def name_gen_image(model, file_data):
    """Generate name of image from save to db

       Parameters
       ----------
       model :
           the model object
       file_data :
           upload file data

       Returns
       -------
       hash_name
           a name of file
       """

    hash_name = f'{model.title}/{file_data.filename}'
    return hash_name


class PostView(ModelView):
    """
        A class of Post View

        Methods
        -------
        _list_thumbnail(view, context, model, name)
            Return tumbnail url

        create_form(self, obj)
            Return admin create form

        edit_form(self, obj):
            Return admin edit form
        """
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = True

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        url = url_for('static', filename=os.path.join('storage/', model.image))
        if model.image.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
            return Markup(f'<img src={url} width="100">')

    column_formatters = {
        'image': _list_thumbnail
    }

    form_extra_fields = {

        "image": form.ImageUploadField('',

                                        base_path=
                                        os.path.join(file_path, 'static/storage'),
                                        url_relative_path='storage',
                                        namegen=name_gen_image,
                                        max_size=(1200, 780, True),
                                        thumbnail_size=(100, 100, True),

                                        )}

    def create_form(self, obj=None):
        return super(PostView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(PostView, self).edit_form(obj)


admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(PostView(Post, db.session, name="Posts"))


@app.get("/")
def index():
    """Index page renderer

        Returns
        -------
        render template
            render template of index.html
        """
    return render_template("index.html")


@app.route("/posts")
def posts():
    """Posts page renderer


            Returns
            -------
            render template
                render template of blog.html
            """
    posts_qry = db.session.query(Post).all()
    return render_template("blog.html", posts=posts_qry)


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    """Post page renderer

            Parameters
            ----------
            post_id : int
                The id of record in post db

            Returns
            -------
            render template
                render template of post.html
            """
    posts_qry = db.session.query(Post).all()
    image_qry = db.session.query(Post.image).filter(Post.id == post_id).all()
    image_name = str(image_qry[0])
    image_file = url_for('static', filename='storage/' + image_name)
    post = next(filter(lambda p: p.id == post_id, posts_qry), None)
    if post is None:
        abort(404)
    return render_template("post.html", post=post, image_url=image_file)


if __name__ == "__main__":
    app.run(debug=True)
