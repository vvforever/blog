import os
import os.path as op
from datetime import datetime
import random

from flask import Flask, render_template, abort, url_for, Markup
from flask_admin import Admin, form
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

# import dbcon as dc

file_path = os.path.abspath(os.path.dirname(__name__))


# Функция, которая будет генерировать имя файла из модели и загруженного файлового объекта.
def generate_name(self, obj, file_data):
    return self.namegen(file_data)


def name_gen_image(model, file_data):
    hash_name = f'{model.id/file_data}'
    return hash_name


# base_path = os.path.abspath(os.path.dirname(__name__))


# app = Flask(__name__)
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


# class StorageAdminModel(sqla.ModelView):

    # form_excluded_columns = ['image']
    #
    # def _list_thumbnail(self, context, model, name):
    #     if not model.image:
    #         return ''
    #
    #     url = url_for('static', filename=os.path.join('storage/post_img/', model.image))
    #     if model.image.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
    #         return Markup(f'<img src={url} width="100">')
    #
    # # передаю функцию _list_thumbnail в поле image_user
    # column_formatters = {
    #     'image': _list_thumbnail
    # }
    #
    # form_extra_fields = {
    #     # ImageUploadField Выполняет проверку изображений, создание эскизов, обновление и удаление изображений.
    #     "image": form.ImageUploadField('Image',
    #                                    # Абсолютный путь к каталогу, в котором будут храниться файлы
    #                                    base_path=os.path.abspath(os.path.join(file_path, 'static/storage/post_img/'))
    #                                    ,
    #                                    # Относительный путь из каталога. Будет добавляться к имени загружаемого файла.
    #                                    url_relative_path='storage/post_img/',
    #                                    namegen=name_gen_image,
    #                                    # namegen=generate_name,
    #                                    # Список разрешенных расширений. Если не указано, то будут разрешены форматы gif, jpg, jpeg, png и tiff.
    #                                    # allowed_extensions=['jpg'],
    #                                    max_size=(1200, 780, True),
    #                                    thumbnail_size=(100, 100, True),
    #                                    )
    # }
    #
    # def create_form(self, obj=None):
    #     return super(StorageAdminModel, self).create_form(obj)
    #
    # def edit_form(self, obj=None):
    #     return super(StorageAdminModel, self).edit_form(obj)


    # form_extra_fields = {
    #     'image': form.FileUploadField('image')
    # }
    #
    # def _change_path_data(self, _form):
    #     try:
    #         storage_file = _form.file.data
    #
    #         if storage_file is not None:
    #             hash1 = random.getrandbits(128)
    #             ext = storage_file.filename.split('.')[-1]
    #             path = '%s.%s' % (hash1, ext)
    #
    #             storage_file.save(
    #                 os.path.join(app.config['STORAGE'], path)
    #             )
    #
    #             _form.name.data = _form.name.data or storage_file.filename
    #             _form.path.data = path
    #             _form.type.data = ext
    #
    #             del _form.file
    #
    #     except Exception as ex:
    #         pass
    #
    #     return _form
    #
    # def edit_form(self, obj=None):
    #     return self._change_path_data(
    #         super(StorageAdminModel, self).edit_form(obj)
    #     )
    #
    # def create_form(self, obj=None):
    #     return self._change_path_data(
    #         super(StorageAdminModel, self).create_form(obj)
    #     )


#
# class MyUserAdmin(ModelView):
#     # Кнопка будет в шаблоне
#     list_template = 'templates/admin/userlist.html'
#
#     @expose('/report/<int:id>/')
#     def report(self, id):
#     # Логика тут
#         return self.render('templates/admin/userreport.html', id=id)
#
#
# class DashboardView(AdminIndexView):
#
#     @expose('/')
#     def index(self):
#         return self.render('admin/dashboard_index.html')

@app.get("/")
def index():
    return render_template("index.html")


admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Post, db.session, name="Posts"))
# admin.add_view(StorageAdminModel(Post, db.session, name="Posts"))


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
