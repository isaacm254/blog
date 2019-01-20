from flask import Flask, render_template, request, redirect, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from dbquery import Operations
import datetime
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
import os
import pymysql
from ex_operations import *
from flask_login import UserMixin , LoginManager, current_user, login_user, logout_user

# folder of photos that uploaded
UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)
# database connection uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/drsalwablog'
# secret key for session
app.config['SECRET_KEY'] = 'asdfkngoithrgtrg'
# config upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# initializing sqlalchemy
db_ = SQLAlchemy(app)
# initializing databse operations object
db = Operations()
# init loaing manager
login = LoginManager(app)

# add user loader
@login.user_loader
def load_user(user_id):
    return admins.query.get(user_id)

# create admin table model
class admins(db_.Model, UserMixin):
    id = db_.Column(db_.Integer, primary_key=True)
    username = db_.Column(db_.String(100), unique=True)
    password = db_.Column(db_.String(100))
    created_at = db_.Column(db_.DateTime, server_default=db_.func.now())
    updated_at = db_.Column(db_.DateTime, server_onupdate=db_.func.now())

# create view for editor and article editor(which is route /editor/<the article id>)
class Editor(BaseView):
    @expose('/')
    def index(self):
        # get all classes in categories table
        rows = db.get_all_classes()
        return self.render('admin/editor.html', rows=rows, page='add')
    @expose('/<article_id>/')
    def dashboard(self, article_id):
        # get all classes in categories table
        rows = db.get_all_classes()
        # get the article to edit it
        result = db.get_article(article_id)
        if result:
            # get the article imgs from upload folder  
            article = get_imgs_from_url(result)
            return self.render('admin/editor.html', rows=rows, article=article[0], page='edit')
        else:
            return self.render('admin/editor.html', rows=rows, page='add')
        # add new article to article table
    @expose('/add-article/', methods=['POST'])
    def add_article(self):
        req_data = request.get_json()
        if req_data:
                main_img_url = save_imgs(req_data['main-img'])
                sub_imgs_urls = save_imgs(req_data['sub-imgs'])

                result = db.add_article(req_data['title'], main_img_url, req_data['article'],
                                    req_data['class'], sub_imgs_urls)
                return result
        return 'error'
    # update article in article table
    @expose('/update-article/', methods=['POST'])
    def update_article(self):
        req_data = request.get_json()
        if req_data:
                main_img_url = save_imgs(req_data['main-img'])
                sub_imgs_urls = save_imgs(req_data['sub-imgs'])

                result = db.update_article(req_data['article_id'], req_data['title'], main_img_url, req_data['article'], sub_imgs_urls,
                req_data['class'])
                return result

        return 'error'

    # add new class to categories table
    @expose('/add-class/', methods=['POST'])
    def add_class(self):
        req_data = request.get_json()
        if req_data:
            classe = req_data['class']
            result = db.add_class(classe)
            if result:
                return jsonify(success=True) 
            return jsonify(success=False)  
        else:
            return jsonify(success=False) 
    @expose('/delete-article/<article_id>/')
    def delete_article(self, article_id):
        # delete article in articles table by id
        result = db.delete_article(article_id)
        if result:
            return redirect('/categories/')
        else:
            print('couldn\'t')   
        
# check if the current admin is the main admin
class is_main_admin(ModelView):
    def is_accessible(self):
        return str(current_user) == '<admins 1>'
