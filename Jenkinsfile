pipeline {
    agent any
    
    // GitHub-triggered pipeline - runs automatically on push
    triggers {
        githubPush()
    }
    
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
            }
        }
        stage('Build & Up') {
            steps {
                sh 'docker-compose build'
                sh 'docker-compose up -d server client'
            }
        }
        stage('Run Selenium Tests') {
            steps {
                sh 'mkdir -p tests/reports'
                // Force rebuild selenium-tests to get latest test files
                sh 'docker-compose build --no-cache selenium-tests'
                sh 'docker-compose run --rm -e APP_URL=http://client:80 -e HEADLESS=true selenium-tests'
            }
        }
    }
    
    post {
        always {
            script {
                node {
                    // Archive test reports
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'tests/reports',
                        reportFiles: 'test_report.html',
                        reportName: 'Selenium Test Report'
                    ])
                    // Only remove test container, keep app running!
                    sh 'docker-compose rm -f selenium-tests || true'
                    // Cleanup Docker
                    sh 'docker system prune -f || true'
                }
            }
        }
        success {
            echo '''
            ========================================
            ✅ PIPELINE SUCCESSFUL!
            ✅ All Selenium tests passed
            ✅ Check HTML report for details
            ========================================
            '''
            // Email notification on success to all contributors
            mail(
                to: 'ranadanyalarshad@gmail.com, aka.mdrana@gmail.com',
                subject: "✅ Build SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """Build Successful!

Job: ${env.JOB_NAME}
Build Number: #${env.BUILD_NUMBER}
Status: SUCCESS
Git Branch: ${env.GIT_BRANCH ?: 'main'}

Test Results: All Selenium tests passed!

View Build: ${env.BUILD_URL}
View Test Report: ${env.BUILD_URL}Selenium_20Test_20Report/

--
DevOps CI/CD Pipeline - Todo App
"""
            )
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
            
            // Email notification on failure to all contributors
            mail(
                to: 'ranadanyalarshad@gmail.com, aka.mdrana@gmail.com',
                subject: "❌ Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """Build Failed!

Job: ${env.JOB_NAME}
Build Number: #${env.BUILD_NUMBER}
Status: FAILED
Git Branch: ${env.GIT_BRANCH ?: 'main'}

Test Results: Some tests failed! Please check the test report.

View Build: ${env.BUILD_URL}
View Console: ${env.BUILD_URL}console
View Test Report: ${env.BUILD_URL}Selenium_20Test_20Report/

Action Required: Please investigate and fix the failing tests.

--
DevOps CI/CD Pipeline - Todo App
"""
            )
        }
    }
}
