pipeline {
    agent any

    parameters {
        string(
            name: 'DEPLOY_URL',
            defaultValue: 'http://stc21.webredirect.himshang.com.np',
            description: 'URL of the deployed application to test'
        )
        string(
            name: 'BUILD_VERSION',
            defaultValue: 'latest',
            description: 'Build version or number being tested'
        )
        choice(
            name: 'TEST_SUITE',
            choices: ['login', 'all'],
            description: 'Which tests to run'
        )
    }

    environment {
        HEADLESS = 'true'
        PYTHONUNBUFFERED = '1'
        TEST_URL = "${params.DEPLOY_URL}"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        stage('📋 Environment Info') {
            steps {
                script {
                    echo "=========================================="
                    echo "QA Test Pipeline Started"
                    echo "=========================================="
                    echo "Build Number:     ${env.BUILD_NUMBER}"
                    echo "Test Suite:       ${params.TEST_SUITE}"
                    echo "Deploy URL:       ${params.DEPLOY_URL}"
                    echo "Build Version:    ${params.BUILD_VERSION}"
                    echo "Headless Mode:    ${env.HEADLESS}"
                    echo "Workspace:        ${env.WORKSPACE}"
                    echo "=========================================="

                    sh '''
                        echo "Python version: $(python3 --version)"
                        echo "Pip version:    $(pip3 --version)"
                    '''
                }
            }
        }

        stage('🔧 Setup Python Environment') {
            steps {
                script {
                    echo "Setting up Python virtual environment..."
                    sh '''
                        set -e
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip -q
                        pip install -r requirements.txt -q
                        echo "✅ Virtual environment and dependencies installed"
                    '''
                }
            }
        }

        stage('🌐 Install Playwright Browsers') {
            steps {
                script {
                    echo "Installing Playwright browsers..."
                    sh '''
                        set -e
                        . venv/bin/activate
                        playwright install chromium
                        echo "✅ Chromium browser installed"
                    '''
                }
            }
        }

        stage('🧪 Run QA Tests') {
            steps {
                script {
                    echo "Running QA tests against: ${params.DEPLOY_URL}"
                    sh '''
                        set -e
                        . venv/bin/activate
                        
                        # Create allure results directory
                        mkdir -p allure-results
                        rm -rf allure-results/*
                        
                        # Run tests based on suite selection
                        if [ "${TEST_SUITE}" = "login" ]; then
                            echo "Running Login Test..."
                            HEADLESS=true pytest Tests/Test_login.py -v --alluredir=allure-results --html=test-report.html --self-contained-html || TEST_EXIT_CODE=$?
                        else
                            echo "Running All Tests..."
                            HEADLESS=true pytest Tests/ -v --alluredir=allure-results --html=test-report.html --self-contained-html || TEST_EXIT_CODE=$?
                        fi
                        
                        echo "Test execution completed"
                        exit ${TEST_EXIT_CODE:-0}
                    '''
                }
            }
        }

        stage('📊 Generate Allure Report') {
            steps {
                script {
                    sh '''
                        set -e
                        . venv/bin/activate
                        
                        # Check if allure-results has data
                        if [ -d "allure-results" ] && [ "$(ls -A allure-results)" ]; then
                            echo "Allure results found, generating report..."
                            # Try to use allure CLI if available
                            if command -v allure &> /dev/null; then
                                allure generate allure-results -o allure-report --clean
                                echo "✅ Allure HTML report generated"
                            else
                                echo "⚠️  Allure CLI not available, but test results are in JSON format"
                            fi
                        else
                            echo "⚠️  No test results found"
                        fi
                    '''
                }
            }
        }

        stage('📈 Test Summary') {
            steps {
                script {
                    sh '''
                        set -e
                        
                        cat > test-summary.txt << 'EOF'
========================================
QA Test Execution Summary
========================================
Build Number:        ${BUILD_NUMBER}
Date:                $(date)
Test Suite:          ${TEST_SUITE}
Deploy URL:          ${DEPLOY_URL}
Build Version:       ${BUILD_VERSION}
Headless Mode:       ${HEADLESS}

Test Results:
-----------
EOF
                        
                        # Parse pytest results if available
                        if [ -f ".pytest_cache/.pytest.json" ]; then
                            cat .pytest_cache/.pytest.json >> test-summary.txt
                        fi
                        
                        echo "Test Artifacts:" >> test-summary.txt
                        echo "- Allure Results: allure-results/" >> test-summary.txt
                        echo "- HTML Report: test-report.html" >> test-summary.txt
                        if [ -d "allure-report" ]; then
                            echo "- Allure Report: allure-report/" >> test-summary.txt
                        fi
                        echo "========================================" >> test-summary.txt
                        
                        cat test-summary.txt
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Archiving test artifacts..."
                // Archive Allure results
                archiveArtifacts artifacts: 'allure-results/**', 
                                 allowEmptyArchive: true
                
                // Archive HTML report
                archiveArtifacts artifacts: 'test-report.html',
                                 allowEmptyArchive: true
                
                // Archive Allure generated report if available
                archiveArtifacts artifacts: 'allure-report/**',
                                 allowEmptyArchive: true
                
                // Archive summary
                archiveArtifacts artifacts: 'test-summary.txt',
                                 allowEmptyArchive: true
                
                // Publish HTML report
                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'allure-report',
                    reportFiles: 'index.html',
                    reportName: 'Allure Test Report'
                ])
            }
        }

        success {
            echo "✅ QA Tests Passed!"
            echo "Deploy URL: ${DEPLOY_URL}"
            echo "Build Version: ${BUILD_VERSION}"
        }

        failure {
            echo "❌ QA Tests Failed!"
            echo "Review test-report.html for details"
            echo "Check allure-results for test data"
        }
    }
}
