pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        PIP = 'C:\\Users\\DELL\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pip.exe'
        VENV_DIR = '.venv'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/LiLyTampone/Run_Movie.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                bat """
                    "%PYTHON%" -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate.bat
                    %VENV_DIR%\\Scripts\\pip.exe install --upgrade pip
                    %VENV_DIR%\\Scripts\\pip.exe install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                    call %VENV_DIR%\\Scripts\\activate.bat
                    %VENV_DIR%\\Scripts\\pytest.exe tests/
                """
            }
        }

        stage('Deploy App') {
            steps {
                echo 'Deploying...'
                bat """
                    call %VENV_DIR%\\Scripts\\activate.bat
                    start /b %VENV_DIR%\\Scripts\\python.exe app.py
                """
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
