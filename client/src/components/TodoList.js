import React from 'react';
import TodoItem from './TodoItem';

function TodoList({ todos, onToggle, onEdit, onDelete }) {
    if (todos.length === 0) {
        return (
            <div className="empty-state">
                <p>No todos yet! Add one above to get started.</p>
            </div>
        );
    }

    return (
        <div className="todo-list">
            {todos.map(todo => (
                <TodoItem
                    key={todo._id}
                    todo={todo}
                    onToggle={onToggle}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />
            ))}
        </div>
    );
}

export default TodoList;
