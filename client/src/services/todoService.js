import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Add auth token to requests
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Handle 401 responses (token expired)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/';
        }
        return Promise.reject(error);
    }
);

// Todo API Service
const todoService = {
    // Get all todos
    getAll: async () => {
        const response = await api.get('/todos');
        return response.data;
    },

    // Get single todo
    getById: async (id) => {
        const response = await api.get(`/todos/${id}`);
        return response.data;
    },

    // Create new todo
    create: async (todoData) => {
        const response = await api.post('/todos', todoData);
        return response.data;
    },

    // Update todo
    update: async (id, todoData) => {
        const response = await api.put(`/todos/${id}`, todoData);
        return response.data;
    },

    // Delete todo
    delete: async (id) => {
        const response = await api.delete(`/todos/${id}`);
        return response.data;
    },

    // Toggle todo completion
    toggle: async (id) => {
        const response = await api.patch(`/todos/${id}/toggle`);
        return response.data;
    }
};

export default todoService;
