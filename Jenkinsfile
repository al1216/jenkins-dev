#!/usr/bin/env groovy

// This pipeline uses the Active Choices plugin to create a dynamic UI.

// Define all job properties, including dynamic parameters, outside the pipeline block.
properties([
    parameters([
        password(
            name: 'X_API_KEY',
            defaultValue: '',
            description: '🔑 Your X-API-Key (required for authentication).'
        ),
        choice(
            name: 'OPERATION',
            choices: ['onboardInstance', 'activateInstance'],
            description: '🎯 Select the top-level operation.'
        ),
        // Dynamic "Purpose" dropdown
        [
            $class: 'org.biouno.unochoice.CascadeChoiceParameter',
            name: 'PURPOSE',
            description: 'Select the specific goal for your operation.',
            referencedParameters: 'OPERATION',
            choiceType: 'PT_SINGLE_SELECT',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        if (OPERATION == 'onboardInstance') {
                            return [
                                'Onboard a new retailer or account',
                                'Enable a new feature for an existing instance',
                                'Blacklist a feature for an existing instance'
                            ]
                        } else if (OPERATION == 'activateInstance') {
                            return [
                                'Activate an onboarded instance',
                                'De-onboard a retailer',
                                'Enable a new region for an existing instance',
                                'Whitelabel a blacklisted feature'
                            ]
                        } else {
                            return ['Select an Operation first']
                        }
                    '''
                ]
            ]
        ],
        // --- Conditionally Enabled/Disabled Parameters ---
        [
            $class: 'org.biouno.unochoice.DynamicParameter',
            name: 'clientId',
            description: 'Client ID',
            choiceType: 'ET_FORMATTED_HTML',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        def neededFor = [
                            'Onboard a new retailer or account',
                            'Enable a new feature for an existing instance',
                            'Blacklist a feature for an existing instance',
                            'Enable a new region for an existing instance',
                            'Whitelabel a blacklisted feature'
                        ]
                        def disabled = (PURPOSE in neededFor) ? '' : 'disabled'
                        return "<input type=\"text\" name=\"value\" class=\"setting-input\" ${disabled}>"
                    '''
                ]
            ]
        ],
        [
            $class: 'org.biouno.unochoice.DynamicParameter',
            name: 'instanceName',
            description: 'Instance Name',
            choiceType: 'ET_FORMATTED_HTML',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        def disabled = (PURPOSE != null && PURPOSE != 'Select an Operation first') ? '' : 'disabled'
                        return "<input type=\"text\" name=\"value\" class=\"setting-input\" ${disabled}>"
                    '''
                ]
            ]
        ],
        [
            $class: 'org.biouno.unochoice.DynamicParameter',
            name: 'retailer',
            description: 'Retailer',
            choiceType: 'ET_FORMATTED_HTML',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        def neededFor = [
                            'Onboard a new retailer or account',
                            'Enable a new feature for an existing instance',
                            'Blacklist a feature for an existing instance',
                            'De-onboard a retailer',
                            'Enable a new region for an existing instance',
                            'Whitelabel a blacklisted feature'
                        ]
                        def disabled = (PURPOSE in neededFor) ? '' : 'disabled'
                        return "<input type=\"text\" name=\"value\" class=\"setting-input\" ${disabled}>"
                    '''
                ]
            ]
        ],
        [
            $class: 'org.biouno.unochoice.DynamicParameter',
            name: 'retailerVariant',
            description: 'Retailer Variant',
            choiceType: 'ET_FORMATTED_HTML',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        def neededFor = [
                            'Onboard a new retailer or account',
                            'Enable a new feature for an existing instance',
                            'Blacklist a feature for an existing instance',
                            'De-onboard a retailer',
                            'Enable a new region for an existing instance',
                            'Whitelabel a blacklisted feature'
                        ]
                        def disabled = (PURPOSE in neededFor) ? '' : 'disabled'
                        return "<input type=\"text\" name=\"value\" class=\"setting-input\" ${disabled}>"
                    '''
                ]
            ]
        ],
        [
            $class: 'org.biouno.unochoice.DynamicParameter',
            name: 'region',
            description: 'Region',
            choiceType: 'ET_FORMATTED_HTML',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        def neededFor = [
                            'Onboard a new retailer or account',
                            'Enable a new feature for an existing instance',
                            'Blacklist a feature for an existing instance',
                            'De-onboard a retailer',
                            'Enable a new region for an existing instance',
                            'Whitelabel a blacklisted feature'
                        ]
                        def disabled = (PURPOSE in neededFor) ? '' : 'disabled'
                        return "<input type=\"text\" name=\"value\" class=\"setting-input\" ${disabled}>"
                    '''
                ]
            ]
        ],
        [
            $class: 'org.biouno.unochoice.DynamicParameter',
            name: 'productLine',
            description: 'Product Line',
            choiceType: 'ET_FORMATTED_HTML',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        def neededFor = [
                            'Onboard a new retailer or account',
                            'Enable a new feature for an existing instance',
                            'Blacklist a feature for an existing instance',
                            'Enable a new region for an existing instance',
                            'Whitelabel a blacklisted feature'
                        ]
                        def disabled = (PURPOSE in neededFor) ? '' : 'disabled'
                        return "<select name=\"value\" ${disabled}><option value=\"\"></option><option value=\"RMM\">RMM</option><option value=\"ESM\">ESM</option></select>"
                    '''
                ]
            ]
        ],
        [
            $class: 'org.biouno.unochoice.DynamicParameter',
            name: 'features',
            description: 'Features (comma-separated)',
            choiceType: 'ET_FORMATTED_HTML',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        def neededFor = [
                            'Onboard a new retailer or account',
                            'Enable a new feature for an existing instance',
                            'Blacklist a feature for an existing instance',
                            'Enable a new region for an existing instance'
                        ]
                        def disabled = (PURPOSE in neededFor) ? '' : 'disabled'
                        return "<input type=\"text\" name=\"value\" class=\"setting-input\" ${disabled}>"
                    '''
                ]
            ]
        ],
        [
            $class: 'org.biouno.unochoice.DynamicParameter',
            name: 'feature',
            description: 'Feature (single)',
            choiceType: 'ET_FORMATTED_HTML',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        def disabled = (PURPOSE == 'Whitelabel a blacklisted feature') ? '' : 'disabled'
                        return "<input type=\"text\" name=\"value\" class=\"setting-input\" ${disabled}>"
                    '''
                ]
            ]
        ],
        [
            $class: 'org.biouno.unochoice.DynamicParameter',
            name: 'enableDisableEntity',
            description: 'Entity to Enable/Disable',
            choiceType: 'ET_FORMATTED_HTML',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        def neededFor = [
                            'Activate an onboarded instance',
                            'De-onboard a retailer',
                            'Whitelabel a blacklisted feature'
                        ]
                        def disabled = (PURPOSE in neededFor) ? '' : 'disabled'
                        return "<input type=\"text\" name=\"value\" class=\"setting-input\" ${disabled}>"
                    '''
                ]
            ]
        ],
        [
            $class: 'org.biouno.unochoice.DynamicParameter',
            name: 'activate',
            description: 'Activate?',
            choiceType: 'ET_FORMATTED_HTML',
            script: [
                $class: 'GroovyScript',
                script: [
                    classpath: [],
                    sandbox: true,
                    script: '''
                        def neededFor = [
                            'Activate an onboarded instance',
                            'De-onboard a retailer',
                            'Whitelabel a blacklisted feature'
                        ]
                        def disabled = (PURPOSE in neededFor) ? '' : 'disabled'
                        return "<select name=\"value\" ${disabled}><option value=\"true\">true</option><option value=\"false\">false</option></select>"
                    '''
                ]
            ]
        ],
        booleanParam(
            name: 'DRY_RUN',
            defaultValue: false,
            description: '🔍 Dry run mode (preview without executing)'
        )
    ])
])

