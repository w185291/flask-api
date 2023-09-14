from flask import Flask, escape, jsonify, make_response, redirect, url_for, request, session
from flask import render_template, Markup
from werkzeug.utils import secure_filename
import os

# flask run --host=0.0.0.0 --debugger --reload
app = Flask(__name__)

app.secret_key = 'XeToKAyI1ar8kuTemOC116d6fO4ir1'


@app.route('/', methods=['GET'])
@app.route('/index/<name>', methods=['GET'])
def index(name=None):
    name = Markup(name)
    return render_template('page/index.html', name=name)


@app.route('/user/<string:username>')
def show_user_profile(username):
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    del user['password']
    user['data'] = ["aaa", "ddd", "cccc"]
    # return {
    #     "username": user['username'],
    #     "email": user['email']
    # }
    return jsonify(user)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'Subpath %s' % escape(subpath)


@app.route('/login', methods=['GET', 'POST'])
# 順便測試收 post
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        if email != '' and password != '':
            session['user'] = {
                'email': email,
                'password': password,
                'username': "roger"
            }

        return redirect(url_for('show_user_profile', username="roger"))
    else:
        return render_template('page/login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    savePath = 'storage'+os.sep+'upload'+os.sep
    if not os.path.exists:
        os.mkdir(savePath)
    if request.method == 'POST':
        uploadFile = request.files['file']
        uploadFile.save(savePath+secure_filename(uploadFile.filename))

    return render_template('page/upload.html')


@app.context_processor
# 装饰器 可共享數據
def menu_items():
    menu_data = [
        {'url': url_for('index'), 'label': 'home'},
        {'url': url_for('login'), 'label': 'login'},
    ]
    if 'user' in session:
        menu_data.append({'url': url_for(
            'show_user_profile', username=session['user']['username']), 'label': 'user info'})
        menu_data.append({'url': url_for('logout'), 'label': 'logout'})

    return dict(menu=menu_data)


@app.errorhandler(404)
# 404統一處理
def pageNotFound(error):
    # return render_template('error/404.html'), 404
    resp = make_response(render_template('error/404.html'), 404)
    resp.headers['X-Test'] = 'my auth'
    return resp


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('index'))


# 使用url for 類似laravle route 自動取得 url
with app.test_request_context():
    print(url_for('index'))
    print(url_for('show_user_profile', username="roger"))


# 榜定測試 request post 測試
with app.test_request_context('/login', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/login'
    assert request.method == 'POST'

if __name__ == '__main__':
    # port 番号を使用するプロセスの pid を取得する。
    # $ lsof -i :5000
    # 指定された PID のアプリケーションを終了します。
    # $ kill [pid]
    app.run(host='0.0.0.0', debug=True, port=5000,
            threaded=True, use_reloader=True)
