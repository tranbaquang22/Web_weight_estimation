import os
from flask import Flask
import math
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app
from app.api_client import call_api  # Import hàm gọi API
import cloudinary
import cloudinary.uploader
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
@app.template_filter('floatformat')
def floatformat(value, precision=0):
    try:
        value = float(value)
        return f"{value:.{precision}f}"
    except (ValueError, TypeError):
        return value
def allowed_file(filename):
    """Kiểm tra xem file có được phép upload không"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Route cho trang chủ"""
    return render_template('home.html', title="Trang chủ")

# Cấu hình Cloudinary
cloudinary.config(
    cloud_name='dnneb5dav',  # Thay bằng cloud_name của bạn
    api_key='159839376563776',        # Thay bằng API key
    api_secret='gj_LrVwUfC6T2bicyEApu1mARIM'   # Thay bằng API secret
)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image_file = request.files['image_file']
        name_product = request.form.get('name_product')
        name_level_1 = request.form.get('name_level_1')
        name_level_2 = request.form.get('name_level_2') or "Không xác định"
        name_level_3 = request.form.get('name_level_3') or "Không xác định"
        price_product = request.form.get('price_product')
        color = request.form.get('color') or "Không xác định"

        if image_file and allowed_file(image_file.filename):
            # Upload ảnh lên Cloudinary
            upload_result = cloudinary.uploader.upload(image_file)
            image_link = upload_result['url']  # URL công khai

            # Gọi API để dự đoán
            result = call_api(image_link, name_product, name_level_1, name_level_2, name_level_3, price_product)

            if "error" in result:
                flash(result["error"])
                return redirect(request.url)

            # Lấy giá trị trọng lượng từ API trả về
            estimated_weight = result.get('weight_estimation', "Không xác định")

            # Redirect đến trang kết quả
            return redirect(url_for(
                'result',
                filename=image_file.filename,
                result=result,
                image_url=image_link,
                name_product=name_product,
                price_product=price_product,
                color=color,
                estimated_weight=estimated_weight
            ))

    return render_template('upload.html', title="Upload Sản phẩm")





@app.route('/result')
def result():
    filename = request.args.get('filename')
    image_url = request.args.get('image_url')
    name_product = request.args.get('name_product')
    price_product = request.args.get('price_product')
    color = request.args.get('color')
    estimated_weight = request.args.get('estimated_weight')

    return render_template(
        'result.html',
        filename=filename,
        image_url=image_url,
        name_product=name_product,
        price_product=price_product,
        color=color,
        estimated_weight=estimated_weight
    )



