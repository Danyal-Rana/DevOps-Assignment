import React, { useState, useEffect } from 'react';

function TodoForm({ onSubmit, editingTodo, onCancelEdit }) {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        priority: 'medium'
    });

    // Update form when editing todo changes
    useEffect(() => {
        if (editingTodo) {
            setFormData({
                title: editingTodo.title,
                description: editingTodo.description || '',
                priority: editingTodo.priority || 'medium'
            });
        } else {
            setFormData({
                title: '',
                description: '',
                priority: 'medium'
            });
        }
    }, [editingTodo]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!formData.title.trim()) {
            alert('Please enter a title');
            return;
        }

        if (editingTodo) {
            onSubmit(editingTodo._id, formData);
        } else {
            onSubmit(formData);
        }

        // Reset form
        setFormData({
            title: '',
            description: '',
            priority: 'medium'
        });
    };

    const handleCancel = () => {
        setFormData({
            title: '',
            description: '',
            priority: 'medium'
        });
        onCancelEdit();
    };

    return (
        <form className="todo-form" onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="title">Title *</label>
                <input
                    type="text"
                    id="title"
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                    placeholder="What needs to be done?"
                    maxLength={200}
                />
            </div>

            <div className="form-group">
                <label htmlFor="description">Description</label>
                <textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    placeholder="Add more details (optional)"
                    maxLength={1000}
                />
            </div>

            <div className="form-group">
                <label htmlFor="priority">Priority</label>
                <select
                    id="priority"
                    name="priority"
                    value={formData.priority}
                    onChange={handleChange}
                >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                </select>
            </div>

            <div className="form-actions">
                <button type="submit" className="btn btn-primary">
                    {editingTodo ? '✓ Update Todo' : '+ Add Todo'}
                </button>
                {editingTodo && (
                    <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={handleCancel}
                    >
                        Cancel
                    </button>
                )}
            </div>
        </form>
    );
}

export default TodoForm;
