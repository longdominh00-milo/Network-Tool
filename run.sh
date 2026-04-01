#!/bin/bash
# ============================================================
# run.sh - Build và chạy Network Tool container
# Dùng khi server không có docker compose / docker-compose
# ============================================================

IMAGE_NAME="network-tool"
CONTAINER_NAME="network-tool"
PORT=5001

echo ">>> Stop and remove old container (if any)..."
sudo docker stop "$CONTAINER_NAME" 2>/dev/null || true
sudo docker rm   "$CONTAINER_NAME" 2>/dev/null || true

echo ">>> Build docker image..."
sudo docker build -t "$IMAGE_NAME" .

echo ">>> Run docker container..."
sudo docker run -d \
  --name "$CONTAINER_NAME" \
  -p 8081:"$PORT" \
  --network host \
  --cap-add NET_RAW \
  --cap-add NET_ADMIN \
  --restart unless-stopped \
  -e FLASK_APP=app.py \
  -e PYTHONUNBUFFERED=1 \
  -v "$(pwd)/users.json:/app/users.json" \
  "$IMAGE_NAME"

echo ""
echo "✅ Container is running!"
echo "   Access: http://$(hostname -I | awk '{print $1}'):8001"
echo ""
echo "   View logs : sudo docker logs -f $CONTAINER_NAME"
echo "   Stop     : sudo docker stop $CONTAINER_NAME"
