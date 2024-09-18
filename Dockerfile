# Chọn image python chính thức với phiên bản slim để giảm dung lượng image
FROM python:3.12-slim

# Cài đặt make và docker-compose
RUN apt-get update && \
    apt-get install -y make curl && \
    curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '\"' -f 4)/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Cài đặt các gói phụ thuộc hệ thống
RUN apt-get update && apt-get install -y gcc libpq-dev

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt và cài đặt các gói Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của bạn vào thư mục /app
COPY . .

# Mở port cho ứng dụng Flask (port 5000)
EXPOSE 5000

# Đặt lệnh mặc định để khởi động ứng dụng sử dụng make
CMD ["make", "start"]
