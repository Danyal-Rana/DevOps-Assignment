#!/bin/bash

# ===========================================
# Kubernetes Deployment Script for Todo App
# ===========================================

set -e  # Exit on any error

echo "🚀 Starting Kubernetes Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if minikube is running
if ! minikube status | grep -q "Running"; then
    print_warning "Minikube is not running. Starting minikube..."
    minikube start --driver=docker --memory=3000 --cpus=2
fi

# Enable metrics-server for HPA
print_status "Enabling metrics-server addon..."
minikube addons enable metrics-server

# Set Docker environment to minikube's Docker
print_status "Setting Docker environment to minikube..."
eval $(minikube docker-env)

# Build Docker images
print_status "Building backend Docker image..."
docker build -t todo-backend:latest ./server

print_status "Building frontend Docker image..."
docker build -t todo-frontend:latest ./client

# Apply Kubernetes manifests in order
print_status "Creating namespace..."
kubectl apply -f k8s/namespace.yaml

print_status "Creating secrets..."
kubectl apply -f k8s/secrets.yaml

print_status "Creating MongoDB PersistentVolumeClaim..."
kubectl apply -f k8s/mongodb-pvc.yaml

print_status "Deploying MongoDB..."
kubectl apply -f k8s/mongodb-deployment.yaml
kubectl apply -f k8s/mongodb-service.yaml

print_status "Waiting for MongoDB to be ready..."
kubectl wait --for=condition=ready pod -l app=mongodb -n todo-app --timeout=120s

print_status "Deploying Backend..."
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/backend-hpa.yaml

print_status "Deploying Frontend..."
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

# Wait for all deployments to be ready
print_status "Waiting for all pods to be ready..."
kubectl wait --for=condition=ready pod -l app=backend -n todo-app --timeout=120s
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app --timeout=120s

# Display deployment status
echo ""
echo "=========================================="
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "=========================================="
echo ""

# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

echo "📊 Cluster Status:"
kubectl get all -n todo-app

echo ""
echo "🌐 Access URLs:"
echo "   Frontend: http://$MINIKUBE_IP:30080"
echo "   Backend:  http://$MINIKUBE_IP:30500/api/health"

echo ""
echo "📝 Next Steps:"
echo "   1. Run 'ngrok http $MINIKUBE_IP:30080' to expose frontend"
echo "   2. Run 'minikube dashboard --url' and tunnel to expose dashboard"

echo ""
print_status "Deployment successful!"