pipeline {
    agent any

    environment {
        API_BASE_URL = 'http://client-setup-platform.beta-dbx.commerceiq.ai'
        TIMEOUT_SECONDS = '30'
        RETRY_COUNT = '3'
    }

    stages {
        stage('🔨 Build and Execute') {
            steps {
                script {
                    echo "--- Starting Operation ---"
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

    // Conditionally add parameters to the payload if they exist and are not empty
    if (params.clientId) payload.clientId = params.clientId
    if (params.instanceName) payload.instanceName = params.instanceName
    if (params.retailer) payload.retailer = params.retailer
    if (params.retailerVariant) payload.retailerVariant = params.retailerVariant
    if (params.region) payload.region = params.region
    if (params.productLine) payload.productLine = params.productLine
    if (params.activate) payload.activate = params.activate.toBoolean()
    if (params.enableDisableEntity) payload.enableDisableEntity = params.enableDisableEntity
    
    // Handle features and feature
    def featuresList = []
    if (params.features) {
        featuresList.addAll(params.features.split(',').collect { it.trim() })
    }
    if (params.feature) {
        if (PURPOSE == 'Whitelabel a blacklisted feature') {
             payload.feature = params.feature.trim()
        } else {
             featuresList.add(params.feature.trim())
        }
    }

    if (featuresList) {
        payload.features = featuresList
    }

    return payload
}

def executeAPICall() {
    def operation = (params.PURPOSE.contains('Onboard') || params.PURPOSE.contains('Enable') || params.PURPOSE.contains('Blacklist')) ? 'onboardInstance' : 'activateInstance'
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
            validResponseCodes: '100:599'
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
