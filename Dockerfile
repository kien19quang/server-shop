# Chọn image python chính thức với phiên bản slim để giảm dung lượng image
FROM python:3.12-slim

# Cài đặt các gói phụ thuộc hệ thống cần thiết (gcc, libpq-dev) và loại bỏ các gói không cần thiết
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Thiết lập biến môi trường cho môi trường production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt và cài đặt các gói Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của bạn vào thư mục /app
COPY . .

# Mở port cho ứng dụng (port 5000)
EXPOSE 5000

# Sử dụng Gunicorn để chạy ứng dụng Flask
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
