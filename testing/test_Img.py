# pip install flask
from flask import Flask,send_file
app = Flask(__name__)

@app.route('/')
def index():
    return 'hello'

@app.route('/get_img')
def get_img():
    # 跟DB取得img
    filename=DB_img
    return send_file(filename, mimetype='image/gif')


if __name__ == '__main__':
    app.debug = True
    app.run()