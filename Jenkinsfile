pipeline {
    agent any
    
    environment {
        COMPOSE_PROJECT_NAME = 'todo-app'
        MONGO_URI = credentials('mongo-uri')  // Set in Jenkins Credentials
        JWT_SECRET = credentials('jwt-secret') // Set in Jenkins Credentials
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
                echo '✅ All Docker images built (server, client, tests)'
            }
        }
        
        stage('Start Application') {
            steps {
                // Start app containers
                sh 'docker-compose up -d server client'
                
                // Wait for services to be healthy
                sh '''
                    echo "Waiting for services to be ready..."
                    sleep 20
                    
                    # Check if containers are running
                    docker-compose ps
                '''
                echo '✅ Application started in containers'
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                // Run tests container
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
            // Archive test reports
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'tests/reports',
                reportFiles: 'test_report.html',
                reportName: 'Selenium Test Report'
            ])
            
            // Stop and remove all containers
            sh 'docker-compose down --remove-orphans || true'
            
            // Cleanup Docker
            sh 'docker system prune -f || true'
        }
        success {
            echo '''
            ========================================
            ✅ PIPELINE SUCCESSFUL!
            ✅ All Selenium tests passed
            ✅ Check HTML report for details
            ========================================
            '''
        }
        failure {
            echo '''
            ========================================
            ❌ PIPELINE FAILED!
            ❌ Check logs and test report
            ========================================
            '''
            // Show container logs on failure
            sh 'docker-compose logs || true'
        }
    }
}
