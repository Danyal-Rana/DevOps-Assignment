# Kubernetes Deployment Guide - Todo Application

This guide walks you through deploying the Todo application on a Kubernetes (minikube) cluster hosted on an AWS EC2 instance, with ngrok tunnels for external access.

---

## Table of Contents

1. [AWS EC2 Instance Setup](#1-aws-ec2-instance-setup)
2. [Install Docker](#2-install-docker)
3. [Install Minikube & kubectl](#3-install-minikube--kubectl)
4. [Clone & Build Docker Images](#4-clone--build-docker-images)
5. [Deploy to Kubernetes](#5-deploy-to-kubernetes)
6. [Setup ngrok Tunnels](#6-setup-ngrok-tunnels)
7. [Verification & Testing](#7-verification--testing)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. AWS EC2 Instance Setup

### Step 1.1: Launch EC2 Instance

1. Go to **AWS Console → EC2 → Launch Instance**
2. Configure the following:

| Setting           | Value                                                 |
| ----------------- | ----------------------------------------------------- |
| **Name**          | `kubernetes-todo-app`                                 |
| **AMI**           | Ubuntu Server 22.04 LTS (Free tier eligible)          |
| **Instance Type** | `t2.medium` (2 vCPU, 4 GB RAM) - **minimum required** |
| **Key Pair**      | Create new or use existing (.pem file)                |
| **Storage**       | 30 GB gp3 (increase from default 8GB)                 |

### Step 1.2: Configure Security Group

Create a new security group with these inbound rules:

| Type       | Port Range  | Source    | Description               |
| ---------- | ----------- | --------- | ------------------------- |
| SSH        | 22          | My IP     | SSH access                |
| Custom TCP | 30000-32767 | 0.0.0.0/0 | Kubernetes NodePort range |
| HTTP       | 80          | 0.0.0.0/0 | Web traffic               |
| HTTPS      | 443         | 0.0.0.0/0 | Secure web traffic        |

### Step 1.3: Connect to EC2

```bash
# Make your key file secure (run on your local machine)
chmod 400 your-key.pem

# SSH into EC2
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

---

## 2. Install Docker

Run these commands on your EC2 instance:

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io

# Start Docker and enable on boot
sudo systemctl start docker
sudo systemctl enable docker

# Add ubuntu user to docker group (avoids needing sudo)
sudo usermod -aG docker $USER

# Log out and log back in for group change to take effect
exit
```

SSH back in and verify:

```bash
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
docker --version
```

---

## 3. Install Minikube & kubectl

### Install kubectl

```bash
# Download kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Make executable and move to PATH
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify
kubectl version --client
```

### Install Minikube

```bash
# Download minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# Install minikube
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify
minikube version
```

### Start Minikube

```bash
# Start minikube with Docker driver
minikube start --driver=docker --memory=3000 --cpus=2

# Enable metrics-server addon (required for HPA)
minikube addons enable metrics-server

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

---

## 4. Clone & Build Docker Images

### Clone Repository

```bash
# Clone your repository
git clone https://github.com/Danyal-Rana/DevOps-Assignment.git
cd DevOps-Assignment
```

### Build Images Inside Minikube's Docker

**Important:** To use local images in minikube, build them inside minikube's Docker environment:

```bash
# Point your shell to minikube's Docker daemon
eval $(minikube docker-env)

# Build backend image
docker build -t todo-backend:latest ./server

# Build frontend image
docker build -t todo-frontend:latest ./client

# Verify images are built
docker images | grep todo
```

---

## 5. Deploy to Kubernetes

### Apply YAML Files in Order

```bash
# Create namespace first
kubectl apply -f k8s/namespace.yaml

# Create secrets
kubectl apply -f k8s/secrets.yaml

# Deploy MongoDB (PVC → Deployment → Service)
kubectl apply -f k8s/mongodb-pvc.yaml
kubectl apply -f k8s/mongodb-deployment.yaml
kubectl apply -f k8s/mongodb-service.yaml

# Wait for MongoDB to be ready
kubectl wait --for=condition=ready pod -l app=mongodb -n todo-app --timeout=120s

# Deploy Backend
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/backend-hpa.yaml

# Deploy Frontend
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

Or use the deploy script:

```bash
chmod +x deploy.sh
./deploy.sh
```

### Verify Deployment

```bash
# Check all resources
kubectl get all -n todo-app

# Check pods are running
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check PVC is bound
kubectl get pvc -n todo-app

# Check HPA status
kubectl get hpa -n todo-app
```

Expected output:

```
NAME                                      READY   STATUS    RESTARTS   AGE
pod/backend-deployment-xxxxx-xxxxx        1/1     Running   0          1m
pod/backend-deployment-xxxxx-xxxxx        1/1     Running   0          1m
pod/frontend-deployment-xxxxx-xxxxx       1/1     Running   0          1m
pod/frontend-deployment-xxxxx-xxxxx       1/1     Running   0          1m
pod/mongodb-deployment-xxxxx-xxxxx        1/1     Running   0          2m

NAME                       TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)
service/backend-service    NodePort   10.xxx.xxx.xxx   <none>        5000:30500/TCP
service/frontend-service   NodePort   10.xxx.xxx.xxx   <none>        80:30080/TCP
service/mongodb-service    NodePort   10.xxx.xxx.xxx   <none>        27017:30017/TCP
```

---

## 6. Setup ngrok Tunnels

### Install ngrok

```bash
# Download ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# OR download directly
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
```

### Authenticate ngrok

1. Go to https://dashboard.ngrok.com/signup and create a free account
2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
3. Run:

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### Create Tunnel for Frontend (Web Application)

```bash
# Get the minikube IP and frontend NodePort
MINIKUBE_IP=$(minikube ip)
echo "Minikube IP: $MINIKUBE_IP"

# Start ngrok tunnel for frontend (in a new terminal or use screen/tmux)
ngrok http $MINIKUBE_IP:30080
```

Save the generated URL (e.g., `https://xxxx-xx-xx-xx-xx.ngrok-free.app`)

### Create Tunnel for Minikube Dashboard

In a **new terminal**:

```bash
# Start minikube dashboard (runs in background)
minikube dashboard --url &

# The dashboard usually runs on a random port. Get the URL:
# It will print something like: http://127.0.0.1:XXXXX/api/v1/namespaces/kubernetes-dashboard/...

# Start ngrok tunnel for dashboard
ngrok http 127.0.0.1:XXXXX  # Replace XXXXX with the actual port
```

### Using tmux for Multiple Terminals

```bash
# Install tmux
sudo apt install tmux

# Start tmux session
tmux new -s tunnels

# Split pane horizontally: Ctrl+B then "

# In first pane: ngrok for frontend
ngrok http $(minikube ip):30080

# Switch pane: Ctrl+B then arrow key
# In second pane: ngrok for dashboard
minikube dashboard --url
# Then in another split, tunnel to that port
```

---

## 7. Verification & Testing

### Test Application

1. Open the ngrok frontend URL in your browser
2. Register a new account
3. Create, update, and delete todos
4. Verify everything works

### Test Persistence

```bash
# Delete the MongoDB pod
kubectl delete pod -l app=mongodb -n todo-app

# Wait for new pod to come up
kubectl get pods -n todo-app -w

# Check the app - your data should still be there!
```

### Test Auto-scaling (HPA)

```bash
# Watch HPA in one terminal
kubectl get hpa -n todo-app -w

# In another terminal, generate load
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -n todo-app -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://backend-service:5000/api/health; done"

# Watch the replicas increase
```

### Check Pod Logs

```bash
# Backend logs
kubectl logs -l app=backend -n todo-app

# Frontend logs
kubectl logs -l app=frontend -n todo-app

# MongoDB logs
kubectl logs -l app=mongodb -n todo-app
```

---

## 8. Troubleshooting

### Pods Not Starting

```bash
# Check pod events
kubectl describe pod <pod-name> -n todo-app

# Check pod logs
kubectl logs <pod-name> -n todo-app
```

### ImagePullBackOff Error

Make sure you built images inside minikube's Docker:

```bash
eval $(minikube docker-env)
docker images | grep todo
```

### MongoDB Connection Issues

```bash
# Verify MongoDB is running
kubectl get pods -l app=mongodb -n todo-app

# Test MongoDB connection from backend pod
kubectl exec -it <backend-pod-name> -n todo-app -- sh
# Inside pod:
wget -qO- mongodb-service:27017
```

### HPA Not Scaling

```bash
# Ensure metrics-server is running
kubectl get pods -n kube-system | grep metrics-server

# If not enabled:
minikube addons enable metrics-server

# Wait a few minutes and check again
kubectl top pods -n todo-app
```

### Reset Everything

```bash
# Delete all resources
kubectl delete namespace todo-app

# Restart minikube
minikube stop
minikube start
```

---

## Quick Reference

| Component   | NodePort | URL                                      |
| ----------- | -------- | ---------------------------------------- |
| Frontend    | 30080    | `http://$(minikube ip):30080`            |
| Backend API | 30500    | `http://$(minikube ip):30500/api/health` |
| MongoDB     | 30017    | `mongodb://$(minikube ip):30017`         |

### Useful Commands

```bash
# Get all resources
kubectl get all -n todo-app

# Watch pods
kubectl get pods -n todo-app -w

# Port forward (alternative to NodePort)
kubectl port-forward svc/frontend-service 8080:80 -n todo-app

# Scale deployment manually
kubectl scale deployment backend-deployment --replicas=5 -n todo-app

# View HPA details
kubectl describe hpa backend-hpa -n todo-app
```
