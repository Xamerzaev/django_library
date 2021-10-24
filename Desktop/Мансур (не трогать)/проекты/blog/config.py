from os.path import join, dirname, realpath
class Config():
    SECRET_KEY = 'gfsddxhgsdft325r4q32r5'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    SQLALCHEMY_TRACK_MODIFICATION = False
    UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'blog/static/images/')