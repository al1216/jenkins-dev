#!/usr/bin/env groovy

import groovy.json.JsonOutput

// ============================================================================
// Jenkinsfile: Intelligent Client Setup Platform Automation
// ============================================================================

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
                'Whitelabel a blacklisted feature',
                'Disable a module'
            ],
            description: '🎯 Select the specific goal for your operation.'
        )
        string(name: 'clientId', defaultValue: '', description: 'The Client ID (required for most operations).')
        string(name: 'instanceName', defaultValue: '', description: 'The Instance Name (required for all operations).')
        choice(
            name: 'retailer',
            choices: [
                '', 'ahold', 'albertsons', 'amazon', 'bestbuy', 'chewy', 'costco', 'cvs',
                'fresh', 'gopuff', 'hyvee', 'instacart', 'kroger', 'meijer', 'omni',
                'overstock', 'samsclub', 'shipt', 'shoprite', 'target', 'ubereats',
                'walgreen', 'walmart', 'wayfair'
            ],
            description: 'Select the retailer (for onboarding, de-onboarding, etc.).'
        )
        choice(
            name: 'retailerVariant',
            choices: [
                '', '3P', 'api', 'business', 'citrus', 'criteo', 'direct', 'fresh',
                'hybrid', 'kevel', 'native', 'promoteiq', 'retail', 'retailer', 'rms'
            ],
            description: 'Select the retailer variant.'
        )
        choice(
            name: 'region',
            choices: ['', 'CA', 'FR', 'GB', 'IE', 'IT', 'MX', 'UK', 'US'],
            description: 'Select the region (for onboarding, region enablement, etc.).'
        )
        choice(
            name: 'productLine',
            choices: ['', 'RMM', 'ESM'],
            description: 'Product Line (required for onboarding/feature changes).'
        )
        string(name: 'features', defaultValue: '', description: 'Comma-separated list of features (for onboarding/enabling/blacklisting multiple).')
        string(name: 'feature', defaultValue: '', description: 'Single feature name (for white labeling/disable module a single feature).')
        choice(
            name: 'enableDisableEntity',
            choices: ['', 'CLIENT', 'FEATURE', 'INSTANCE', 'REGION', 'RETAILER'],
            description: '(For Activation/Deactivation) Select the entity.'
        )
        choice(
            name: 'activate',
            choices: ['true', 'false'],
            description: '(For Activation/Deactivation) Set to true or false.'
        )
        booleanParam(
            name: 'DRY_RUN',
            defaultValue: false,
            description: '🔍 Dry run mode (preview without executing).'
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

                    // ✅ Build the payload as a Groovy map (NOT stored in env)
                    def payload = buildPayload()
                    echo "Final Payload:\n${prettyPrintJson(payload)}"

                    if (!params.DRY_RUN) {
                        executeAPICall(payload)
                    } else {
                        echo "\n--- DRY RUN: API Call would be executed with the payload above ---"
                    }

                    archiveAuditLog(payload)
                }
            }
        }
    }

    post {
        success {
            echo "✅ OPERATION COMPLETED SUCCESSFULLY"
        }
        failure {
            echo "❌ OPERATION FAILED"
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

    switch (params.PURPOSE) {
        case 'Onboard a new retailer or account':
        case 'Enable a new feature for an existing instance':
        case 'Blacklist a feature for an existing instance':
            payload.clientId = params.clientId.toInteger()
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
            payload.clientId = params.clientId.toInteger()
            payload.instanceName = params.instanceName
            payload.enableDisableEntity = params.enableDisableEntity
            payload.activate = params.activate.toBoolean()
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
            payload.clientId = params.clientId.toInteger()
            payload.productLine = params.productLine
            payload.feature = params.feature
            break

        case 'Disable a module':
            payload.instanceName = params.instanceName
            payload.enableDisableEntity = params.enableDisableEntity
            payload.clientId = params.clientId.toInteger()
            payload.region = params.region
            payload.retailer = params.retailer
            payload.retailerVariant = params.retailerVariant
            payload.productLine = params.productLine
            payload.feature = params.feature
            payload.activate = params.activate.toBoolean()
            break
    }

    return payload
}

def executeAPICall(payload) {
    def onboardPurposes = [
        'Onboard a new retailer or account',
        'Enable a new feature for an existing instance',
        'Blacklist a feature for an existing instance'
    ]
    def activatePurposes = [
        'Activate an onboarded instance',
        'De-onboard a retailer',
        'Enable a new region for an existing instance',
        'Whitelabel a blacklisted feature',
        'Disable a module'
    ]

    def operation
    if (params.PURPOSE in onboardPurposes) {
        operation = 'onboardInstance'
    } else if (params.PURPOSE in activatePurposes) {
        operation = 'activateInstance'
    } else {
        error("Internal error: Cannot determine operation for purpose '${params.PURPOSE}'")
    }

    def endpoint = (operation == 'onboardInstance')
        ? '/common-auth/api/v1/instance/onboard'
        : '/common-auth/api/v1/instance/activate-deactivate'

    def fullUrl = "${env.API_BASE_URL}${endpoint}"

    echo "🚀 Executing API call to ${fullUrl}..."

    def maxRetries = env.RETRY_COUNT.toInteger()
    def retryCount = 0
    def lastError = null

    while (retryCount < maxRetries) {
        if (retryCount > 0) {
            echo "🔄 Retry attempt ${retryCount + 1} of ${maxRetries}"
            sleep(time: (retryCount * 5), unit: 'SECONDS')
        }

        def response = httpRequest(
            url: fullUrl,
            httpMode: 'POST',
            contentType: 'APPLICATION_JSON',
            requestBody: JsonOutput.toJson(payload),
            customHeaders: [
                [name: 'X-API-Key', value: params.X_API_KEY.toString()],
                [name: 'Content-Type', value: 'application/json']
            ],
            timeout: env.TIMEOUT_SECONDS.toInteger(),
            validResponseCodes: '100:599',
            ignoreSslErrors: true
        )

        env.API_STATUS = response.status.toString()
        env.API_RESPONSE = response.content

        if (response.status >= 200 && response.status < 300) {
            echo "✅ Response Status: ${response.status}"
            echo "📄 Raw Response: ${response.content}"
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
        def jsonString = (json instanceof String) ? json : JsonOutput.toJson(json)
        def jsonObj = readJSON text: jsonString
        return JsonOutput.prettyPrint(JsonOutput.toJson(jsonObj))
    } catch (Exception e) {
        return json.toString()
    }
}

def archiveAuditLog(payload) {
    def auditLog = [
        buildNumber: env.BUILD_NUMBER,
        timestamp: new Date().format("yyyy-MM-dd'T'HH:mm:ss'Z'"),
        user: env.BUILD_USER ?: 'System',
        purpose: params.PURPOSE,
        parameters: params,
        requestPayload: payload,
        result: currentBuild.result,
        duration: currentBuild.durationString,
        apiStatus: env.API_STATUS,
        apiResponse: env.API_RESPONSE
    ]

    writeJSON file: "audit-log-${env.BUILD_NUMBER}.json", json: auditLog, pretty: 4
    archiveArtifacts artifacts: "audit-log-${env.BUILD_NUMBER}.json", allowEmptyArchive: true
}