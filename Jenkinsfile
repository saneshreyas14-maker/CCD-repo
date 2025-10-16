pipeline {
    agent any

    options {
        // Set a build timeout
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
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
                # Start the API in background and write PID to file
                $p = Start-Process -FilePath python -ArgumentList 'app.py' -PassThru
                $p.Id | Out-File -FilePath api.pid -Encoding ascii
                Start-Sleep -Seconds 3
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
            # Stop the background API process if it exists
            if (Test-Path api.pid) {
                $id = Get-Content api.pid | Out-String
                $id = $id.Trim()
                if ($id -match '\\d+') {
                    try {
                        Stop-Process -Id $id -ErrorAction SilentlyContinue
                        Write-Host "Stopped API process $id"
                    } catch {
                        Write-Host "Failed to stop process $id"
                    }
                }
                Remove-Item api.pid -ErrorAction SilentlyContinue
            }
            '''
        }
    }
}
