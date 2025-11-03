# Design Doc: Jenkins Pipeline for Client Setup Platform API Operations

**Author(s):**
**Date:**
**Status:** Draft

## 1. Introduction

*   **Problem:** There is a need for non-technical users to execute API operations on the Client Setup Platform without having to interact with the API directly. This reduces the need for technical intervention for routine tasks and empowers operational teams.

*   **Proposed Solution:** A Jenkins pipeline that provides a user-friendly interface to perform specific, predefined API operations. Users can select an operation, fill in the necessary parameters, and execute the task, while the pipeline handles the underlying API calls, validation, and error handling.

## 2. Goals and Non-Goals

### Goals

*   Provide a simple UI for non-technical users to perform client setup operations.
*   Automate the `onboardInstance` and `activateInstance` API calls.
*   Implement robust input validation to prevent errors.
*   Include a "dry run" mode to allow users to preview the API request without executing it.
*   Send email and Slack notifications to users upon completion or failure of an operation.
*   Maintain an audit log of all operations performed through the pipeline.

### Non-Goals

*   This pipeline is not intended to be a comprehensive replacement for the full Client Setup Platform API.
*   It will not support operations other than those explicitly listed in the parameters.
*   It does not manage the infrastructure of the Client Setup Platform itself.

## 3. Technical Design

The pipeline is defined in a `Jenkinsfile` and is composed of several stages, parameters, and helper functions.

### 3.1. Pipeline Architecture

The pipeline is structured into the following stages:

1.  **Initialize:** Displays a summary of the selected parameters and execution details.
2.  **Validate Parameters:** Ensures that all the required inputs are provided and are in the correct format.
3.  **Build API Request:** Constructs the API endpoint and the JSON payload based on the user's input.
4.  **Execute API Call:** Sends the request to the Client Setup Platform API. This stage is skipped if "Dry Run" is enabled.
5.  **Dry Run Summary:** If "Dry Run" is enabled, this stage displays the API request that would have been sent.
6.  **Display Results:** Shows the response from the API call. This stage is skipped if "Dry Run" is enabled.

The pipeline also includes a `post` block that executes after all stages are complete:
*   **success:** Sends a success notification.
*   **failure:** Sends a failure notification.
*   **always:** Archives an audit log of the operation.

### 3.2. Parameters

The pipeline accepts the following parameters from the user:

| Parameter | Type | Description |
|---|---|---|
| `X_API_KEY` | `password` | The API key for authentication. |
| `OPERATION` | `choice` | The operation to perform (`onboardInstance`, `activateInstance`). |
| `INSTANCE_NAME` | `string` | The name of the instance. |
| `REGION` | `choice` | The AWS region for the instance. |
| `RETAILER` | `choice` | The retailer associated with the instance. |
| `RETAILER_VARIANT` | `choice` | The retailer variant. |
| `PRODUCT_LINE` | `choice` | The product line (`RMM`, `ESM`). |
| `FEATURES` | `string` | A comma-separated list of features to enable. |
| `ACTIVATE` | `choice` | Whether to activate or deactivate the instance. |
| `ENABLE_DISABLE_ENTITY` | `choice` | The entity to enable or disable. |
| `DRY_RUN` | `boolean` | If checked, the pipeline will not execute the API call. |

### 3.3. API Interaction

*   **Endpoint Construction:** The `buildEndpoint` function dynamically creates the API endpoint URL based on the selected `OPERATION`.
*   **Payload Construction:** The `buildPayload` function assembles the JSON payload for the API request, including all the relevant parameters provided by the user.
*   **API Execution:** The `executeAPICall` function is responsible for making the HTTP POST request. It includes a retry mechanism (up to 3 retries) to handle transient network issues.

## 4. Security Considerations

*   The `X_API_KEY` is handled using Jenkins's `password` parameter type, which masks the value in the Jenkins UI and console logs to prevent exposure.

## 5. Testing Plan

*   The "Dry Run" feature serves as a primary testing mechanism, allowing for verification of the generated API request payload and endpoint before any actual changes are made.

## 6. Rollout Plan

*   The pipeline can be deployed to a Jenkins server.
*   Users will need to be provided with the URL to the Jenkins job.
*   Documentation should be provided to users on how to fill out the parameters for each operation.

## 7. Appendix

*   [Link to Jenkinsfile](/Users/adityakumar/Personal/repos/jenkins-dev/Jenkinsfile)

