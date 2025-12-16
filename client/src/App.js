import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import todoService from './services/todoService';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import Login from './components/Login';
import Register from './components/Register';

// Main Todo Application Component
function TodoApp() {
    const { user, logout } = useAuth();
    const [todos, setTodos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [editingTodo, setEditingTodo] = useState(null);

    // Fetch all todos on component mount
    useEffect(() => {
        fetchTodos();
    }, []);

    const fetchTodos = async () => {
        try {
            setLoading(true);
            const response = await todoService.getAll();
            setTodos(response.data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch todos. Make sure the server is running.');
            console.error('Error fetching todos:', err);
        } finally {
            setLoading(false);
        }
    };

    // Create new todo
    const handleCreate = async (todoData) => {
        try {
            const response = await todoService.create(todoData);
            setTodos([response.data, ...todos]);
            setError(null);
        } catch (err) {
            setError('Failed to create todo');
            console.error('Error creating todo:', err);
        }
    };

    // Update todo
    const handleUpdate = async (id, todoData) => {
        try {
            const response = await todoService.update(id, todoData);
            setTodos(todos.map(todo =>
                todo._id === id ? response.data : todo
            ));
            setEditingTodo(null);
            setError(null);
        } catch (err) {
            setError('Failed to update todo');
            console.error('Error updating todo:', err);
        }
    };

    // Delete todo
    const handleDelete = async (id) => {
        try {
            await todoService.delete(id);
            setTodos(todos.filter(todo => todo._id !== id));
            setError(null);
        } catch (err) {
            setError('Failed to delete todo');
            console.error('Error deleting todo:', err);
        }
    };

    // Toggle todo completion
    const handleToggle = async (id) => {
        try {
            const response = await todoService.toggle(id);
            setTodos(todos.map(todo =>
                todo._id === id ? response.data : todo
            ));
            setError(null);
        } catch (err) {
            setError('Failed to toggle todo');
            console.error('Error toggling todo:', err);
        }
    };

    // Start editing
    const handleEdit = (todo) => {
        setEditingTodo(todo);
    };

    // Cancel editing
    const handleCancelEdit = () => {
        setEditingTodo(null);
    };

    // Calculate stats
    const completedCount = todos.filter(todo => todo.completed).length;
    const pendingCount = todos.length - completedCount;

    return (
        <div className="app">
            <header className="app-header">
                <h1>📝 Todo App</h1>
                <div className="user-info">
                    <span>Welcome, <strong>{user?.username}</strong></span>
                    <button className="btn btn-logout" onClick={logout}>
                        Logout
                    </button>
                </div>
            </header>

            {todos.length > 0 && (
                <div className="stats">
                    <div className="stat-item">
                        <div className="stat-number">{todos.length}</div>
                        <div className="stat-label">Total</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-number">{completedCount}</div>
                        <div className="stat-label">Completed</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-number">{pendingCount}</div>
                        <div className="stat-label">Pending</div>
                    </div>
                </div>
            )}

            <TodoForm
                onSubmit={editingTodo ? handleUpdate : handleCreate}
                editingTodo={editingTodo}
                onCancelEdit={handleCancelEdit}
            />

            {error && <div className="error-message">{error}</div>}

            {loading ? (
                <div className="loading">Loading todos...</div>
            ) : (
                <TodoList
                    todos={todos}
                    onToggle={handleToggle}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                />
            )}
        </div>
    );
}

// Auth Wrapper Component
function AuthWrapper() {
    const { isAuthenticated } = useAuth();
    const [isLoginView, setIsLoginView] = useState(true);

    if (isAuthenticated) {
        return <TodoApp />;
    }

    return isLoginView ? (
        <Login onSwitchToRegister={() => setIsLoginView(false)} />
    ) : (
        <Register onSwitchToLogin={() => setIsLoginView(true)} />
    );
}

// Main App Component with Provider
function App() {
    return (
        <AuthProvider>
            <AuthWrapper />
        </AuthProvider>
    );
}

export default App;
