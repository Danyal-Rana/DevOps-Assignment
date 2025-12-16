import React from 'react';

function TodoItem({ todo, onToggle, onEdit, onDelete }) {
    const getPriorityClass = (priority) => {
        switch (priority) {
            case 'high':
                return 'priority-high';
            case 'low':
                return 'priority-low';
            default:
                return 'priority-medium';
        }
    };

    const handleDelete = () => {
        if (window.confirm('Are you sure you want to delete this todo?')) {
            onDelete(todo._id);
        }
    };

    return (
        <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
            <div className="todo-header">
                <span className="todo-title">{todo.title}</span>
                <span className={`todo-priority ${getPriorityClass(todo.priority)}`}>
                    {todo.priority}
                </span>
            </div>

            {todo.description && (
                <p className="todo-description">{todo.description}</p>
            )}

            <div className="todo-actions">
                <button
                    className={`btn btn-sm ${todo.completed ? 'btn-warning' : 'btn-success'}`}
                    onClick={() => onToggle(todo._id)}
                >
                    {todo.completed ? '↩ Undo' : '✓ Complete'}
                </button>
                <button
                    className="btn btn-sm btn-primary"
                    onClick={() => onEdit(todo)}
                >
                    ✎ Edit
                </button>
                <button
                    className="btn btn-sm btn-danger"
                    onClick={handleDelete}
                >
                    ✕ Delete
                </button>
            </div>
        </div>
    );
}

export default TodoItem;
