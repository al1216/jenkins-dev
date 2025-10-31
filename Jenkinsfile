#!/usr/bin/env groovy

/**
 * Jenkins Pipeline for Client Setup Platform API Operations
 * This pipeline enables non-technical users to execute API operations via UI
 */

pipeline {
    agent any
    
    parameters {
        password(
            name: 'X_API_KEY',
            defaultValue: '',
            description: '🔑 Your X-API-Key (required for authentication). Contact DevOps if you don\'t have one.'
        )
        
        choice(
            name: 'OPERATION',
            choices: [
                'onboardInstance',
                'activateInstance',
                'deactivateInstance',
                'updateInstance'
            ],
            description: '🎯 Select the operation to perform'
        )
        
        string(
            name: 'INSTANCE_NAME',
            defaultValue: '',
            description: '📝 Instance name (e.g., walmart-prod-001). Use lowercase with hyphens.'
        )
        
        choice(
            name: 'REGION',
            choices: [
                'us-east-1',
                'us-west-1',
                'us-west-2',
                'eu-west-1',
                'ap-south-1'
            ],
            description: '🌍 Select AWS region'
        )
        
        choice(
            name: 'RETAILER',
            choices: [
                'walmart',
                'amazon',
                'target',
                'kroger',
                'instacart',
                'chewy',
                'costco',
                'samsclub',
                'other'
            ],
            description: '🏪 Select retailer'
        )
        
        choice(
            name: 'RETAILER_VARIANT',
            choices: [
                'walmart-us',
                'walmart-ca',
                'walmart-mx',
                'amazon-us',
                'amazon-uk',
                'amazon-de',
                'amazon-jp',
                'amazon-vendor-central',
                'amazon-seller-central',
                'target-us',
                'target-online',
                'target-store',
                'kroger-us',
                'kroger-delivery',
                'kroger-pickup',
                'instacart-us',
                'instacart-ca',
                'chewy-us',
                'chewy-pharmacy',
                'costco-us',
                'costco-ca',
                'costco-warehouse',
                'costco-online',
                'samsclub-us',
                'samsclub-plus',
                'samsclub-business',
                'custom-variant'
            ],
            description: '🔖 Select retailer variant'
        )
        
        choice(
            name: 'ACTIVATE',
            choices: ['true', 'false'],
            description: '⚡ Activate or deactivate the instance'
        )
        
        choice(
            name: 'ENABLE_DISABLE_ENTITY',
            choices: [
                'all',
                'data-ingestion',
                'reporting',
                'analytics',
                'alerts',
                'integrations',
                'api-access'
            ],
            description: '🔧 Entity to enable/disable'
        )
        
        booleanParam(
            name: 'DRY_RUN',
            defaultValue: false,
            description: '🔍 Dry run mode (preview without executing)'
        )
    }
    
    environment {
        API_BASE_URL = 'http://client-setup-platform.beta-dbx.commerceiq.ai'
        TIMEOUT_SECONDS = '30'
        RETRY_COUNT = '3'
    }
    
    stages {
        stage('🔍 Initialize') {
            steps {
                script {
                    echo """
╔═══════════════════════════════════════════════════════════════╗
║  CLIENT SETUP PLATFORM - INSTANCE OPERATION                   ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📋 Operation Details:                                        ║
║  ──────────────────────────────────────────────────────────  ║
║  API Key Provided  : ${params.X_API_KEY.toString() ? '✓ Yes (hidden)' : '✗ No'} ║
║  Operation Type    : ${params.OPERATION}                      ║
║  Instance Name     : ${params.INSTANCE_NAME}                  ║
║  Region           : ${params.REGION}                          ║
║  Retailer         : ${params.RETAILER}                        ║
║  Retailer Variant : ${params.RETAILER_VARIANT}               ║
║  Activate         : ${params.ACTIVATE}                        ║
║  Entity           : ${params.ENABLE_DISABLE_ENTITY}           ║
║  Dry Run          : ${params.DRY_RUN}                         ║
║                                                               ║
║  Executed by      : ${env.BUILD_USER ?: 'System'}            ║
║  Build Number     : #${env.BUILD_NUMBER}                      ║
║  Timestamp        : ${new Date()}                             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
                    """
                }
            }
        }
        
        stage('✅ Validate Parameters') {
            steps {
                script {
                    echo "🔍 Validating input parameters..."
                    validateInputs()
                    echo "✅ All parameters are valid"
                }
            }
        }
        
        stage('🔨 Build API Request') {
            steps {
                script {
                    echo "🔨 Building API request..."
                    
                    // Build endpoint
                    env.API_ENDPOINT = buildEndpoint(params.OPERATION)
                    echo "📍 Endpoint: ${env.API_ENDPOINT}"
                    
                    // Build payload
                    env.API_PAYLOAD = buildPayload()
                    echo """
📦 Payload:
${prettyPrintJson(env.API_PAYLOAD)}
                    """
                }
            }
        }
        
        stage('🚀 Execute API Call') {
            when {
                expression { return !params.DRY_RUN }
            }
            steps {
                script {
                    echo "🚀 Executing API call..."
                    executeAPICall()
                }
            }
        }
        
        stage('🔍 Dry Run Summary') {
            when {
                expression { return params.DRY_RUN }
            }
            steps {
                script {
                    echo """
╔═══════════════════════════════════════════════════════════════╗
║  🔍 DRY RUN MODE - NO API CALL EXECUTED                       ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  The following API call would be executed:                   ║
║                                                               ║
║  URL: ${env.API_ENDPOINT}                                     ║
║  Method: POST                                                 ║
║  Payload: (see above)                                         ║
║                                                               ║
║  To execute for real, uncheck "Dry Run" option               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
                    """
                }
            }
        }
        
        stage('📊 Display Results') {
            when {
                expression { return !params.DRY_RUN }
            }
            steps {
                script {
                    displayResults()
                }
            }
        }
    }
    
    post {
        success {
            script {
                echo """
╔═══════════════════════════════════════════════════════════════╗
║  ✅ OPERATION COMPLETED SUCCESSFULLY                          ║
╚═══════════════════════════════════════════════════════════════╝
                """
                notifySuccess()
            }
        }
        
        failure {
            script {
                echo """
╔═══════════════════════════════════════════════════════════════╗
║  ❌ OPERATION FAILED                                          ║
║                                                               ║
║  Please check the console output above for error details.    ║
║  Contact DevOps team if you need assistance.                 ║
╚═══════════════════════════════════════════════════════════════╝
                """
                notifyFailure()
            }
        }
        
        always {
            script {
                // Archive artifacts and logs
                archiveAuditLog()
            }
        }
    }
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

def validateInputs() {
    // Validate X-API-Key
    def apiKey = params.X_API_KEY.toString()
    if (apiKey.trim().isEmpty()) {
        error("❌ X-API-Key is required! Please provide your API key. Contact DevOps if you don't have one.")
    }
    
    if (apiKey.length() < 10) {
        error("❌ X-API-Key appears to be invalid (too short). Please check your API key.")
    }
    
    // Validate instance name
    if (!params.INSTANCE_NAME || params.INSTANCE_NAME.trim().isEmpty()) {
        error("❌ Instance name is required!")
    }
    
    if (!params.INSTANCE_NAME.matches(/^[a-zA-Z0-9-_]+$/)) {
        error("❌ Instance name can only contain alphanumeric characters, hyphens, and underscores")
    }
    
    if (params.INSTANCE_NAME.length() < 3 || params.INSTANCE_NAME.length() > 50) {
        error("❌ Instance name must be between 3 and 50 characters")
    }
    
    // Validate retailer variant matches retailer
    def retailerPrefix = params.RETAILER_VARIANT.split('-')[0]
    if (retailerPrefix != params.RETAILER && params.RETAILER_VARIANT != 'custom-variant') {
        echo "⚠️  Warning: Retailer variant '${params.RETAILER_VARIANT}' may not match retailer '${params.RETAILER}'"
    }
}

def buildEndpoint(operation) {
    def endpoints = [
        'onboardInstance': '/common-auth/api/v1/instance/onboard',
        'activateInstance': '/common-auth/api/v1/instance/activate',
        'deactivateInstance': '/common-auth/api/v1/instance/deactivate',
        'updateInstance': '/common-auth/api/v1/instance/update'
    ]
    
    def path = endpoints[operation]
    if (!path) {
        error("❌ Unknown operation: ${operation}")
    }
    
    return "${env.API_BASE_URL}${path}"
}

def buildPayload() {
    def payload = [
        instanceName: params.INSTANCE_NAME,
        region: params.REGION,
        retailer: params.RETAILER,
        retailerVariant: params.RETAILER_VARIANT,
        activate: params.ACTIVATE.toBoolean(),
        enableDisableEntity: params.ENABLE_DISABLE_ENTITY,
        user: "ops@commerceiq.ai",
        metadata: [
            executedBy: env.BUILD_USER ?: 'System',
            buildNumber: env.BUILD_NUMBER,
            timestamp: new Date().format("yyyy-MM-dd'T'HH:mm:ss'Z'")
        ]
    ]
    
    return groovy.json.JsonOutput.toJson(payload)
}

def executeAPICall() {
    def maxRetries = env.RETRY_COUNT.toInteger()
    def retryCount = 0
    def lastError = null
    
    // Convert the secret to a string to avoid issues with the httpRequest plugin
    def apiKeyString = params.X_API_KEY.toString()

    while (retryCount < maxRetries) {
        try {
            if (retryCount > 0) {
                echo "🔄 Retry attempt ${retryCount} of ${maxRetries}"
                sleep(time: retryCount * 5, unit: 'SECONDS')
            }
            
            def response = httpRequest(
                url: env.API_ENDPOINT,
                httpMode: 'POST',
                contentType: 'APPLICATION_JSON',
                requestBody: env.API_PAYLOAD,
                customHeaders: [
                    [name: 'X-API-Key', value: apiKeyString],
                    [name: 'Content-Type', value: 'application/json']
                ],
                timeout: env.TIMEOUT_SECONDS.toInteger(),
                validResponseCodes: '200:299',
                ignoreSslErrors: true
            )
            
            env.API_RESPONSE = response.content
            env.API_STATUS = response.status
            
            echo "✅ Response Status: ${env.API_STATUS}"
            
            return // Success, exit retry loop
            
        } catch (Exception e) {
            lastError = e
            retryCount++
            
            echo "❌ API call failed: ${e.message}"
            
            if (retryCount >= maxRetries) {
                error("❌ All ${maxRetries} attempts failed. Last error: ${e.message}")
            }
        }
    }
}

def displayResults() {
    try {
        def responseJson = readJSON text: env.API_RESPONSE
        
        echo """
╔═══════════════════════════════════════════════════════════════╗
║  📊 OPERATION RESULTS                                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Status Code      : ${env.API_STATUS}                         ║
║  Status           : ${responseJson.status ?: 'Success'}       ║
║  Message          : ${responseJson.message ?: 'Completed'}    ║
║                                                               ║
║  Instance Details:                                            ║
║  ──────────────────────────────────────────────────────────  ║
║  Instance ID      : ${responseJson.instanceId ?: 'N/A'}       ║
║  Instance Name    : ${params.INSTANCE_NAME}                   ║
║  Region           : ${params.REGION}                          ║
║  Retailer         : ${params.RETAILER}                        ║
║  Status           : ${responseJson.instanceStatus ?: 'N/A'}   ║
║                                                               ║
║  Execution Info:                                              ║
║  ──────────────────────────────────────────────────────────  ║
║  Timestamp        : ${new Date()}                             ║
║  Executed By      : ${env.BUILD_USER ?: 'System'}            ║
║  Build Number     : #${env.BUILD_NUMBER}                      ║
║  Duration         : ${currentBuild.durationString}            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Full Response:
${prettyPrintJson(env.API_RESPONSE)}
        """
    } catch (Exception e) {
        echo "📄 Raw Response: ${env.API_RESPONSE}"
    }
}

def prettyPrintJson(jsonString) {
    try {
        def json = readJSON text: jsonString
        return groovy.json.JsonOutput.prettyPrint(groovy.json.JsonOutput.toJson(json))
    } catch (Exception e) {
        return jsonString
    }
}

def notifySuccess() {
    // Email notification
    emailext(
        subject: "✅ Client Setup: ${params.OPERATION} - SUCCESS",
        body: """
Hello,

Your Client Setup Platform operation has completed successfully!

Operation Details:
- Operation: ${params.OPERATION}
- Instance: ${params.INSTANCE_NAME}
- Region: ${params.REGION}
- Retailer: ${params.RETAILER}
- Executed by: ${env.BUILD_USER ?: 'System'}

Build URL: ${env.BUILD_URL}

Thanks,
Jenkins Automation
        """,
        to: "${env.BUILD_USER_EMAIL}",
        mimeType: 'text/plain'
    )
    
    // Slack notification (if configured)
    try {
        slackSend(
            channel: '#client-setup-notifications',
            color: 'good',
            message: "✅ *${params.OPERATION}* completed successfully for instance `${params.INSTANCE_NAME}` by ${env.BUILD_USER ?: 'System'}"
        )
    } catch (Exception e) {
        echo "Slack notification skipped: ${e.message}"
    }
}

def notifyFailure() {
    emailext(
        subject: "❌ Client Setup: ${params.OPERATION} - FAILED",
        body: """
Hello,

Your Client Setup Platform operation has failed.

Operation Details:
- Operation: ${params.OPERATION}
- Instance: ${params.INSTANCE_NAME}
- Region: ${params.REGION}
- Retailer: ${params.RETAILER}
- Executed by: ${env.BUILD_USER ?: 'System'}

Please check the build logs for details:
${env.BUILD_URL}console

Contact DevOps team if you need assistance.

Thanks,
Jenkins Automation
        """,
        to: "${env.BUILD_USER_EMAIL}",
        mimeType: 'text/plain'
    )
    
    // Slack notification (if configured)
    try {
        slackSend(
            channel: '#client-setup-alerts',
            color: 'danger',
            message: "❌ *${params.OPERATION}* failed for instance `${params.INSTANCE_NAME}` by ${env.BUILD_USER ?: 'System'}. <${env.BUILD_URL}|View Logs>"
        )
    } catch (Exception e) {
        echo "Slack notification skipped: ${e.message}"
    }
}

def archiveAuditLog() {
    def auditLog = [
        buildNumber: env.BUILD_NUMBER,
        timestamp: new Date().format("yyyy-MM-dd'T'HH:mm:ss'Z'"),
        user: env.BUILD_USER ?: 'System',
        userEmail: env.BUILD_USER_EMAIL ?: 'N/A',
        operation: params.OPERATION,
        parameters: [
            instanceName: params.INSTANCE_NAME,
            region: params.REGION,
            retailer: params.RETAILER,
            retailerVariant: params.RETAILER_VARIANT,
            activate: params.ACTIVATE,
            enableDisableEntity: params.ENABLE_DISABLE_ENTITY,
            dryRun: params.DRY_RUN
        ],
        result: currentBuild.result,
        duration: currentBuild.durationString,
        apiEndpoint: env.API_ENDPOINT,
        apiStatus: env.API_STATUS
    ]
    
    writeJSON file: "audit-log-${env.BUILD_NUMBER}.json", json: auditLog, pretty: 4
    archiveArtifacts artifacts: "audit-log-${env.BUILD_NUMBER}.json", allowEmptyArchive: true
}
