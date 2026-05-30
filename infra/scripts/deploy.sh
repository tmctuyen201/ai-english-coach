# AI English Coach — Deploy Script
#!/bin/bash
set -e

echo "🚀 Deploying AI English Coach..."

# Load environment
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Build and deploy
echo "📦 Building containers..."
docker compose build

echo "🗄️ Starting database services..."
docker compose up -d postgres redis qdrant minio

echo "⏳ Waiting for database to be ready..."
sleep 5

echo "🔧 Running database migrations..."
docker compose exec backend alembic upgrade head

echo "🌐 Starting application..."
docker compose up -d backend frontend nginx celery_worker celery_beat

echo "✅ Deployment complete!"
echo ""
echo "Services:"
echo "  Frontend:    http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo "  Flower:      http://localhost:5555"
echo "  MinIO:       http://localhost:9001"
echo ""
echo "Health check:"
curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "Backend starting..."
