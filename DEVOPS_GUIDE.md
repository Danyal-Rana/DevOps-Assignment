# DevOps Assignment - Complete Guide

## Table of Contents
1. [Docker Files Explained](#1-docker-files-explained)
2. [Docker Compose Explained](#2-docker-compose-explained)
3. [Jenkinsfile Explained](#3-jenkinsfile-explained)
4. [Step-by-Step Assignment Completion](#4-step-by-step-assignment-completion)

---

# 1. Docker Files Explained

## What is a Dockerfile?
A Dockerfile is a text file containing instructions to build a Docker image. Think of it as a recipe that tells Docker how to create a container with your application.

---

## 1.1 Server Dockerfile (`server/Dockerfile`)

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci --only=production

COPY . .

# Production stage
FROM node:18-alpine

WORKDIR /app

RUN apk add --no-cache curl

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app .

EXPOSE 5000

CMD ["node", "server.js"]
```

### Line-by-Line Explanation:

| Line | Explanation |
|------|-------------|
| `FROM node:18-alpine AS builder` | **Base Image**: Uses Node.js 18 on Alpine Linux (small ~50MB). `AS builder` names this stage for multi-stage build. |
| `WORKDIR /app` | **Working Directory**: All subsequent commands run inside `/app` folder in the container. |
| `COPY package*.json ./` | **Copy Package Files**: Copies `package.json` and `package-lock.json` to container. Done first for Docker caching. |
| `RUN npm ci --only=production` | **Install Dependencies**: `npm ci` is faster than `npm install`, installs exact versions. `--only=production` skips devDependencies. |
| `COPY . .` | **Copy Source Code**: Copies all remaining files to container. |
| `FROM node:18-alpine` | **Second Stage**: Starts fresh from same base image (multi-stage build reduces final image size). |
| `RUN apk add --no-cache curl` | **Install curl**: Needed for health checks. `--no-cache` keeps image small. |
| `COPY --from=builder /app/node_modules ./node_modules` | **Copy from Builder**: Copies only what we need from the builder stage. |
| `EXPOSE 5000` | **Document Port**: Tells Docker this container listens on port 5000. Informational only. |
| `CMD ["node", "server.js"]` | **Startup Command**: Runs when container starts. Executes `node server.js`. |

### Why Multi-Stage Build?
- Stage 1 (builder): Installs dependencies
- Stage 2 (production): Only copies what's needed
- Result: Smaller, cleaner image without build tools

---

## 1.2 Client Dockerfile (`client/Dockerfile`)

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build

# Production stage - Nginx
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Line-by-Line Explanation:

| Line | Explanation |
|------|-------------|
| `FROM node:18-alpine AS builder` | Uses Node.js to build React app. |
| `RUN npm ci` | Installs ALL dependencies (including devDependencies needed for build). |
| `RUN npm run build` | **Builds React App**: Creates optimized production build in `/app/build` folder. |
| `FROM nginx:alpine` | **Switches to Nginx**: Lightweight web server to serve static files. |
| `COPY --from=builder /app/build /usr/share/nginx/html` | Copies built React files to Nginx's serving directory. |
| `COPY nginx.conf /etc/nginx/conf.d/default.conf` | Custom Nginx config for React Router and API proxy. |
| `CMD ["nginx", "-g", "daemon off;"]` | Runs Nginx in foreground (required for Docker). |

### Why Nginx instead of Node?
- React builds to static files (HTML, CSS, JS)
- Nginx serves static files faster than Node.js
- Much smaller footprint (~20MB vs ~150MB)

---

## 1.3 Tests Dockerfile (`tests/Dockerfile`)

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HEADLESS=true
ENV APP_URL=http://localhost:3000

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    --no-install-recommends \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tests

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p reports

CMD ["pytest", "--html=reports/test_report.html", "--self-contained-html", "-v", "--tb=short"]
```

### Line-by-Line Explanation:

| Line | Explanation |
|------|-------------|
| `FROM python:3.11-slim` | Python 3.11 on Debian slim (smaller than full Debian). |
| `ENV PYTHONDONTWRITEBYTECODE=1` | Prevents Python from creating `.pyc` files. |
| `ENV PYTHONUNBUFFERED=1` | Ensures Python output is sent straight to terminal. |
| `ENV HEADLESS=true` | Default: run Chrome without GUI. |
| `ENV APP_URL=http://localhost:3000` | Default app URL to test. |
| `RUN apt-get update && apt-get install -y ...` | Installs system dependencies needed for Chrome. |
| `wget ... google_signing_key.pub` | Adds Google's package signing key. |
| `echo "deb ... google-chrome.list"` | Adds Chrome repository. |
| `apt-get install -y google-chrome-stable` | **Installs Google Chrome** browser. |
| `rm -rf /var/lib/apt/lists/*` | Cleans up apt cache to reduce image size. |
| `COPY requirements.txt .` | Copies Python dependencies file. |
| `RUN pip install --no-cache-dir -r requirements.txt` | Installs Selenium, pytest, etc. |
| `RUN mkdir -p reports` | Creates reports directory. |
| `CMD ["pytest", ...]` | **Runs Tests**: Executes pytest with HTML report generation. |

### Key pytest Options:
| Option | Meaning |
|--------|---------|
| `--html=reports/test_report.html` | Generate HTML report |
| `--self-contained-html` | Embed CSS/JS in HTML file |
| `-v` | Verbose output |
| `--tb=short` | Short traceback on errors |

---

# 2. Docker Compose Explained

## What is Docker Compose?
Docker Compose is a tool for defining and running multi-container applications. Instead of running multiple `docker run` commands, you define everything in one YAML file.

## `docker-compose.yml`

```yaml
version: '3.8'

services:
  server:
    build:
      context: ./server
      dockerfile: Dockerfile
    container_name: todo-server
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
      - MONGO_URI=${MONGO_URI}
      - JWT_SECRET=${JWT_SECRET:-your-super-secret-jwt-key}
      - JWT_EXPIRE=7d
      - NODE_ENV=production
    networks:
      - todo-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  client:
    build:
      context: ./client
      dockerfile: Dockerfile
    container_name: todo-client
    ports:
      - "3000:80"
    depends_on:
      - server
    networks:
      - todo-network

  selenium-tests:
    build:
      context: ./tests
      dockerfile: Dockerfile
    container_name: todo-tests
    environment:
      - APP_URL=http://client:80
      - HEADLESS=true
    volumes:
      - ./tests/reports:/tests/reports
    depends_on:
      - client
      - server
    networks:
      - todo-network
    profiles:
      - test

networks:
  todo-network:
    driver: bridge
```

### Complete Field Reference:

#### Top-Level Keys:

| Key | Explanation |
|-----|-------------|
| `version: '3.8'` | Docker Compose file format version. 3.8 is widely compatible. |
| `services:` | Defines all containers to run. |
| `networks:` | Defines custom networks for container communication. |

#### Service Configuration (for each container):

| Key | Explanation | Example |
|-----|-------------|---------|
| `build:` | How to build the image | |
| `build.context` | Directory containing Dockerfile | `./server` |
| `build.dockerfile` | Name of Dockerfile | `Dockerfile` |
| `container_name` | Custom name for container | `todo-server` |
| `ports` | Port mapping `"HOST:CONTAINER"` | `"5000:5000"` |
| `environment` | Environment variables passed to container | `- PORT=5000` |
| `${MONGO_URI}` | Reads from host environment variable | Set in Jenkins |
| `${JWT_SECRET:-default}` | Uses default if not set | Fallback value |
| `networks` | Which networks to connect to | `- todo-network` |
| `depends_on` | Start order (waits for listed services) | `- server` |
| `volumes` | Mount host directory into container | `./tests/reports:/tests/reports` |
| `healthcheck` | Command to check if container is healthy | |
| `healthcheck.test` | Command to run | `curl http://localhost:5000/api/health` |
| `healthcheck.interval` | How often to check | `10s` |
| `healthcheck.timeout` | Max time for check | `5s` |
| `healthcheck.retries` | Failures before unhealthy | `5` |
| `profiles` | Only run with `--profile` flag | `- test` |

#### Network Configuration:

| Key | Explanation |
|-----|-------------|
| `todo-network:` | Network name |
| `driver: bridge` | Network type (bridge = isolated network for containers) |

### How Containers Communicate:

```
┌─────────────────── todo-network ───────────────────┐
│                                                     │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐      │
│  │ server  │◄───►│ client  │◄───►│  tests  │      │
│  │  :5000  │     │   :80   │     │         │      │
│  └─────────┘     └─────────┘     └─────────┘      │
│                                                     │
│  Containers use service names as hostnames:        │
│  - http://server:5000                              │
│  - http://client:80                                │
└─────────────────────────────────────────────────────┘
```

---

# 3. Jenkinsfile Explained

## What is a Jenkinsfile?
A Jenkinsfile defines your CI/CD pipeline as code. It tells Jenkins what steps to execute when building your project.

## Complete Jenkinsfile:

```groovy
pipeline {
    agent any
    
    environment {
        COMPOSE_PROJECT_NAME = 'todo-app'
        MONGO_URI = credentials('mongo-uri')
        JWT_SECRET = credentials('jwt-secret')
    }
    
    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
                echo '✅ Code fetched from GitHub'
            }
        }
        
        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
                echo '✅ All Docker images built'
            }
        }
        
        stage('Start Application') {
            steps {
                sh 'docker-compose up -d server client'
                sh '''
                    echo "Waiting for services to be ready..."
                    sleep 20
                    docker-compose ps
                '''
                echo '✅ Application started in containers'
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                sh '''
                    docker-compose run --rm \
                        -e APP_URL=http://client:80 \
                        -e HEADLESS=true \
                        selenium-tests
                '''
                echo '✅ Selenium tests completed'
            }
        }
    }
    
    post {
        always {
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'tests/reports',
                reportFiles: 'test_report.html',
                reportName: 'Selenium Test Report'
            ])
            sh 'docker-compose down --remove-orphans || true'
            sh 'docker system prune -f || true'
        }
        success {
            echo '✅ PIPELINE SUCCESSFUL!'
        }
        failure {
            echo '❌ PIPELINE FAILED!'
            sh 'docker-compose logs || true'
        }
    }
}
```

### Complete Field Reference:

#### Pipeline Structure:

| Key | Explanation |
|-----|-------------|
| `pipeline { }` | Root block for declarative pipeline |
| `agent any` | Run on any available Jenkins agent/node |
| `environment { }` | Define environment variables for entire pipeline |
| `stages { }` | Contains all stage definitions |
| `post { }` | Actions to run after all stages complete |

#### Environment Block:

| Key | Explanation |
|-----|-------------|
| `COMPOSE_PROJECT_NAME = 'todo-app'` | Names Docker Compose project (prefixes container names) |
| `MONGO_URI = credentials('mongo-uri')` | **Fetches secret** from Jenkins Credentials store by ID |
| `JWT_SECRET = credentials('jwt-secret')` | Same - fetches JWT secret securely |

#### Stage Structure:

```groovy
stage('Stage Name') {
    steps {
        // Commands to execute
    }
}
```

| Key | Explanation |
|-----|-------------|
| `stage('Name')` | Defines a pipeline stage (shown in Jenkins UI) |
| `steps { }` | Contains commands to run in this stage |

#### Common Step Commands:

| Command | Explanation |
|---------|-------------|
| `cleanWs()` | Cleans workspace (deletes all files) |
| `checkout scm` | Checks out code from configured SCM (Git) |
| `echo 'message'` | Prints message to console |
| `sh 'command'` | Runs shell command |
| `sh '''multi-line'''` | Runs multi-line shell script |

#### Post Block Conditions:

| Condition | When it runs |
|-----------|--------------|
| `always { }` | Always runs, regardless of success/failure |
| `success { }` | Only runs if pipeline succeeded |
| `failure { }` | Only runs if pipeline failed |
| `unstable { }` | Only if marked unstable (e.g., test failures) |

#### publishHTML Options:

| Option | Explanation |
|--------|-------------|
| `allowMissing: true` | Don't fail if report doesn't exist |
| `alwaysLinkToLastBuild: true` | Link to latest report |
| `keepAll: true` | Keep reports from all builds |
| `reportDir` | Directory containing report |
| `reportFiles` | Name of HTML file |
| `reportName` | Display name in Jenkins |

---

# 4. Step-by-Step Assignment Completion

## Prerequisites Checklist

- [ ] MERN Todo App working locally
- [ ] MongoDB Atlas account with connection string
- [ ] GitHub account
- [ ] AWS account with EC2 access

---

## STEP 1: Verify Local Files

Make sure you have these files:

```
DevOps-Assignment/
├── server/
│   ├── Dockerfile              ✅
│   ├── .dockerignore           ✅
│   ├── .gitignore              ✅
│   ├── .env                    ❌ (don't push)
│   ├── .env.example            ✅
│   ├── server.js
│   ├── package.json
│   └── ... (other server files)
│
├── client/
│   ├── Dockerfile              ✅
│   ├── nginx.conf              ✅
│   ├── .dockerignore           ✅
│   ├── package.json
│   └── ... (other client files)
│
├── tests/
│   ├── Dockerfile              ✅
│   ├── .dockerignore           ✅
│   ├── requirements.txt        ✅
│   ├── pytest.ini              ✅
│   ├── conftest.py             ✅
│   ├── test_auth.py            ✅
│   ├── test_todo.py            ✅
│   └── reports/                (generated)
│
├── docker-compose.yml          ✅
├── Jenkinsfile                 ✅
└── README.md                   ✅
```

---

## STEP 2: Push to GitHub

```bash
# Navigate to project
cd "e:\RanaDoesCode\DevOps-Assignment"

# Initialize git (if not done)
git init

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/DevOps-Assignment.git

# Check what will be pushed (should NOT include .env)
git status

# Add all files
git add .

# Commit
git commit -m "Complete MERN app with Selenium tests and CI/CD pipeline"

# Push to GitHub
git push -u origin main
```

### Verify on GitHub:
1. Go to `https://github.com/YOUR_USERNAME/DevOps-Assignment`
2. Check these files exist:
   - `Jenkinsfile`
   - `docker-compose.yml`
   - `tests/Dockerfile`
   - `tests/test_auth.py`
   - `tests/test_todo.py`

---

## STEP 3: Create EC2 Instance

### 3.1 Login to AWS Console
1. Go to [AWS Console](https://aws.amazon.com/console/)
2. Navigate to **EC2**

### 3.2 Launch Instance
1. Click **"Launch Instance"**
2. Configure:

| Setting | Value |
|---------|-------|
| Name | `jenkins-server` |
| AMI | Ubuntu Server 22.04 LTS |
| Instance type | `t2.medium` (2 vCPU, 4GB RAM) |
| Key pair | Create new or use existing |
| Network settings | Allow SSH (22), HTTP (80), Custom TCP (8080, 3000, 5000) |
| Storage | 20 GB gp3 |

3. Click **"Launch Instance"**

### 3.3 Note Your Instance Details
- Public IP: `XX.XX.XX.XX`
- Key pair file: `your-key.pem`

---

## STEP 4: Connect to EC2

### 4.1 SSH into Instance

```bash
# On Windows (PowerShell)
ssh -i "your-key.pem" ubuntu@XX.XX.XX.XX

# On Mac/Linux
chmod 400 your-key.pem
ssh -i "your-key.pem" ubuntu@XX.XX.XX.XX
```

---

## STEP 5: Install Dependencies on EC2

Run these commands one by one:

### 5.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 5.2 Install Docker
```bash
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

### 5.3 Install Docker Compose
```bash
sudo apt install docker-compose -y
```

### 5.4 Install Java (Required for Jenkins)
```bash
sudo apt install openjdk-17-jdk -y
```

### 5.5 Install Jenkins
```bash
# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt update
sudo apt install jenkins -y

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### 5.6 Add Jenkins User to Docker Group
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### 5.7 Get Jenkins Initial Password
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
**Copy this password!**

---

## STEP 6: Configure Jenkins

### 6.1 Access Jenkins
Open browser: `http://XX.XX.XX.XX:8080`

### 6.2 Unlock Jenkins
Paste the initial password from Step 5.7

### 6.3 Install Plugins
1. Click **"Install suggested plugins"**
2. Wait for installation
3. After completion, go to:
   - **Manage Jenkins → Plugins → Available plugins**
   - Search and install:
     - `Docker Pipeline`
     - `HTML Publisher`

### 6.4 Create Admin User
Fill in your details and save.

### 6.5 Add Credentials

1. Go to: **Manage Jenkins → Credentials → System → Global credentials**
2. Click **"Add Credentials"**

**Credential 1: MongoDB URI**
| Field | Value |
|-------|-------|
| Kind | Secret text |
| Secret | `mongodb+srv://username:password@cluster.mongodb.net/todo-app` |
| ID | `mongo-uri` |
| Description | MongoDB Atlas Connection String |

**Credential 2: JWT Secret**
| Field | Value |
|-------|-------|
| Kind | Secret text |
| Secret | `your-super-secret-jwt-key` |
| ID | `jwt-secret` |
| Description | JWT Secret Key |

---

## STEP 7: Create Jenkins Pipeline

### 7.1 Create New Job
1. Click **"New Item"**
2. Enter name: `todo-app-tests`
3. Select **"Pipeline"**
4. Click **"OK"**

### 7.2 Configure Pipeline
Scroll to **Pipeline** section:

| Setting | Value |
|---------|-------|
| Definition | Pipeline script from SCM |
| SCM | Git |
| Repository URL | `https://github.com/YOUR_USERNAME/DevOps-Assignment.git` |
| Branch | `*/main` |
| Script Path | `Jenkinsfile` |

Click **"Save"**

---

## STEP 8: Run the Pipeline

### 8.1 Build
1. Click **"Build Now"**
2. Watch the build progress

### 8.2 View Console Output
Click on build number → **"Console Output"**

### 8.3 View Test Report
After successful build:
1. Click on build number
2. Click **"Selenium Test Report"** on left sidebar

---

## STEP 9: Verify Everything Works

### Expected Pipeline Stages:
```
✅ Checkout         - Code fetched from GitHub
✅ Build Images     - Docker images built
✅ Start App        - Containers running
✅ Run Tests        - Selenium tests executed
✅ Cleanup          - Containers stopped
```

### Expected Test Report:
- 10+ test cases
- All passing (or showing failures with details)
- HTML report generated

---

## Troubleshooting

### Issue: Permission denied for Docker
```bash
sudo chmod 666 /var/run/docker.sock
sudo systemctl restart jenkins
```

### Issue: Tests failing
```bash
# Check container logs
cd /var/lib/jenkins/workspace/todo-app-tests
sudo docker-compose logs
```

### Issue: Cannot connect to EC2
- Check Security Group allows port 8080
- Check instance is running

---

## Summary

| What You Built | Technology |
|----------------|------------|
| Backend API | Express.js + MongoDB |
| Frontend | React |
| Testing | Selenium + Python + pytest |
| Containerization | Docker + Docker Compose |
| CI/CD | Jenkins Pipeline |
| Cloud | AWS EC2 |

### Assignment Requirements Met:
- ✅ Write automated test cases using Selenium
- ✅ Create an automation pipeline in Jenkins for test phase
- ✅ Configure and apply Jenkins pipeline for running automated test cases in a containerized way

---

## Quick Reference Commands

```bash
# EC2: Check Jenkins status
sudo systemctl status jenkins

# EC2: View Jenkins logs
sudo journalctl -u jenkins -f

# EC2: Check Docker containers
sudo docker ps -a

# EC2: View container logs
sudo docker-compose logs

# EC2: Restart Jenkins
sudo systemctl restart jenkins
```

---

**Congratulations! You've completed the DevOps assignment! 🎉**
