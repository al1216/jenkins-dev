# Design Document
## Client Setup Platform Automation - Jenkins Pipeline

---

### Document Information
| Property | Value |
|----------|-------|
| **Document Version** | 1.0 |
| **Last Updated** | November 3, 2025 |
| **Status** | Active |
| **Related HLD** | [High-Level Design Document](./HLD.md) |

---

## Table of Contents
1. [Overview](#1-overview)
2. [Architecture & Design](#2-architecture--design)
3. [Technical Specifications](#3-technical-specifications)
4. [Parameter Reference](#4-parameter-reference)
5. [Operation Details](#5-operation-details)
6. [API Integration](#6-api-integration)
7. [Error Handling & Resilience](#7-error-handling--resilience)
8. [Security Implementation](#8-security-implementation)
9. [Audit & Logging](#9-audit--logging)
10. [Testing Strategy](#10-testing-strategy)
11. [Deployment Guide](#11-deployment-guide)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Overview

### 1.1 Purpose
The Client Setup Platform Automation is a Jenkins-based pipeline that provides a unified interface for operations teams to manage client configurations across multiple environments. It abstracts complex API interactions into a user-friendly, parameterized Jenkins job.

**For detailed system architecture and business context, see the [High-Level Design (HLD)](./HLD.md).**

### 1.2 Scope
This design document covers:
- Technical implementation details of the Jenkins pipeline
- Parameter specifications and validation rules
- API integration patterns and payload structures
- Error handling and retry mechanisms
- Security controls and audit logging
- Operational procedures and troubleshooting

### 1.3 Target Audience
- DevOps Engineers
- Platform Engineers
- Operations Teams
- Technical Managers
- QA Engineers

---

## 2. Architecture & Design

### 2.1 Pipeline Structure

The pipeline follows a declarative syntax with the following structure:

```
Jenkinsfile
├── Pipeline Definition
│   ├── Agent Configuration
│   ├── Parameters (Input UI)
│   ├── Environment Variables
│   └── Stages
│       └── Build and Execute
│           ├── Validation
│           ├── Payload Building
│           ├── API Execution
│           └── Audit Archival
├── Helper Functions
│   ├── buildPayload()
│   ├── executeAPICall()
│   ├── prettyPrintJson()
│   └── archiveAuditLog()
└── Post Actions
    ├── Success Handler
    └── Failure Handler
```

### 2.2 Design Principles

1. **Declarative Configuration**: Using Jenkins Declarative Pipeline for readability and maintainability
2. **Fail-Fast Validation**: Early parameter validation before API calls
3. **Idempotency**: Safe to re-run failed operations
4. **Auditability**: Complete logging of all operations
5. **Security by Default**: API keys as password parameters, HTTPS only
6. **Graceful Degradation**: Retry logic with exponential backoff

### 2.3 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Orchestration** | Jenkins | 2.414.2+ | Pipeline execution |
| **Pipeline DSL** | Groovy | N/A | Pipeline definition |
| **API Protocol** | REST/HTTPS | N/A | Backend communication |
| **Data Format** | JSON | N/A | Payload and logging |
| **Plugin** | HTTP Request Plugin | Latest | API calls |
| **Plugin** | Pipeline Utility Steps | Latest | JSON handling |

---

## 3. Technical Specifications

### 3.1 Pipeline Configuration

#### Agent Configuration
```groovy
agent any
```
- Executes on any available Jenkins agent
- No special requirements (no Docker/Kubernetes needed)

#### Environment Variables
```groovy
environment {
    TIMEOUT_SECONDS = '30'
    RETRY_COUNT = '3'
}
```

| Variable | Value | Purpose |
|----------|-------|---------|
| `TIMEOUT_SECONDS` | 30 | HTTP request timeout |
| `RETRY_COUNT` | 3 | Maximum retry attempts |

### 3.2 Data Flow

```
┌─────────────┐
│ User Input  │
│ (Parameters)│
└──────┬──────┘
       │
       ↓
┌──────────────────────┐
│ Validation Layer     │
│ • Required fields    │
│ • Format validation  │
└──────┬───────────────┘
       │
       ↓
┌──────────────────────┐
│ Payload Builder      │
│ • Purpose-based      │
│ • Type conversion    │
│ • Array parsing      │
└──────┬───────────────┘
       │
       ↓
┌──────────────────────┐
│ API Executor         │
│ • URL construction   │
│ • Retry logic        │
│ • Response handling  │
└──────┬───────────────┘
       │
       ↓
┌──────────────────────┐
│ Audit Logger         │
│ • JSON formatting    │
│ • Artifact archival  │
└──────────────────────┘
```

---

## 4. Parameter Reference

### 4.1 Complete Parameter List

#### 4.1.1 Authentication & Environment

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `X_API_KEY` | Password | ✅ Yes | - | API authentication key (masked) |
| `STAGING_ENV` | Choice | ✅ Yes | beta | Target environment: beta, qa, prod |
| `DRY_RUN` | Boolean | No | false | Preview mode without execution |

#### 4.1.2 Operation Parameters

| Parameter | Type | Required | Default | Values |
|-----------|------|----------|---------|--------|
| `PURPOSE` | Choice | ✅ Yes | - | See [Purpose Options](#purpose-options) |
| `clientId` | String | Conditional | - | Numeric client identifier |
| `instanceName` | String | ✅ Yes | - | Unique instance identifier |

#### 4.1.3 Retailer Configuration

| Parameter | Type | Required | Default | Values |
|-----------|------|----------|---------|--------|
| `retailer` | Choice | Conditional | - | ahold, albertsons, amazon, bestbuy, chewy, costco, cvs, fresh, gopuff, hyvee, instacart, kroger, meijer, omni, overstock, samsclub, shipt, shoprite, target, ubereats, walgreen, walmart, wayfair |
| `retailerVariant` | Choice | Conditional | - | 3P, api, business, citrus, criteo, direct, fresh, hybrid, kevel, native, promoteiq, retail, retailer, rms |
| `region` | Choice | Conditional | - | CA, FR, GB, IE, IT, MX, UK, US |

#### 4.1.4 Product & Feature Configuration

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `productLine` | Choice | Conditional | - | RMM or ESM |
| `features` | String | Conditional | - | Comma-separated feature list |
| `feature` | String | Conditional | - | Single feature name |

#### 4.1.5 Activation/Deactivation Parameters

| Parameter | Type | Required | Default | Values |
|-----------|------|----------|---------|--------|
| `enableDisableEntity` | Choice | Conditional | - | CLIENT, FEATURE, INSTANCE, REGION, RETAILER |
| `activate` | Choice | Conditional | true | true, false |

### 4.2 Purpose Options

The `PURPOSE` parameter determines the operation type and required parameters:

| Purpose | Operation Type | Required Parameters |
|---------|----------------|---------------------|
| **Onboard a new retailer or account** | onboard | clientId, instanceName, retailer, retailerVariant, region, productLine, features (optional) |
| **Enable a new feature for an existing instance** | onboard | clientId, instanceName, retailer, retailerVariant, region, productLine, features |
| **Blacklist a feature for an existing instance** | onboard | clientId, instanceName, retailer, retailerVariant, region, productLine, features |
| **Activate an onboarded instance** | activate | instanceName, enableDisableEntity, activate |
| **De-onboard a retailer** | activate | instanceName, enableDisableEntity, region, retailer, retailerVariant, activate |
| **Enable a new region for an existing instance** | activate | clientId, instanceName, enableDisableEntity, activate, retailer, retailerVariant, region, productLine, features (optional) |
| **Whitelabel a blacklisted feature** | activate | instanceName, enableDisableEntity, region, retailer, retailerVariant, activate, clientId, productLine, feature |
| **Disable a module** | activate | instanceName, enableDisableEntity, clientId, region, retailer, retailerVariant, productLine, feature, activate |

---

## 5. Operation Details

### 5.1 Payload Building Logic

The `buildPayload()` function constructs operation-specific payloads:

#### Base Payload Structure
```json
{
  "user": "ops@commerceiq.ai",
  "metadata": {
    "executedBy": "jenkins_user",
    "buildNumber": "123",
    "timestamp": "2025-11-03T10:30:00Z"
  }
}
```

#### Purpose-Specific Additions

##### Onboard Operations
```json
{
  "clientId": 12345,
  "instanceName": "client-prod",
  "retailer": "walmart",
  "retailerVariant": "retail",
  "region": "US",
  "productLine": "RMM",
  "features": ["feature1", "feature2"]
}
```

##### Activate/Deactivate Operations
```json
{
  "instanceName": "client-prod",
  "enableDisableEntity": "FEATURE",
  "activate": true
}
```

### 5.2 Type Conversions

The pipeline performs automatic type conversions:

| Parameter | Input Type | Conversion | Output Type |
|-----------|------------|------------|-------------|
| `clientId` | String | `.toInteger()` | Integer |
| `activate` | String | `.toBoolean()` | Boolean |
| `features` | String (CSV) | `.split(',').collect { it.trim() }` | Array[String] |

---

## 6. API Integration

### 6.1 Endpoint Mapping

#### Base URL Construction
```groovy
def apiBaseUrl = "http://client-setup-platform.${params.STAGING_ENV}-dbx.commerceiq.ai"
```

**Environment Examples:**
- Beta: `http://client-setup-platform.beta-dbx.commerceiq.ai`
- QA: `http://client-setup-platform.qa-dbx.commerceiq.ai`
- Prod: `http://client-setup-platform.prod-dbx.commerceiq.ai`

#### Endpoint Selection Logic

| Purpose Category | Endpoint | HTTP Method |
|------------------|----------|-------------|
| Onboard Operations | `/common-auth/api/v1/instance/onboard` | POST |
| Activate Operations | `/common-auth/api/v1/instance/activate-deactivate` | POST |

### 6.2 HTTP Request Specification

```groovy
httpRequest(
    url: fullUrl,
    httpMode: 'POST',
    contentType: 'APPLICATION_JSON',
    requestBody: JsonOutput.toJson(payload),
    customHeaders: [
        [name: 'X-API-Key', value: params.X_API_KEY.toString()],
        [name: 'Content-Type', value: 'application/json']
    ],
    timeout: 30,
    validResponseCodes: '100:599',
    ignoreSslErrors: true
)
```

### 6.3 Request Headers

| Header | Value | Purpose |
|--------|-------|---------|
| `X-API-Key` | User-provided | Authentication |
| `Content-Type` | `application/json` | Payload format |

### 6.4 Response Handling

#### Success Criteria
- HTTP Status: `200-299`
- Response logged to console and audit file

#### Failure Handling
- HTTP Status: `>= 300`
- Triggers retry mechanism
- Error details logged

---

## 7. Error Handling & Resilience

### 7.1 Retry Mechanism

```groovy
def maxRetries = 3
def retryCount = 0

while (retryCount < maxRetries) {
    if (retryCount > 0) {
        sleep(time: (retryCount * 5), unit: 'SECONDS')
    }
    
    // Execute API call
    
    if (success) {
        return
    }
    
    retryCount++
}

error("All attempts failed")
```

**Retry Strategy:**
- **Attempt 1**: Immediate
- **Attempt 2**: After 5 seconds
- **Attempt 3**: After 10 seconds

### 7.2 Timeout Configuration

- **Per-Request Timeout**: 30 seconds
- **Total Max Duration**: ~105 seconds (3 attempts with backoff)

### 7.3 Error Propagation

```
API Failure
    ↓
Retry Logic (3x)
    ↓
Final Failure
    ↓
Pipeline Fails
    ↓
Audit Log Updated (FAILURE)
    ↓
Post-Failure Hook Executed
```

### 7.4 Common Error Scenarios

| Error Type | Status Code | Retry? | Resolution |
|------------|-------------|--------|------------|
| Invalid API Key | 401 | No | Check X-API-Key parameter |
| Missing Parameters | 400 | No | Review payload in dry run |
| Service Unavailable | 503 | Yes | Automatic retry |
| Gateway Timeout | 504 | Yes | Automatic retry |
| Internal Server Error | 500 | Yes | Automatic retry |

---

## 8. Security Implementation

### 8.1 Authentication

#### API Key Management
```groovy
password(
    name: 'X_API_KEY',
    defaultValue: '',
    description: '🔑 Your X-API-Key (required for authentication).'
)
```

**Security Features:**
- Password parameter type (masked in UI)
- Not logged in console output
- Not stored in audit logs (redacted)
- Transmitted over HTTPS only

### 8.2 Access Control

**Jenkins Level:**
- Role-Based Access Control (RBAC)
- Project-level permissions
- Build permission required

**API Level:**
- X-API-Key validation
- Environment-specific keys
- Key rotation support

### 8.3 Secure Communication

```groovy
ignoreSslErrors: true  // For internal certificates
```

**Note**: In production, use valid SSL certificates and set `ignoreSslErrors: false`

### 8.4 Audit Trail Security

- All operations logged with user attribution
- Immutable audit logs (Jenkins artifacts)
- Timestamped entries
- Payload sanitization (API keys redacted)

---

## 9. Audit & Logging

### 9.1 Audit Log Structure

```json
{
  "buildNumber": "123",
  "timestamp": "2025-11-03T10:30:00Z",
  "user": "jenkins_user",
  "purpose": "Onboard a new retailer or account",
  "parameters": {
    "X_API_KEY": "***REDACTED***",
    "STAGING_ENV": "beta",
    "clientId": "12345",
    "instanceName": "client-prod",
    "retailer": "walmart",
    "region": "US",
    "productLine": "RMM"
  },
  "requestPayload": {
    "user": "ops@commerceiq.ai",
    "clientId": 12345,
    "instanceName": "client-prod"
  },
  "result": "SUCCESS",
  "duration": "45 sec",
  "apiStatus": "200",
  "apiResponse": "{\"status\": \"success\", \"instanceId\": \"abc123\"}"
}
```

### 9.2 Log Levels

| Level | Source | Content |
|-------|--------|---------|
| **INFO** | Pipeline | Operation start, purpose, parameters |
| **DEBUG** | Payload Builder | Final payload (pretty-printed JSON) |
| **INFO** | API Executor | Request details, response status |
| **ERROR** | Error Handler | Failure reasons, retry attempts |
| **AUDIT** | Archive Function | Complete audit log (JSON artifact) |

### 9.3 Artifact Archival

```groovy
writeJSON file: "audit-log-${env.BUILD_NUMBER}.json", json: auditLog, pretty: 4
archiveArtifacts artifacts: "audit-log-*.json", allowEmptyArchive: true
```

**Artifact Details:**
- **Format**: JSON (pretty-printed with 4-space indent)
- **Filename**: `audit-log-{BUILD_NUMBER}.json`
- **Storage**: Jenkins artifact repository
- **Retention**: Per Jenkins global configuration
- **Access**: Available via Jenkins UI and API

### 9.4 Console Output

The pipeline provides rich console output:

```
--- Starting Operation for Purpose: Onboard a new retailer or account ---
API Host: http://client-setup-platform.beta-dbx.commerceiq.ai

Final Payload:
{
  "user": "ops@commerceiq.ai",
  "clientId": 12345,
  ...
}

🚀 Executing API call to http://client-setup-platform.beta-dbx.commerceiq.ai/common-auth/api/v1/instance/onboard...
✅ Response Status: 200
📄 Raw Response: {"status": "success"}

✅ OPERATION COMPLETED SUCCESSFULLY
```

---

## 10. Testing Strategy

### 10.1 Dry Run Testing

**Purpose**: Preview operations without executing API calls

**Usage:**
1. Set `DRY_RUN` parameter to `true`
2. Configure all other parameters normally
3. Run pipeline
4. Review console output for payload validation

**Output:**
```
Final Payload:
{
  "user": "ops@commerceiq.ai",
  "clientId": 12345,
  ...
}

--- DRY RUN: API Call would be executed with the payload above ---
```

### 10.2 Test Scenarios

#### Test Case 1: New Client Onboarding
```yaml
Purpose: Onboard a new retailer or account
Environment: beta
ClientId: 99999
InstanceName: test-instance
Retailer: walmart
RetailerVariant: retail
Region: US
ProductLine: RMM
Features: feature1,feature2
DryRun: true
Expected: Valid payload generated, no API call
```

#### Test Case 2: Feature Enablement
```yaml
Purpose: Enable a new feature for an existing instance
Environment: qa
ClientId: 12345
InstanceName: existing-instance
Features: new-feature
DryRun: false
Expected: API call succeeds, audit log created
```

#### Test Case 3: Retry Logic
```yaml
Purpose: Any
Environment: beta
Setup: Temporarily invalid API endpoint
Expected: 3 retry attempts, exponential backoff, final failure
```

### 10.3 Integration Testing

**Pre-Deployment Checklist:**
- [ ] Test all purpose types in beta environment
- [ ] Validate dry run mode
- [ ] Test retry logic (simulate API failures)
- [ ] Verify audit log completeness
- [ ] Test with invalid parameters
- [ ] Verify error messages are clear

---

## 11. Deployment Guide

### 11.1 Prerequisites

**Jenkins Requirements:**
- Jenkins version 2.300+
- Plugins:
  - Pipeline
  - HTTP Request Plugin
  - Pipeline Utility Steps Plugin
  - Credentials Plugin

**Network Requirements:**
- Outbound HTTPS access to:
  - `*.beta-dbx.commerceiq.ai`
  - `*.qa-dbx.commerceiq.ai`
  - `*.prod-dbx.commerceiq.ai`

**Access Requirements:**
- Jenkins job creation permission
- API keys for each environment

### 11.2 Deployment Steps

#### Step 1: Create Jenkins Job
1. Navigate to Jenkins dashboard
2. Click "New Item"
3. Enter job name: `Client-Setup-Platform-Automation`
4. Select "Pipeline"
5. Click "OK"

#### Step 2: Configure Pipeline
1. In job configuration, scroll to "Pipeline" section
2. Select "Pipeline script from SCM"
3. SCM: Git
4. Repository URL: `<your-repo-url>`
5. Script Path: `Jenkinsfile`
6. Save

#### Step 3: Test in Beta
1. Run job with `STAGING_ENV=beta`
2. Enable `DRY_RUN=true`
3. Verify payload structure
4. Execute with `DRY_RUN=false`
5. Verify API response

#### Step 4: Promote to QA/Prod
1. Update API keys for target environment
2. Test critical scenarios
3. Document successful test cases
4. Enable for operations team

### 11.3 Rollback Procedure

If issues are detected:
1. Disable job (mark as "disabled" in Jenkins)
2. Revert to previous Jenkinsfile version
3. Investigate audit logs for failures
4. Fix issues in development
5. Re-test in beta before re-enabling

---

## 12. Troubleshooting

### 12.1 Common Issues

#### Issue: "You must select a Purpose for the operation"
**Cause**: Empty PURPOSE parameter  
**Solution**: Select a purpose from dropdown

#### Issue: "All 3 attempts failed"
**Cause**: API unavailable or incorrect parameters  
**Solution**: 
1. Check API endpoint accessibility
2. Verify X-API-Key validity
3. Review payload in dry run mode
4. Check audit log for error details

#### Issue: "Invalid API Key" (401)
**Cause**: Incorrect or expired X-API-Key  
**Solution**: 
1. Verify API key with platform team
2. Check environment-specific keys
3. Rotate key if compromised

#### Issue: Missing required parameters (400)
**Cause**: Required fields not provided for selected purpose  
**Solution**: Review [Parameter Reference](#4-parameter-reference) for required fields

### 12.2 Debug Checklist

When troubleshooting failures:
- [ ] Review console output for error messages
- [ ] Check audit log artifact for request/response details
- [ ] Verify environment selection matches intended target
- [ ] Test with dry run mode first
- [ ] Validate API key in Postman/curl
- [ ] Check network connectivity to API endpoint
- [ ] Review recent changes to Jenkinsfile
- [ ] Contact platform team if API issues persist

### 12.3 Support Contacts

| Issue Type | Contact | Method |
|------------|---------|--------|
| Jenkins Configuration | DevOps Team | Slack: #devops-support |
| API Issues | Platform Team | Slack: #platform-team |
| Access/Permissions | IT Security | JIRA: IT-SUPPORT |
| Emergency | On-Call Engineer | PagerDuty |

---

## 13. Maintenance & Operations

### 13.1 Regular Maintenance Tasks

| Task | Frequency | Owner |
|------|-----------|-------|
| Review audit logs for patterns | Weekly | Operations |
| Update retailer/region choices | As needed | DevOps |
| Rotate API keys | Quarterly | Security |
| Archive old audit logs | Monthly | DevOps |
| Jenkins plugin updates | Monthly | DevOps |

### 13.2 Monitoring

**Key Metrics to Track:**
- Success rate by environment
- Average execution time
- Retry rate
- Most common purposes
- User adoption metrics

**Alerting:**
- Success rate drops below 90%
- Average retry rate exceeds 20%
- API endpoint unreachable

---

## 14. Appendix

### 14.1 Code Examples

#### Example: Manual API Call (curl)
```bash
curl -X POST \
  http://client-setup-platform.beta-dbx.commerceiq.ai/common-auth/api/v1/instance/onboard \
  -H 'X-API-Key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "user": "ops@commerceiq.ai",
    "clientId": 12345,
    "instanceName": "test-instance",
    "retailer": "walmart",
    "retailerVariant": "retail",
    "region": "US",
    "productLine": "RMM",
    "features": ["feature1", "feature2"]
  }'
```

### 14.2 Useful Jenkins Pipeline Snippets

#### Retrieve Audit Log Programmatically
```groovy
def auditLog = readJSON file: "audit-log-${BUILD_NUMBER}.json"
echo "Operation: ${auditLog.purpose}"
```

#### Send Slack Notification (if Slack plugin installed)
```groovy
slackSend(
    channel: '#operations',
    color: 'good',
    message: "Client setup completed: ${params.instanceName}"
)
```

---

## 15. Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-03 | DevOps Team | Initial design document |

---

## 16. Related Documents

- **[High-Level Design (HLD)](./HLD.md)** - System architecture and business context
- **[Jenkinsfile](./Jenkinsfile)** - Pipeline source code
- **[README](./readme.md)** - Setup and installation instructions

---

**Document Classification**: Internal Use  
**Last Review Date**: November 3, 2025  
**Next Review Date**: February 3, 2026

