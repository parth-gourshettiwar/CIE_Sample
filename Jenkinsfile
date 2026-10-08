pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'devops-task-api:1.0'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies & Test') {
            steps {
                // Compatible with both Linux and Windows agents (using sh/bat if necessary)
                // For simplicity, assuming Linux-based Jenkins agent here
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                // Ensure kubectl context is set correctly before running this pipeline
                sh "kubectl apply -f k8s/deployment.yaml"
                sh "kubectl apply -f k8s/service.yaml"
                
                // Wait for deployment to succeed
                sh "kubectl rollout status deployment/devops-task-api"
            }
        }
    }
}
