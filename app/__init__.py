from flask import Flask

# Khởi tạo Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/img/'  # Thư mục lưu ảnh tải lên
app.config['SECRET_KEY'] = 'your_secret_key'     # Key bảo mật

# Import routes (định nghĩa các route)
from app import routes
