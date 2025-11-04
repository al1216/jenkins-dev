# High-Level Design (HLD)
## Client Setup Platform Automation via Jenkins

---

### Document Information
| Property | Value |
|----------|-------|
| **Document Version** | 1.0 |
| **Last Updated** | November 3, 2025 |
| **Status** | Active |
| **Owner** | DevOps Team |

---

## 1. Executive Summary

The Client Setup Platform Automation is a Jenkins-based orchestration system that provides a self-service portal for operations teams to manage client onboarding, feature enablement, and instance configuration across multiple environments (beta, qa, prod). This solution eliminates manual API interactions, reduces operational errors, and provides comprehensive audit trails for all configuration changes.

### Key Benefits
- **🚀 Operational Efficiency**: Reduces client setup time from hours to minutes
- **🛡️ Error Reduction**: Standardized workflows minimize human error
- **📊 Audit Compliance**: Complete audit trail for all configuration changes
- **🔐 Security**: Centralized API key management with role-based access
- **🌍 Multi-Environment Support**: Seamless operations across beta, qa, and production

---

## 2. System Architecture

### 2.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Jenkins Server                           │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         Client Setup Automation Pipeline               │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │    │
│  │  │  Parameter   │  │   Payload    │  │  API Call   │ │    │
│  │  │ Validation   │→ │  Building    │→ │  Execution  │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │    │
│  │           │                │                 │         │    │
│  │           ↓                ↓                 ↓         │    │
│  │  ┌──────────────────────────────────────────────────┐ │    │
│  │  │         Audit Logging & Archival                 │ │    │
│  │  └──────────────────────────────────────────────────┘ │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS/REST API
                         │ (with X-API-Key)
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│              Client Setup Platform Service                       │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │   Onboarding     │  │    Activation    │  │   Feature    │ │
│  │     Service      │  │     Service      │  │  Management  │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│                                                                  │
│  Environment-Specific URLs:                                     │
│  • beta-dbx.commerceiq.ai                                       │
│  • qa-dbx.commerceiq.ai                                         │
│  • prod-dbx.commerceiq.ai                                       │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Configuration Database                        │
│  (Client Instances, Features, Retailers, Regions)               │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Description

#### Jenkins Pipeline (Orchestration Layer)
- **Responsibility**: User interaction, parameter validation, API orchestration
- **Technology**: Jenkins Declarative Pipeline (Groovy DSL)
- **Key Functions**: 
  - Parameter collection and validation
  - Dynamic payload construction
  - API call execution with retry logic
  - Audit log generation

#### Client Setup Platform Service (Backend API)
- **Responsibility**: Business logic for client configuration
- **Endpoints**:
  - `/common-auth/api/v1/instance/onboard` - New client/feature onboarding
  - `/common-auth/api/v1/instance/activate-deactivate` - Instance state management
- **Authentication**: X-API-Key based authentication

#### Configuration Database
- **Responsibility**: Persistent storage of client configurations
- **Data**: Client instances, features, retailer mappings, region settings

---

## 3. Supported Operations

### 3.1 Operation Categories

| Operation | Purpose | Target Audience | Frequency |
|-----------|---------|-----------------|-----------|
| **Onboard a new retailer or account** | Initial client setup with base configuration | Account Management, Sales Ops | Weekly |
| **Enable a new feature** | Add capabilities to existing instances | Product Team, CSM | Daily |
| **Blacklist a feature** | Disable specific features for compliance/testing | Product Team, Engineering | Weekly |
| **Activate an onboarded instance** | Make a configured instance live | Operations, Account Management | Weekly |
| **De-onboard a retailer** | Remove/deactivate client configuration | Account Management | Monthly |
| **Enable a new region** | Expand instance to new geographic regions | Global Operations | Monthly |
| **Whitelabel a blacklisted feature** | Re-enable previously disabled feature | Product Team, Engineering | As needed |
| **Disable a module** | Turn off specific functional modules | Engineering, Support | As needed |

### 3.2 Supported Configurations

#### Retailers (23 Total)
Ahold, Albertsons, Amazon, BestBuy, Chewy, Costco, CVS, Fresh, GoPuff, HyVee, Instacart, Kroger, Meijer, Omni, Overstock, SamsClub, Shipt, ShopRite, Target, UberEats, Walgreens, Walmart, Wayfair

#### Regions
CA, FR, GB, IE, IT, MX, UK, US

#### Product Lines
- **RMM** (Retail Media Management)
- **ESM** (E-commerce Shelf Management)

---

## 4. Security Architecture

### 4.1 Authentication & Authorization
```
┌──────────────┐
│   Jenkins    │
│     User     │
└──────┬───────┘
       │ (1) Jenkins RBAC
       │     Authentication
       ↓
┌──────────────────┐
│  Jenkins Server  │
│  ┌────────────┐  │
│  │  X-API-Key │  │ (2) Secure Parameter
│  │  (Password │  │     (Masked in logs)
│  │   Param)   │  │
│  └────────────┘  │
└────────┬─────────┘
         │ (3) HTTPS Request
         │     with X-API-Key
         ↓
┌─────────────────────┐
│  Client Setup API   │
│  ┌───────────────┐  │
│  │  API Key      │  │ (4) Key Validation
│  │  Validation   │  │
│  └───────────────┘  │
└─────────────────────┘
```

### 4.2 Security Features
- **🔐 API Key Security**: Password parameter type (masked in Jenkins UI and logs)
- **🔒 HTTPS Communication**: All API calls over TLS
- **📝 Audit Trails**: Complete logging of all operations with user attribution
- **🛡️ Dry Run Mode**: Preview changes before execution
- **🚫 Input Validation**: Parameter validation before API execution

---

## 5. Workflow & Process Flow

### 5.1 Standard Operation Flow

