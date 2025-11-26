from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Trang chủ đơn giản
@app.route('/')
def home():
    return '''
    <h1>Web Test Tấn Công WAF</h1>
    <ul>
        <li><a href="/xss?q=hello">Test XSS (Reflected)</a></li>
        <li><a href="/sqli?id=1">Test SQL Injection</a></li>
        <li><a href="/cmd?ip=127.0.0.1">Test Command Injection</a></li>
    </ul>
    '''

# 1. Lỗ hổng XSS: In thẳng input của người dùng ra màn hình mà không lọc
@app.route('/xss')
def xss():
    query = request.args.get('q', '')
    # LỖ HỔNG: Biến query được đưa thẳng vào HTML
    template = f"<h2>Kết quả tìm kiếm cho: {query}</h2>"
    return render_template_string(template)

# 2. Lỗ hổng SQL Injection (Giả lập)
@app.route('/sqli')
def sqli():
    user_id = request.args.get('id', '')
    # Giả lập câu lệnh SQL không an toàn
    fake_db_query = f"SELECT * FROM users WHERE id = {user_id}" 
    return f"Đang thực thi lệnh SQL (Giả lập): <br><code>{fake_db_query}</code>"

# 3. Lỗ hổng Command Injection: Chạy lệnh hệ thống
@app.route('/cmd')
def cmd():
    ip = request.args.get('ip', '')
    # LỖ HỔNG: Nối chuỗi để chạy lệnh ping
    cmd_str = f"ping -c 1 {ip}"
    # Lưu ý: Tôi comment dòng chạy thật để an toàn cho máy bạn, chỉ in ra lệnh thôi
    # stream = os.popen(cmd_str)
    # output = stream.read()
    return f"Hệ thống backend đang cố chạy lệnh: <br><code>{cmd_str}</code>"

if __name__ == '__main__':
    # Chạy trên tất cả các IP của máy, cổng 5000
    app.run(host='0.0.0.0', port=5000, debug=True)