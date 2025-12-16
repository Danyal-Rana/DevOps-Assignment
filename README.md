# 📝 MERN Stack Todo Application

> **DevOps Assignment Project** - A full-stack Todo application demonstrating modern web development practices with MongoDB, Express.js, React, and Node.js.

![MERN Stack](https://img.shields.io/badge/Stack-MERN-green)
![Node.js](https://img.shields.io/badge/Node.js-18+-brightgreen)
![React](https://img.shields.io/badge/React-18-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-6+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [API Endpoints](#-api-endpoints)
- [Environment Variables](#-environment-variables)
- [Selenium Testing](#-selenium-testing)
- [Screenshots](#-screenshots)
- [DevOps Considerations](#-devops-considerations)
- [License](#-license)

---

## 🎯 About The Project

This project is part of a **DevOps Assignment** that demonstrates the development of a complete full-stack web application using the MERN stack. The application implements a fully functional Todo management system with:

- Complete CRUD (Create, Read, Update, Delete) operations
- RESTful API architecture
- Interactive API documentation using Swagger/OpenAPI
- Modern React frontend with responsive design
- MongoDB database integration
- Proper environment configuration
- Clean code architecture with separation of concerns

---

## ✨ Features

### Backend Features
- ✅ RESTful API with Express.js
- ✅ MongoDB database with Mongoose ODM
- ✅ Full CRUD operations for todos
- ✅ Toggle completion status
- ✅ Priority levels (Low, Medium, High)
- ✅ **Swagger/OpenAPI documentation**
- ✅ CORS configuration
- ✅ Environment-based configuration
- ✅ Error handling middleware
- ✅ Health check endpoint

### Frontend Features
- ✅ Modern React 18 with Hooks
- ✅ Create, edit, and delete todos
- ✅ Mark todos as complete/incomplete
- ✅ Priority-based visual indicators
- ✅ Real-time statistics dashboard
- ✅ Responsive design for all devices
- ✅ Beautiful gradient UI
- ✅ Form validation
- ✅ Error handling with user feedback

---

## 🛠 Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Node.js** | JavaScript runtime environment |
| **Express.js** | Web application framework |
| **MongoDB** | NoSQL database |
| **Mongoose** | MongoDB object modeling |
| **Swagger** | API documentation |
| **CORS** | Cross-origin resource sharing |
| **dotenv** | Environment variable management |
| **Nodemon** | Development auto-restart |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI library |
| **Axios** | HTTP client |
| **CSS3** | Styling with gradients & animations |

---

## 📁 Project Structure

```
DevOps-Assignment/
│
├── 📂 server/                      # Backend (Express.js)
│   ├── 📂 config/
│   │   └── swagger.js              # Swagger configuration
│   ├── 📂 controllers/
│   │   ├── auth.controller.js      # Authentication logic
│   │   └── todo.controller.js      # Todo CRUD logic
│   ├── 📂 middleware/
│   │   ├── auth.middleware.js      # JWT verification
│   │   └── validation.middleware.js # Input validation
│   ├── 📂 models/
│   │   ├── user.model.js           # User schema
│   │   └── todo.model.js           # Todo schema
│   ├── 📂 routes/
│   │   ├── auth.routes.js          # Auth endpoints
│   │   └── todo.routes.js          # Todo endpoints
│   ├── server.js                   # Entry point
│   ├── .env                        # Environment variables
│   ├── .env.example                # Environment template
│   ├── .gitignore
│   └── package.json
│
├── 📂 client/                      # Frontend (React)
│   ├── 📂 public/
│   │   └── index.html
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── Login.js            # Login form
│   │   │   ├── Register.js         # Registration form
│   │   │   ├── TodoForm.js         # Create/Edit form
│   │   │   ├── TodoList.js         # List container
│   │   │   └── TodoItem.js         # Individual todo card
│   │   ├── 📂 context/
│   │   │   └── AuthContext.js      # Auth state management
│   │   ├── 📂 services/
│   │   │   ├── authService.js      # Auth API calls
│   │   │   └── todoService.js      # Todo API calls
│   │   ├── App.js                  # Main component
│   │   ├── index.js                # Entry point
│   │   └── index.css               # Global styles
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   └── package.json
│
├── 📂 tests/                       # Selenium Tests (Python)
│   ├── conftest.py                 # Pytest fixtures
│   ├── pytest.ini                  # Pytest config
│   ├── requirements.txt            # Python dependencies
│   ├── run_tests.py                # Test runner
│   ├── Dockerfile                  # Docker for CI/CD
│   ├── test_auth.py                # Authentication tests
│   └── test_todo.py                # Todo CRUD tests
│
└── README.md                       # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- **Node.js** (v14 or higher) - [Download](https://nodejs.org/)
- **MongoDB** (local or Atlas) - [MongoDB Atlas](https://www.mongodb.com/atlas)
- **npm** or **yarn**
- **Git**

### Installation

#### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd DevOps-Assignment
```

#### 2️⃣ Backend Setup

```bash
# Navigate to server directory
cd server

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env and add your MongoDB URI
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/todo-app
```

#### 3️⃣ Frontend Setup

```bash
# Navigate to client directory (from root)
cd client

# Install dependencies
npm install

# Create environment file
cp .env.example .env
```

#### 4️⃣ Run the Application

**Start Backend Server:**
```bash
cd server
npm run dev     # Development mode with hot reload
# OR
npm start       # Production mode
```
Backend runs on: `http://localhost:5000`

**Start Frontend (new terminal):**
```bash
cd client
npm start
```
Frontend runs on: `http://localhost:3000`

---

## 📚 API Documentation

### Swagger UI

Once the server is running, access the interactive API documentation at:

🔗 **http://localhost:5000/api-docs**

The Swagger UI provides:
- 📖 Complete API documentation
- 🧪 Interactive API testing
- 📋 Request/Response schemas
- 🔍 Try out endpoints directly

### Swagger JSON

Access the OpenAPI specification JSON at:
🔗 **http://localhost:5000/api-docs.json**

---

## 📡 API Endpoints

### Base URL: `http://localhost:5000/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/todos` | Get all todos |
| `GET` | `/todos/:id` | Get a single todo |
| `POST` | `/todos` | Create a new todo |
| `PUT` | `/todos/:id` | Update a todo |
| `DELETE` | `/todos/:id` | Delete a todo |
| `PATCH` | `/todos/:id/toggle` | Toggle completion status |
| `GET` | `/health` | API health check |

### Request/Response Examples

#### Create Todo
```bash
POST /api/todos
Content-Type: application/json

{
  "title": "Complete DevOps Assignment",
  "description": "Implement MERN stack todo app",
  "priority": "high"
}
```

#### Response
```json
{
  "success": true,
  "message": "Todo created successfully",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "title": "Complete DevOps Assignment",
    "description": "Implement MERN stack todo app",
    "completed": false,
    "priority": "high",
    "createdAt": "2025-12-17T10:00:00.000Z",
    "updatedAt": "2025-12-17T10:00:00.000Z"
  }
}
```

---

## ⚙️ Environment Variables

### Server (`server/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `5000` |
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/todo-app` |
| `CLIENT_URL` | Frontend URL for CORS | `http://localhost:3000` |

### Client (`client/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `http://localhost:5000/api` |

---

## 🧪 Selenium Testing

This project includes **12 automated test cases** using Selenium WebDriver with Python for browser automation testing.

### Test Structure

```
tests/
├── conftest.py          # Pytest fixtures and configuration
├── pytest.ini           # Pytest settings
├── requirements.txt     # Python dependencies
├── run_tests.py         # Test runner script
├── Dockerfile           # Docker image for CI/CD
├── test_auth.py         # Authentication tests (7 tests)
└── test_todo.py         # Todo CRUD tests (5 tests)
```

### Test Cases

| # | Test Case | Category | Description |
|---|-----------|----------|-------------|
| 1 | Register with valid data | Auth | Fill form, submit, verify success |
| 2 | Register with invalid email | Auth | Check email validation error |
| 3 | Register with short password | Auth | Check password validation error |
| 4 | Login with valid credentials | Auth | Verify redirect to todos |
| 5 | Login with wrong password | Auth | Check error message |
| 6 | Login with empty fields | Auth | Check validation for empty form |
| 7 | Create a new todo | CRUD | Add todo, verify it appears |
| 8 | Mark todo as complete | CRUD | Toggle, verify status changes |
| 9 | Edit an existing todo | CRUD | Update title, verify change |
| 10 | Delete a todo | CRUD | Remove, verify it's gone |
| 11 | Register with mismatched passwords | Auth | Check password mismatch error |
| 12 | Session persistence after refresh | Auth | Verify user stays logged in |

### Running Tests Locally

```bash
# Navigate to tests directory
cd tests

# Install dependencies
pip install -r requirements.txt

# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --auth    # Authentication tests only
python run_tests.py --todo    # Todo CRUD tests only
python run_tests.py --smoke   # Critical path tests only
```

### Running Tests with Docker

```bash
# Build Docker image
docker build -t selenium-tests ./tests

# Run tests in container
docker run --rm \
  -e APP_URL=http://host.docker.internal:3000 \
  -v $(pwd)/tests/reports:/tests/reports \
  selenium-tests
```

### Environment Variables for Testing

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_URL` | Application URL to test | `http://localhost:3000` |
| `HEADLESS` | Run Chrome in headless mode | `true` |

---

## 📸 Screenshots

### Todo Application UI
```
┌─────────────────────────────────────────────┐
│            📝 Todo App                      │
│          MERN Stack Application             │
│                                             │
│     Total: 5  │  Completed: 2  │  Pending: 3│
├─────────────────────────────────────────────┤
│  [Create New Todo Form]                     │
│  Title: ____________________                │
│  Description: ______________                │
│  Priority: [Medium ▼]                       │
│  [+ Add Todo]                               │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐    │
│  │ Complete DevOps Assignment    HIGH  │    │
│  │ Implement MERN stack todo app       │    │
│  │ [✓ Complete] [✎ Edit] [✕ Delete]   │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### Swagger Documentation
```
┌─────────────────────────────────────────────┐
│  Todo API - DevOps Assignment       v1.0.0  │
├─────────────────────────────────────────────┤
│                                             │
│  Todos                                      │
│  ├── GET    /api/todos          ▶ Try it   │
│  ├── POST   /api/todos          ▶ Try it   │
│  ├── GET    /api/todos/{id}     ▶ Try it   │
│  ├── PUT    /api/todos/{id}     ▶ Try it   │
│  ├── DELETE /api/todos/{id}     ▶ Try it   │
│  └── PATCH  /api/todos/{id}/toggle         │
│                                             │
│  Health                                     │
│  └── GET    /api/health         ▶ Try it   │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🔧 DevOps Considerations

This project is designed with DevOps best practices in mind:

### ✅ Version Control
- Proper `.gitignore` files for both client and server
- Environment files excluded from version control
- `.env.example` templates provided

### ✅ Configuration Management
- Environment-based configuration
- Separation of development and production settings
- Centralized configuration files

### ✅ Documentation
- Comprehensive README documentation
- Swagger/OpenAPI for API documentation
- Inline code comments

### ✅ Code Organization
- Clean architecture with separation of concerns
- MVC pattern in backend
- Component-based frontend architecture

### ✅ Future DevOps Enhancements
- 🐳 Docker containerization
- 🔄 CI/CD pipeline integration
- ☸️ Kubernetes deployment
- 📊 Monitoring and logging
- 🧪 Automated testing

---

## 🧪 Testing the API

### Using Swagger UI
1. Open `http://localhost:5000/api-docs`
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Using cURL

```bash
# Get all todos
curl http://localhost:5000/api/todos

# Create a todo
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Todo","priority":"high"}'

# Toggle completion
curl -X PATCH http://localhost:5000/api/todos/<id>/toggle
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**DevOps Assignment Project**

---

## 🙏 Acknowledgments

- MERN Stack community
- Swagger/OpenAPI documentation
- React.js team
- MongoDB team

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Made with ❤️ as part of DevOps Assignment

</div>