```
┌─────────────────┐
│  User Selects   │
│   Parameters    │
│  in Jenkins UI  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   Validation    │
│  • Required     │
│    fields       │
│  • Format check │
└────────┬────────┘
         │
         ↓
┌─────────────────┐      ┌──────────────┐
│ Build Payload   │      │  Dry Run?    │
│ (Dynamic based  │─────→│  • Preview   │
│  on purpose)    │      │  • No execute│
└────────┬────────┘      └──────────────┘
         │
         ↓
┌─────────────────┐
│  Execute API    │
│  • Retry logic  │
│  • 3 attempts   │
│  • Backoff      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Archive Audit  │
│  Log as JSON    │
│  Artifact       │
└─────────────────┘
```

### 5.2 Error Handling & Resilience

- **Retry Mechanism**: 3 automatic retries with exponential backoff
- **Timeout Management**: 30-second timeout per API call
- **Error Propagation**: Clear error messages for troubleshooting
- **Partial Success Handling**: Audit logs capture attempted operations

---

## 6. Monitoring & Observability

### 6.1 Audit Logs
Each pipeline execution generates a comprehensive audit log containing:
- Build metadata (number, timestamp, user)
- Input parameters
- Request payload (JSON)
- API response status and body
- Execution duration
- Final result (success/failure)

**Storage**: Jenkins artifacts (JSON format)

### 6.2 Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Success Rate** | % of successful executions | > 95% |
| **Execution Time** | Average time per operation | < 2 minutes |
| **Retry Rate** | % of operations requiring retry | < 10% |
| **Audit Log Coverage** | % of operations with complete logs | 100% |

---

## 7. Environment Management

### 7.1 Environment Segregation

| Environment | Purpose | URL Pattern | Access Control |
|-------------|---------|-------------|----------------|
| **Beta** | Development & Testing | `*.beta-dbx.commerceiq.ai` | Engineering, QA |
| **QA** | User Acceptance Testing | `*.qa-dbx.commerceiq.ai` | QA, Product, Select Ops |
| **Prod** | Production Operations | `*.prod-dbx.commerceiq.ai` | Operations, Senior Leadership |

### 7.2 Change Management
- **Beta → QA**: Automated promotion after test validation
- **QA → Prod**: Manual approval required (Change Control)
- **Emergency Changes**: Documented exception process

---

## 8. Scalability & Performance

### 8.1 Current Capacity
- **Concurrent Executions**: Limited by Jenkins agent pool
- **API Rate Limits**: Handled by retry logic
- **Audit Log Storage**: Unlimited (Jenkins artifacts)

### 8.2 Future Scalability Considerations
- Horizontal scaling via Jenkins agent pool expansion
- API rate limit monitoring and alerting
- Automated archive cleanup for old audit logs
- Caching for frequently accessed reference data

---

## 9. Integration Points

### 9.1 External Systems
- **Client Setup Platform API**: Primary integration for configuration management
- **Jenkins**: Orchestration and UI
- **Artifact Storage**: Audit log persistence

### 9.2 Future Integration Opportunities
- **Slack/Teams**: Real-time notifications
- **JIRA**: Ticket creation for failures
- **DataDog/Grafana**: Advanced monitoring dashboards
- **ServiceNow**: ITSM integration for change requests

---

## 10. Risk Assessment & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **API Key Compromise** | High | Low | Rotate keys regularly, audit access |
| **Incorrect Configuration** | Medium | Medium | Dry run mode, validation logic |
| **Service Downtime** | Medium | Low | Retry logic, multi-environment setup |
| **Audit Log Loss** | Low | Low | Jenkins backup strategy |
| **Human Error** | Medium | Medium | UI validation, dry run preview |

---

## 11. Disaster Recovery

### 11.1 Backup Strategy
- **Jenkins Configuration**: Version controlled (Infrastructure as Code)
- **Audit Logs**: Archived as Jenkins artifacts (retained per policy)
- **Pipeline Code**: Version controlled in Git

### 11.2 Recovery Procedures
- **Jenkins Failure**: Restore from Docker image + configuration
- **API Service Failure**: Retry mechanism handles transient failures
- **Configuration Loss**: Reconstruct from audit logs

---

## 12. Future Roadmap

### Phase 2 Enhancements
- [ ] Batch operations for bulk client onboarding
- [ ] Configuration drift detection
- [ ] Advanced approval workflows
- [ ] Integration with ServiceNow for change management

### Phase 3 Features
- [ ] Self-service portal with API key rotation
- [ ] Advanced analytics and reporting dashboards
- [ ] Multi-region API endpoint support
- [ ] Configuration templates and presets

---

## 13. Glossary

| Term | Definition |
|------|------------|
| **Instance** | A configured client environment |
| **Retailer** | E-commerce platform or marketplace |
| **Retailer Variant** | Specific integration type for a retailer |
| **Feature** | Functional capability that can be enabled/disabled |
| **Region** | Geographic market (country/region code) |
| **Product Line** | RMM or ESM service offering |
| **Dry Run** | Preview mode without executing changes |
| **Activation** | Making an instance or feature operational |

---

## 14. References & Related Documents

- [Detailed Design Document](./design_doc.md) - Technical specifications and implementation details
- [Jenkinsfile](./Jenkinsfile) - Pipeline source code
- [README](./readme.md) - Setup and installation instructions

---

## Approval & Review

| Role | Name | Date | Signature |
|------|------|------|-----------|
| **Author** | DevOps Team | 2025-11-03 | _Pending_ |
| **Technical Reviewer** | Engineering Lead | | _Pending_ |
| **Manager Approval** | Engineering Manager | | _Pending_ |
| **Director Approval** | Director of Engineering | | _Pending_ |

---

**Document Status**: Draft - Pending Review

