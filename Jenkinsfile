pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/LiLyTampone/Run_Movie.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest tests/
                '''
            }
        }

        stage('Deploy App') {
            steps {
                echo 'Deploying...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    nohup python app.py > output.log 2>&1 &
                '''
            }
        }
    }

    post {
        failure {
            echo "❌ Build failed"
        }
        success {
            echo "✅ App deployed successfully!"
        }
    }
}
