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
                    // Stop and remove all containers
                    sh 'docker-compose down --remove-orphans || true'
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
            // Email notification on success to all collaborators
            emailext(
                to: 'ranadanyalarshad@gmail.com',
                subject: "✅ Build SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <div style="background: linear-gradient(135deg, #28a745, #20c997); padding: 20px; border-radius: 10px 10px 0 0;">
                            <h1 style="color: white; margin: 0;">✅ Build Successful!</h1>
                        </div>
                        <div style="background: #f8f9fa; padding: 20px; border: 1px solid #dee2e6;">
                            <h3 style="color: #28a745;">Pipeline Summary</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr><td style="padding: 8px; border-bottom: 1px solid #dee2e6;"><b>Job:</b></td><td style="padding: 8px; border-bottom: 1px solid #dee2e6;">${env.JOB_NAME}</td></tr>
                                <tr><td style="padding: 8px; border-bottom: 1px solid #dee2e6;"><b>Build Number:</b></td><td style="padding: 8px; border-bottom: 1px solid #dee2e6;">#${env.BUILD_NUMBER}</td></tr>
                                <tr><td style="padding: 8px; border-bottom: 1px solid #dee2e6;"><b>Status:</b></td><td style="padding: 8px; border-bottom: 1px solid #dee2e6;"><span style="color: #28a745; font-weight: bold;">SUCCESS ✅</span></td></tr>
                                <tr><td style="padding: 8px; border-bottom: 1px solid #dee2e6;"><b>Git Branch:</b></td><td style="padding: 8px; border-bottom: 1px solid #dee2e6;">${env.GIT_BRANCH ?: 'main'}</td></tr>
                            </table>
                            
                            <h3 style="color: #28a745; margin-top: 20px;">🧪 Test Results</h3>
                            <p style="background: #d4edda; padding: 15px; border-radius: 5px; color: #155724;">
                                <b>All Selenium tests passed successfully!</b><br>
                                View the detailed test report for more information.
                            </p>
                            
                            <h3 style="color: #333; margin-top: 20px;">🔗 Quick Links</h3>
                            <p>
                                <a href="${env.BUILD_URL}" style="display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin-right: 10px;">View Build</a>
                                <a href="${env.BUILD_URL}Selenium_20Test_20Report/" style="display: inline-block; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 5px;">View Test Report</a>
                            </p>
                        </div>
                        <div style="background: #343a40; padding: 15px; border-radius: 0 0 10px 10px; text-align: center;">
                            <p style="color: #adb5bd; margin: 0; font-size: 12px;">DevOps CI/CD Pipeline - Todo App</p>
                        </div>
                    </div>
                """,
                mimeType: 'text/html',
                attachLog: false,
                recipientProviders: [
                    [$class: 'DevelopersRecipientProvider'],
                    [$class: 'RequesterRecipientProvider'],
                    [$class: 'CulpritsRecipientProvider']
                ]
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
            
            // Email notification on failure to all collaborators
            emailext(
                to: 'ranadanyalarshad@gmail.com',
                subject: "❌ Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <div style="background: linear-gradient(135deg, #dc3545, #c82333); padding: 20px; border-radius: 10px 10px 0 0;">
                            <h1 style="color: white; margin: 0;">❌ Build Failed!</h1>
                        </div>
                        <div style="background: #f8f9fa; padding: 20px; border: 1px solid #dee2e6;">
                            <h3 style="color: #dc3545;">Pipeline Summary</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr><td style="padding: 8px; border-bottom: 1px solid #dee2e6;"><b>Job:</b></td><td style="padding: 8px; border-bottom: 1px solid #dee2e6;">${env.JOB_NAME}</td></tr>
                                <tr><td style="padding: 8px; border-bottom: 1px solid #dee2e6;"><b>Build Number:</b></td><td style="padding: 8px; border-bottom: 1px solid #dee2e6;">#${env.BUILD_NUMBER}</td></tr>
                                <tr><td style="padding: 8px; border-bottom: 1px solid #dee2e6;"><b>Status:</b></td><td style="padding: 8px; border-bottom: 1px solid #dee2e6;"><span style="color: #dc3545; font-weight: bold;">FAILED ❌</span></td></tr>
                                <tr><td style="padding: 8px; border-bottom: 1px solid #dee2e6;"><b>Git Branch:</b></td><td style="padding: 8px; border-bottom: 1px solid #dee2e6;">${env.GIT_BRANCH ?: 'main'}</td></tr>
                            </table>
                            
                            <h3 style="color: #dc3545; margin-top: 20px;">🧪 Test Results</h3>
                            <p style="background: #f8d7da; padding: 15px; border-radius: 5px; color: #721c24;">
                                <b>Some tests failed!</b><br>
                                Please check the test report and console logs for details on what went wrong.
                            </p>
                            
                            <h3 style="color: #333; margin-top: 20px;">🔗 Quick Links</h3>
                            <p>
                                <a href="${env.BUILD_URL}" style="display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin-right: 10px;">View Build</a>
                                <a href="${env.BUILD_URL}console" style="display: inline-block; padding: 10px 20px; background: #dc3545; color: white; text-decoration: none; border-radius: 5px; margin-right: 10px;">View Console</a>
                                <a href="${env.BUILD_URL}Selenium_20Test_20Report/" style="display: inline-block; padding: 10px 20px; background: #6c757d; color: white; text-decoration: none; border-radius: 5px;">View Test Report</a>
                            </p>
                            
                            <h3 style="color: #856404; margin-top: 20px;">⚠️ Action Required</h3>
                            <p style="background: #fff3cd; padding: 15px; border-radius: 5px; color: #856404;">
                                Please investigate and fix the failing tests. Check the console output for stack traces and error messages.
                            </p>
                        </div>
                        <div style="background: #343a40; padding: 15px; border-radius: 0 0 10px 10px; text-align: center;">
                            <p style="color: #adb5bd; margin: 0; font-size: 12px;">DevOps CI/CD Pipeline - Todo App</p>
                        </div>
                    </div>
                """,
                mimeType: 'text/html',
                attachLog: true,
                recipientProviders: [
                    [$class: 'DevelopersRecipientProvider'],
                    [$class: 'RequesterRecipientProvider'],
                    [$class: 'CulpritsRecipientProvider']
                ]
            )
        }
    }
}
