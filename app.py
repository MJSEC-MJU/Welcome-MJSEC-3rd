from flask import (
    Flask, abort, request, render_template,
    redirect, url_for, make_response
)
from werkzeug.exceptions import HTTPException
import json

app = Flask(__name__)

# flags.json 로드
with open('flags.json', 'r', encoding='utf-8') as f:
    FLAGS = json.load(f)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    code = getattr(e, 'code', None)
    if code and 400 <= code < 500:
        return FLAGS[str(code)], code
    return e

@app.route("/")
def index():
    return "Hello, Flask!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username != 'admin' or password != 'secret':
            error = '잘못된 아이디 또는 비밀번호'
            return render_template('login.html', error=error)
        # 로그인 성공 시
        resp = make_response(redirect(url_for('mjsec')))
        # 쿠키 설정: 이름 hidden_key, 값 MJSEC_secret, 1시간 유효, HttpOnly
        resp.set_cookie('hidden_key', 'MJSEC_secret',
                        max_age=3600, httponly=True)
        return resp

    return render_template('login.html', error=error)

@app.route('/mjsec')
def mjsec():
    # 이제 쿼리가 아니라 쿠키에서 꺼내 봅니다.
    key = request.cookies.get('hidden_key', '')
    if key != 'MJSEC_secret':
        abort(403)
    return render_template('mjsec.html')

@app.route('/admin', methods=['POST'])
def admin():
    key = request.form.get('hidden_key', '')
    if key != 'MJSEC_secret':
        abort(401)
    return render_template('mjsec.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
