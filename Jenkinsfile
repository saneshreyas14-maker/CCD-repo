pipeline {
    agent { label 'windows' }

    options {
        // Limit total runtime of the build
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install deps') {
            steps {
                powershell '''
                python -m pip install --upgrade pip
                python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Start API') {
            steps {
                powershell '''
                # Start the API in background and write its PID to api.pid
                $p = Start-Process -FilePath "python" -ArgumentList "app.py" -PassThru
                $p.Id | Out-File -FilePath "api.pid" -Encoding ascii
                Start-Sleep -Seconds 2
                Get-Content api.pid
                '''
            }
        }

        stage('Run Tests') {
            steps {
                powershell '''
                python -m pytest -q
                exit $LASTEXITCODE
                '''
            }
        }
    }

    post {
        always {
            powershell '''
            if (Test-Path "api.pid") {
                $id = Get-Content "api.pid" | Out-String
                $id = $id.Trim()
                if ($id -match "\\d+") {
                    try {
                        Stop-Process -Id $id -ErrorAction SilentlyContinue
                        Write-Host "Stopped API process with ID $id"
                    } catch {
                        Write-Host "Failed to stop process $id"
                    }
                }
                Remove-Item "api.pid" -ErrorAction SilentlyContinue
            }
            '''
        }
    }
}
