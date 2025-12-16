const Todo = require('../models/todo.model');

// @desc    Get all todos for logged in user
// @route   GET /api/todos
const getAllTodos = async (req, res) => {
    try {
        const todos = await Todo.find({ user: req.user.id }).sort({ createdAt: -1 });
        res.status(200).json({
            success: true,
            count: todos.length,
            data: todos
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error fetching todos',
            error: error.message
        });
    }
};

// @desc    Get single todo
// @route   GET /api/todos/:id
const getTodoById = async (req, res) => {
    try {
        const todo = await Todo.findOne({ _id: req.params.id, user: req.user.id });

        if (!todo) {
            return res.status(404).json({
                success: false,
                message: 'Todo not found'
            });
        }

        res.status(200).json({
            success: true,
            data: todo
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error fetching todo',
            error: error.message
        });
    }
};

// @desc    Create new todo
// @route   POST /api/todos
const createTodo = async (req, res) => {
    try {
        const { title, description, priority } = req.body;

        if (!title) {
            return res.status(400).json({
                success: false,
                message: 'Title is required'
            });
        }

        const todo = await Todo.create({
            title,
            description,
            priority,
            user: req.user.id
        });

        res.status(201).json({
            success: true,
            message: 'Todo created successfully',
            data: todo
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error creating todo',
            error: error.message
        });
    }
};

// @desc    Update todo
// @route   PUT /api/todos/:id
const updateTodo = async (req, res) => {
    try {
        const { title, description, completed, priority } = req.body;

        const todo = await Todo.findOne({ _id: req.params.id, user: req.user.id });

        if (!todo) {
            return res.status(404).json({
                success: false,
                message: 'Todo not found'
            });
        }

        const updatedTodo = await Todo.findByIdAndUpdate(
            req.params.id,
            { title, description, completed, priority },
            { new: true, runValidators: true }
        );

        res.status(200).json({
            success: true,
            message: 'Todo updated successfully',
            data: updatedTodo
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error updating todo',
            error: error.message
        });
    }
};

// @desc    Delete todo
// @route   DELETE /api/todos/:id
const deleteTodo = async (req, res) => {
    try {
        const todo = await Todo.findOne({ _id: req.params.id, user: req.user.id });

        if (!todo) {
            return res.status(404).json({
                success: false,
                message: 'Todo not found'
            });
        }

        await Todo.findByIdAndDelete(req.params.id);

        res.status(200).json({
            success: true,
            message: 'Todo deleted successfully'
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error deleting todo',
            error: error.message
        });
    }
};

// @desc    Toggle todo completion
// @route   PATCH /api/todos/:id/toggle
const toggleTodo = async (req, res) => {
    try {
        const todo = await Todo.findOne({ _id: req.params.id, user: req.user.id });

        if (!todo) {
            return res.status(404).json({
                success: false,
                message: 'Todo not found'
            });
        }

        todo.completed = !todo.completed;
        await todo.save();

        res.status(200).json({
            success: true,
            message: `Todo marked as ${todo.completed ? 'completed' : 'incomplete'}`,
            data: todo
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error toggling todo',
            error: error.message
        });
    }
};

module.exports = {
    getAllTodos,
    getTodoById,
    createTodo,
    updateTodo,
    deleteTodo,
    toggleTodo
};
