#!/usr/bin/env groovy

// This pipeline uses standard parameters and intelligent payload creation.

pipeline {
    agent any

    parameters {
        password(
            name: 'X_API_KEY',
            defaultValue: '',
            description: '🔑 Your X-API-Key (required for authentication).'
        )
        choice(
            name: 'PURPOSE',
            choices: [
                '',
                'Onboard a new retailer or account',
                'Enable a new feature for an existing instance',
                'Blacklist a feature for an existing instance',
                'Activate an onboarded instance',
                'De-onboard a retailer',
                'Enable a new region for an existing instance',
                'Whitelabel a blacklisted feature'
            ],
            description: '🎯 Select the specific goal for your operation. The required fields will be used based on this choice.'
        )
        string(
            name: 'clientId',
            defaultValue: '',
            description: '<b>(Required for most operations)</b> The Client ID.'
        )
        string(
            name: 'instanceName',
            defaultValue: '',
            description: '<b>(Required for all operations)</b> The Instance Name.'
        )
        string(
            name: 'retailer',
            defaultValue: '',
            description: '<b>(Required for Onboarding, De-onboarding, etc.)</b> The retailer.'
        )
        string(
            name: 'retailerVariant',
            defaultValue: '',
            description: '<b>(Required for Onboarding, De-onboarding, etc.)</b> The retailer variant.'
        )
        string(
            name: 'region',
            defaultValue: '',
            description: '<b>(Required for Onboarding, Region Enablement, etc.)</b> The region.'
        )
        choice(
            name: 'productLine',
            choices: ['', 'RMM', 'ESM'],
            description: '<b>(Required for Onboarding, Feature changes, etc.)</b> The Product Line.'
        )
        string(
            name: 'features',
            defaultValue: '',
            description: '<b>(For Onboarding/Enabling multiple features)</b> Comma-separated list of features.'
        )
        string(
            name: 'feature',
            defaultValue: '',
            description: '<b>(For Whitelabeling a single feature)</b> The single feature name.'
        )
        string(
            name: 'enableDisableEntity',
            defaultValue: '',
            description: '<b>(For Activation/Deactivation)</b> The entity to act upon (e.g., INSTANCE, RETAILER).'
        )
        choice(
            name: 'activate',
            choices: ['true', 'false'],
            description: '<b>(For Activation/Deactivation)</b> Set to true or false.'
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
        stage('🔨 Build and Execute') {
            steps {
                script {
                    echo "--- Starting Operation for Purpose: ${params.PURPOSE} ---"
                    
                    if (params.PURPOSE.isEmpty()) {
                        error('You must select a Purpose for the operation.')
                    }

                    env.API_PAYLOAD = buildPayload()
                    echo "Final Payload:\n${prettyPrintJson(env.API_PAYLOAD)}"
                    
                    if (!params.DRY_RUN) {
                        executeAPICall()
                    } else {
                        echo "\n--- DRY RUN: API Call would be executed with the payload above ---"
                    }
                }
            }
        }
    }
    
    post {
        success {
            script {
                echo "✅ OPERATION COMPLETED SUCCESSFULLY"
            }
        }
        failure {
            script {
                echo "❌ OPERATION FAILED"
            }
        }
        always {
            script {
                archiveAuditLog()
            }
        }
    }
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

def buildPayload() {
    def payload = [
        user: "ops@commerceiq.ai",
        metadata: [
            executedBy: env.BUILD_USER ?: 'System',
            buildNumber: env.BUILD_NUMBER,
            timestamp: new Date().format("yyyy-MM-dd'T'HH:mm:ss'Z'")
        ]
    ]

    // Build payload based on the selected purpose
    switch (params.PURPOSE) {
        case 'Onboard a new retailer or account':
        case 'Enable a new feature for an existing instance':
        case 'Blacklist a feature for an existing instance':
            payload.clientId = params.clientId
            payload.instanceName = params.instanceName
            payload.retailer = params.retailer
            payload.retailerVariant = params.retailerVariant
            payload.region = params.region
            payload.productLine = params.productLine
            if (params.features) {
                payload.features = params.features.split(',').collect { it.trim() }
            }
            break

        case 'Activate an onboarded instance':
            payload.instanceName = params.instanceName
            payload.enableDisableEntity = params.enableDisableEntity
            payload.activate = params.activate.toBoolean()
            break

        case 'De-onboard a retailer':
            payload.instanceName = params.instanceName
            payload.enableDisableEntity = params.enableDisableEntity
            payload.region = params.region
            payload.retailer = params.retailer
            payload.retailerVariant = params.retailerVariant
            payload.activate = params.activate.toBoolean()
            break

        case 'Enable a new region for an existing instance':
            payload.clientId = params.clientId
            payload.instanceName = params.instanceName
            payload.retailer = params.retailer
            payload.retailerVariant = params.retailerVariant
            payload.region = params.region
            payload.productLine = params.productLine
            if (params.features) {
                payload.features = params.features.split(',').collect { it.trim() }
            }
            break

        case 'Whitelabel a blacklisted feature':
            payload.instanceName = params.instanceName
            payload.enableDisableEntity = params.enableDisableEntity
            payload.region = params.region
            payload.retailer = params.retailer
            payload.retailerVariant = params.retailerVariant
            payload.activate = params.activate.toBoolean()
            payload.clientId = params.clientId
            payload.productLine = params.productLine
            payload.feature = params.feature
            break
    }

    return payload
}

def executeAPICall() {
    def operation
    def onboardPurposes = [
        'Onboard a new retailer or account',
        'Enable a new feature for an existing instance',
        'Blacklist a feature for an existing instance'
    ]
    def activatePurposes = [
        'Activate an onboarded instance',
        'De-onboard a retailer',
        'Enable a new region for an existing instance',
        'Whitelabel a blacklisted feature'
    ]

    if (params.PURPOSE in onboardPurposes) {
        operation = 'onboardInstance'
    } else if (params.PURPOSE in activatePurposes) {
        operation = 'activateInstance'
    } else {
        error("Internal error: Cannot determine operation for purpose '${params.PURPOSE}'")
    }

    def endpoint = (operation == 'onboardInstance') ? '/common-auth/api/v1/instance/onboard' : '/common-auth/api/v1/instance/activate'
    env.API_ENDPOINT = "${env.API_BASE_URL}${endpoint}"

    echo "🚀 Executing API call to ${env.API_ENDPOINT}..."

    def maxRetries = env.RETRY_COUNT.toInteger()
    def retryCount = 0
    def lastError = null
    
    def apiKeyString = params.X_API_KEY.toString()

    while (retryCount < maxRetries) {
        if (retryCount > 0) {
            echo "🔄 Retry attempt ${retryCount + 1} of ${maxRetries}"
            sleep(time: (retryCount * 5), unit: 'SECONDS')
        }

        def response = httpRequest(
            url: env.API_ENDPOINT,
            httpMode: 'POST',
            contentType: 'APPLICATION_JSON',
            requestBody: groovy.json.JsonOutput.toJson(buildPayload()),
            customHeaders: [
                [name: 'X-API-Key', value: apiKeyString],
                [name: 'Content-Type', value: 'application/json']
            ],
            timeout: env.TIMEOUT_SECONDS.toInteger(),
            validResponseCodes: '100:599' // Accept all codes to handle manually
        )

        env.API_RESPONSE = response.content
        env.API_STATUS = response.status

        if (response.status >= 200 && response.status < 300) {
            echo "✅ Response Status: ${env.API_STATUS}"
            echo "📄 Raw Response: ${env.API_RESPONSE}"
            return
        } else {
            lastError = "Status: ${response.status}, Body: ${response.content}"
            echo "❌ API call failed. ${lastError}"
            retryCount++
        }
    }
    
    error("❌ All ${maxRetries} attempts failed. Last error: ${lastError}")
}

def prettyPrintJson(json) {
    try {
        def jsonString = (json instanceof String) ? json : groovy.json.JsonOutput.toJson(json)
        def jsonObj = readJSON text: jsonString
        return groovy.json.JsonOutput.prettyPrint(groovy.json.JsonOutput.toJson(jsonObj))
    } catch (Exception e) {
        return json.toString()
    }
}

def archiveAuditLog() {
    def auditLog = [
        buildNumber: env.BUILD_NUMBER,
        timestamp: new Date().format("yyyy-MM-dd'T'HH:mm:ss'Z'"),
        user: env.BUILD_USER ?: 'System',
        purpose: params.PURPOSE,
        parameters: params,
        result: currentBuild.result,
        duration: currentBuild.durationString,
        apiEndpoint: env.API_ENDPOINT,
        apiStatus: env.API_STATUS,
        apiResponse: env.API_RESPONSE
    ]
    
    writeJSON file: "audit-log-${env.BUILD_NUMBER}.json", json: auditLog, pretty: 4
    archiveArtifacts artifacts: "audit-log-${env.BUILD_NUMBER}.json", allowEmptyArchive: true
}