# check if the current user is an admin
class is_admin(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login/')
# admin logout 
class Logout(BaseView):
    @expose('/')
    def logout(self):
        logout_user()
        return redirect('/admin/')
# create admin route and admin view
admin = Admin(app, index_view=is_admin())
# add tap views in admin route 
admin.add_view(Editor(name='Editor'))
admin.add_view(is_main_admin(admins, db_.session))
admin.add_view(Logout(name='Logout'))
# admin login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # if the user logged in it will redirect him to /admin route
    if current_user.is_authenticated:
        return redirect('/admin/')
    if request.method == 'POST':
        # get login form data
        req_data = request.form
        if req_data['username'] and req_data['password']:
            # check if there amin with this username and password by flask-login 
            result = admins.query.filter_by(username=req_data['username'], password=req_data['password']).first()
            # set current_user
            login_user(result)
            return redirect('/admin/')
        else: 
            return jsonify(success=False, message='no data')
    return render_template('login.html')

# hash password
@app.route('/document/hash/', methods=['POST'])
def hash():
    req_data = request.get_json()
    if req_data['password']:
        return jsonify(password=hash_password(req_data['password']))
# website mainpage
@app.route('/', methods=['POST', 'GET'])
def index():
    # get the articles from article table
    if request.method == 'POST':
        # specify date to get the article from it 
        from_ = '0000-00-00 00:00:00'
        result = db.get_articles_for_main(from_)
        rows = get_imgs_from_url(result)
        return jsonify(success=True, message=rows, page='index')
    # get most readed articles 
    result = db.get_most_readed()
    most_readed_rows = get_imgs_from_url(result)
    return render_template('index.html', most_readed_rows=most_readed_rows)
# categories route to explore the articles
@app.route('/categories/', methods=['POST', 'GET'])
def categories():
    # get articles
    if request.method == 'POST':
        from_ = request.get_json()
        if from_['article_date'] == '' or from_['id'] == '':
            # if article date is empty or article id is empty
            from_['article_date'] = '0000-00-00 00:00:00'
            from_['id'] = 0
        # get articles from article table after the last article date and id
        result = db.get_articles(from_['article_date'], from_['id'])
        # get article imgs
        rows = get_imgs_from_url(result)
        return jsonify(success=True, message=rows, page='articles')
    # get most readed articles
    most_readed = db.get_most_readed()
    # get article imgs
    most_readed_rows = get_imgs_from_url(most_readed)
    # get the newest articles
    newest = db.get_newest()
    # get articles imgs
    newest_rows = get_imgs_from_url(newest)
    # get all classes in categories table
    categs = db.get_all_classes()
    return render_template('categories.html', most_readed_rows=most_readed_rows, newest_rows=newest_rows, categs=categs)
# get specific article from articles table to show it with its id number it works like the above function
@app.route('/categories/<page_num>/', methods=['POST', 'GET'])
def categories_num(page_num):
    if request.method == 'POST':
        result = db.get_article(page_num)
        if result:
            rows = get_imgs_from_url(result)
            return jsonify(success=True, message=rows, page='article')
        else:
            return jsonify(success=True, message='redirect', page='article')
    most_readed = db.get_most_readed()
    # print(most_readed)
    most_readed_rows = get_imgs_from_url(most_readed)
    newest = db.get_newest()
    newest_rows = get_imgs_from_url(newest)
    categs = db.get_all_classes()
    return render_template('article.html', most_readed_rows=most_readed_rows, newest_rows=newest_rows, categs=categs)
# search for specific article by name and content
@app.route('/search/', methods=['POST'])
def search():
    if request.method == 'POST':
        req_data = request.get_json()
        if req_data:
            result = db.search(req_data['query'])
            rows = get_imgs_from_url(result)
            return jsonify(success=True, message=rows, page='search')
# increase article reads by 1 by its id
@app.route('/add-reads/', methods=['GET', 'POST'])
def add_reads():
    req_data = request.get_json()
    if req_data:
        result = db.add_read(req_data['article_id'])
        if result:
            return jsonify(success=True, message='done')
        else:
            return jsonify(success=False, message='couldn\'t insert it')
    else:
        return jsonify(success=True, message='no data')
# get most readed articles
@app.route('/most-readed/', methods=['POST', 'GET'])
def most_readed():
    result = db.get_most_readed()
    rows = get_imgs_from_url(result)
    return jsonify(success=True, message=rows)
# about dr.salwa
@app.route('/about/')
def about():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="82")
