# ============================================================
# Dockerfile - Network Tool
# Base: Ubuntu 22.04 (giống môi trường server hiện tại)
# ============================================================
FROM ubuntu:22.04

# Không cho apt hỏi timezone hay interactive prompt
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# ----------------------------------------------------------
# Cài hệ thống: Python, các tool network cần thiết
# ----------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    # Network tools được dùng bởi exec_data.py / network_tool.py
    iputils-ping \
    mtr-tiny \
    traceroute \
    hping3 \
    iproute2 \
    dnsutils \
    nmap \
    openssh-client \
    # Build deps cho một số Python packages (netmiko, cryptography)
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------
# Tạo thư mục làm việc
# ----------------------------------------------------------
WORKDIR /app

# ----------------------------------------------------------
# Cài Python dependencies
# ----------------------------------------------------------
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------
# Copy toàn bộ source code
# ----------------------------------------------------------
COPY . .

# ----------------------------------------------------------
# Đảm bảo script shell có quyền execute
# ----------------------------------------------------------
RUN chmod +x nping_wrapper.sh

# ----------------------------------------------------------
# hping3 cần setuid root hoặc NET_RAW capability
# Đặt setuid cho hping3 để ping TCP hoạt động khi chạy
# (Thay thế: dùng --cap-add=NET_RAW khi docker run)
# ----------------------------------------------------------
RUN chmod u+s /usr/sbin/hping3 || true

# ----------------------------------------------------------
# Expose port Flask
# ----------------------------------------------------------
EXPOSE 5001

# ----------------------------------------------------------
# Chạy Flask app
# ----------------------------------------------------------
CMD ["python3", "app.py"]
