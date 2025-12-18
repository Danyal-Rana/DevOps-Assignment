pipeline {
    agent any
    
    // GitHub-triggered pipeline - runs automatically on push
    triggers {
        githubPush()
    }
    
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
                subject: "✅ Build SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Build Successful!</h2>
                    <p><b>Job:</b> ${env.JOB_NAME}</p>
                    <p><b>Build Number:</b> ${env.BUILD_NUMBER}</p>
                    <p><b>Status:</b> SUCCESS ✅</p>
                    <p><b>Build URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><b>Test Report:</b> <a href="${env.BUILD_URL}Selenium_20Test_20Report/">View Report</a></p>
                """,
                mimeType: 'text/html',
                recipientProviders: [
                    [$class: 'DevelopersRecipientProvider'],      // Committers
                    [$class: 'RequesterRecipientProvider'],       // Who triggered build
                    [$class: 'CulpritsRecipientProvider']         // All since last success
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
                subject: "❌ Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Build Failed!</h2>
                    <p><b>Job:</b> ${env.JOB_NAME}</p>
                    <p><b>Build Number:</b> ${env.BUILD_NUMBER}</p>
                    <p><b>Status:</b> FAILED ❌</p>
                    <p><b>Build URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><b>Console Output:</b> <a href="${env.BUILD_URL}console">View Logs</a></p>
                    <p>Please check the build logs for details.</p>
                """,
                mimeType: 'text/html',
                recipientProviders: [
                    [$class: 'DevelopersRecipientProvider'],      // Committers
                    [$class: 'RequesterRecipientProvider'],       // Who triggered build
                    [$class: 'CulpritsRecipientProvider']         // All since last success
                ]
            )
        }
    }
}
