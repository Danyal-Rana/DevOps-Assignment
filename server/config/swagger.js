const swaggerJsdoc = require('swagger-jsdoc');

const options = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'Todo API - DevOps Assignment',
            version: '1.0.0',
            description: 'A complete MERN Stack Todo Application API with full CRUD operations. This project is part of a DevOps Assignment demonstrating modern web development practices.',
            contact: {
                name: 'Developer',
                email: 'developer@example.com'
            },
            license: {
                name: 'MIT',
                url: 'https://opensource.org/licenses/MIT'
            }
        },
        servers: [
            {
                url: 'http://localhost:5000',
                description: 'Development Server'
            }
        ],
        tags: [
            {
                name: 'Todos',
                description: 'Todo management endpoints'
            },
            {
                name: 'Health',
                description: 'API health check'
            }
        ]
    },
    apis: ['./routes/*.js', './server.js']
};

const swaggerSpec = swaggerJsdoc(options);

module.exports = swaggerSpec;
