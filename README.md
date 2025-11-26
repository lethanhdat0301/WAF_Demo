# 🛡️ CasWAF Security Lab - Web Application Firewall Demo

Dự án này là một môi trường Lab giả lập để thực hành tấn công và phòng thủ Web (Web Security). Hệ thống sử dụng **CasWAF** (dựa trên ModSecurity/Casbin) làm Gateway bảo vệ cho một ứng dụng **Python Flask** chứa nhiều lỗ hổng bảo mật nghiêm trọng.

## 🏗️ Kiến trúc Hệ thống

Dữ liệu di chuyển theo luồng sau:
`User (Browser)` ➡️ `CasWAF (Port 80)` ➡️ `Reverse Proxy` ➡️ `Vulnerable App (Port 5000)`

* **WAF Node:** Chạy trên Docker, đóng vai trò Reverse Proxy và Firewall kiểm soát traffic.
* **Upstream (Backend):** Một Web Server Python đơn giản mô phỏng các lỗi bảo mật thường gặp (XSS, SQLi, Command Injection).

## 📂 Cấu trúc Dự án

```text
caswaf-security-lab/
├── caswaf/                 # Mã nguồn và cấu hình Docker của CasWAF
│   ├── docker-compose.yml  # File cấu hình Container (Port 80 & 17000)
│   └── ...
├── vulnerable-app/         # Ứng dụng Web Python chứa lỗ hổng
│   ├── app.py              # Code backend (Flask)
│   └── requirements.txt    # Thư viện cần thiết
├── screenshots/            # Ảnh chụp màn hình Demo (Evidence)
└── README.md               # Tài liệu hướng dẫn
```

🚀 Hướng dẫn Cài đặt
1. Yêu cầu (Prerequisites)
Docker & Docker Compose

Python 3.x

Kali Linux (Khuyên dùng) hoặc Ubuntu.

2. Khởi động WAF (CasWAF)
Bash

cd caswaf
# Khởi động container WAF và Database
sudo docker-compose up -d
CasWAF Dashboard sẽ chạy tại: http://localhost:17000 CasWAF Gateway sẽ lắng nghe tại: http://localhost:80

3. Khởi động Backend (Vulnerable App)
Mở một terminal mới:

Bash

cd vulnerable-app
# Cài đặt thư viện (nếu chưa có)
pip install flask
# Chạy ứng dụng
python3 app.py
App sẽ chạy tại: http://0.0.0.0:5000

4. Cấu hình DNS giả lập
Thêm dòng sau vào file /etc/hosts để giả lập tên miền:

Plaintext

127.0.0.1  test.waf.local
5. Cấu hình Dashboard
Truy cập http://localhost:17000.

Tạo Site mới:

Domain: test.waf.local

Port: 80

Upstream: http://<IP_MAY_HOST>:5000 (Lưu ý: Dùng IP LAN 192.168.x.x, không dùng localhost vì Docker không hiểu).

Tạo Rules:

Thêm rule chặn SQL Injection (Regex).

Thêm rule chặn XSS (Regex <script>).

🧪 Kịch bản Demo (Test Cases)
Dưới đây là các kịch bản tấn công đã được thực hiện để kiểm chứng khả năng bảo vệ của WAF.

1. Tấn công Cross-Site Scripting (XSS)
Kẻ tấn công cố gắng chèn mã JavaScript độc hại để đánh cắp Cookie hoặc chuyển hướng người dùng.

Payload: http://test.waf.local/xss?q=<script>alert('Hacked')</script>

Kết quả:

🔴 Không có WAF: Trình duyệt hiện hộp thoại Alert.

🟢 Có WAF: Trả về lỗi 403 Forbidden.

2. Tấn công SQL Injection (SQLi)
Kẻ tấn công cố gắng thao túng câu lệnh truy vấn Database.

Payload: http://test.waf.local/sqli?id=1' OR '1'='1

Kết quả:

🔴 Không có WAF: Hiển thị thông tin người dùng nhạy cảm.

🟢 Có WAF: Trả về lỗi 403 Forbidden.

3. Tấn công Path Traversal
Kẻ tấn công cố gắng truy cập file hệ thống trái phép.

Payload: http://test.waf.local/../../etc/passwd (Test bằng curl hoặc Burp Suite).

Kết quả: Bị chặn bởi Rule kiểm tra URI.

📸 Hình ảnh Demo (Evidence)

1. Dashboard quản lý WAF
Giao diện cấu hình Site và Rule.
![Site](images/Screenshot_2025-11-26_221537.png)

![Rules](images/Screenshot_2025-11-26_220818.png)

2. WAF chặn thành công (403 Forbidden)
Màn hình kẻ tấn công nhận được khi bị chặn.
![SQLi](WAF/images/Screenshot_2025-11-26_220714.png)

![XSS](images/Screenshot_2025-11-26_221943.png)

![CMDi](images/Screenshot_2025-11-26_222550.png)

![Path_Traversal](images/Screenshot_2025-11-26_222920.png)

3. Nhật ký tấn công (Audit Logs)
Hệ thống ghi lại chi tiết IP, thời gian và payload tấn công.
![Records](images/Screenshot_2025-11-26_220751.png)


⚠️ Tuyên bố miễn trừ trách nhiệm (Disclaimer)
Dự án này được xây dựng hoàn toàn cho mục đích GIÁO DỤC và NGHIÊN CỨU bảo mật. Tác giả không chịu trách nhiệm cho bất kỳ hành vi sử dụng sai mục đích nào trên các hệ thống thực tế mà không có sự cho phép.
