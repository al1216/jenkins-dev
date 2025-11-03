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
                'activateInstance'
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
                '',
                'FR',
                'IE',
                'IT',
                'MX',
                'UK',
                'US'
            ],
            description: '🌍 Select AWS region (or leave blank for none)'
        )

        choice(
            name: 'RETAILER',
            choices: [
                '',
                'ahold',
                'albertsons',
                'amazon',
                'bestbuy',
                'chewy',
                'costco',
                'cvs',
                'fresh',
                'gopuff',
                'hyvee',
                'instacart',
                'kroger',
                'meijer',
                'omni',
                'overstock',
                'samsclub',
                'shipt',
                'shoprite',
                'target',
                'ubereats',
                'walgreen',
                'walmart',
                'wayfair'
            ],
            description: '🏪 Select retailer (or leave blank for none)'
        )

        choice(
            name: 'RETAILER_VARIANT',
            choices: [
                '',
                '3P',
                'api',
                'business',
                'citrus',
                'criteo',
                'direct',
                'fresh',
                'hybrid',
                'kevel',
                'native',
                'promoteiq',
                'retail',
                'retailer',
                'rms'
            ],
            description: '🔖 Select retailer variant (or leave blank for none)'
        )

        choice(
            name: 'PRODUCT_LINE',
            choices: ['', 'RMM', 'ESM'],
            description: '📦 Select the product line (or leave blank for none)'
        )

        string(
            name: 'FEATURE',
            defaultValue: '',
            description: '✨ Single feature to enable (e.g., rmm_base)'
        )

        string(
            name: 'FEATURES',
            defaultValue: '',
            description: '✨ Multiple features to enable (comma-separated list, e.g., rmm_base,rmm_dsp)'
        )

        choice(
            name: 'ACTIVATE',
            choices: ['', 'true', 'false'],
            description: '⚡ Activate or deactivate the instance (or leave blank for none)'
        )

        choice(
            name: 'ENABLE_DISABLE_ENTITY',
            choices: [
                '',
                'CLIENT',
                'FEATURE',
                'INSTANCE',
                'REGION',
                'RETAILER'
            ],
            description: '🔧 Entity to enable/disable (or leave blank for none)'
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
║  Region           : ${params.REGION ?: 'N/A'}                          ║
║  Retailer         : ${params.RETAILER ?: 'N/A'}                        ║
║  Retailer Variant : ${params.RETAILER_VARIANT ?: 'N/A'}               ║
║  Product Line     : ${params.PRODUCT_LINE ?: 'N/A'}                  ║
║  Feature          : ${params.FEATURE ?: 'N/A'}                       ║
║  Features         : ${params.FEATURES ?: 'N/A'}                      ║
║  Activate         : ${params.ACTIVATE ?: 'N/A'}                        ║
║  Entity           : ${params.ENABLE_DISABLE_ENTITY ?: 'N/A'}           ║
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

    // Validate retailer variant matches retailer only if both are provided
    if (params.RETAILER_VARIANT && params.RETAILER) {
        def retailerPrefix = params.RETAILER_VARIANT.split('-')[0]
        if (retailerPrefix != params.RETAILER && params.RETAILER_VARIANT != 'custom-variant') {
            echo "⚠️  Warning: Retailer variant '${params.RETAILER_VARIANT}' may not match retailer '${params.RETAILER}'"
        }
    }
}

def buildEndpoint(operation) {
    def endpoints = [
        'onboardInstance': '/common-auth/api/v1/instance/onboard',
        'activateInstance': '/common-auth/api/v1/instance/activate'
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
        user: "ops@commerceiq.ai",
        metadata: [
            executedBy: env.BUILD_USER ?: 'System',
            buildNumber: env.BUILD_NUMBER,
            timestamp: new Date().format("yyyy-MM-dd'T'HH:mm:ss'Z'")
        ]
    ]

    if (params.REGION) {
        payload.region = params.REGION
    }
    if (params.RETAILER) {
        payload.retailer = params.RETAILER
    }
    if (params.RETAILER_VARIANT) {
        payload.retailerVariant = params.RETAILER_VARIANT
    }
    if (params.PRODUCT_LINE) {
        payload.productLine = params.PRODUCT_LINE
    }
    if (params.FEATURE) {
        payload.feature = params.FEATURE.trim()
    }
    if (params.FEATURES) {
        payload.features = params.FEATURES.split(',').collect { it.trim() }
    }
    if (params.ACTIVATE) {
        payload.activate = params.ACTIVATE.toBoolean()
    }
    if (params.ENABLE_DISABLE_ENTITY) {
        payload.enableDisableEntity = params.ENABLE_DISABLE_ENTITY
    }

    return groovy.json.JsonOutput.toJson(payload)
}

def executeAPICall() {
    def maxRetries = env.RETRY_COUNT.toInteger()
    def retryCount = 0
    def lastError = null

    // Convert the secret to a string to avoid issues with the httpRequest plugin
    def apiKeyString = params.X_API_KEY.toString()

    while (retryCount < maxRetries) {
        if (retryCount > 0) {
            echo "🔄 Retry attempt ${retryCount + 1} of ${maxRetries}"
            sleep(time: (retryCount * 5), unit: 'SECONDS')
        }

        // Tell the plugin to consider all HTTP status codes as valid
        // so we can handle the response manually.
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
            validResponseCodes: '100:599', // Accept all codes
            ignoreSslErrors: true
        )

        env.API_RESPONSE = response.content
        env.API_STATUS = response.status

        // Manually check for a successful status code
        if (response.status >= 200 && response.status < 300) {
            echo "✅ Response Status: ${env.API_STATUS}"
            return // Success, exit the function
        } else {
            // This is a logical failure, not a plugin failure
            lastError = "Status: ${response.status}, Body: ${response.content}"
            echo "❌ API call failed. ${lastError}"
            retryCount++
        }
    }

    // If all retries fail, stop the build
    error("❌ All ${maxRetries} attempts failed. Last error: ${lastError}")
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