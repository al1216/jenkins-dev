#!/usr/bin/env python3
"""
Client Setup Platform API Handler
Handles API operations for Jenkins automation
"""

import os
import sys
import json
import requests
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'api_handler_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)


class Operation(Enum):
    """Supported operations"""
    ONBOARD = "onboardInstance"
    ACTIVATE = "activateInstance"
    DEACTIVATE = "deactivateInstance"
    UPDATE = "updateInstance"


class APIResponse:
    """API response wrapper"""
    def __init__(self, success: bool, status_code: Optional[int] = None, 
                 data: Optional[Dict] = None, error: Optional[str] = None):
        self.success = success
        self.status_code = status_code
        self.data = data or {}
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'status_code': self.status_code,
            'data': self.data,
            'error': self.error
        }


class ClientSetupAPIHandler:
    """Handler for Client Setup Platform API operations"""
    
    def __init__(self, base_url: str, x_api_key: str, timeout: int = 30, 
                 retry_count: int = 3, retry_backoff: int = 5):
        self.base_url = base_url.rstrip('/')
        self.x_api_key = x_api_key
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_backoff = retry_backoff
        
        # Initialize session
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': x_api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'Jenkins-API-Automation/1.0'
        })
    
    def execute_operation(self, operation: str, payload: Dict[str, Any]) -> APIResponse:
        """Execute an API operation"""
        logger.info(f"Executing operation: {operation}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Map operation to endpoint
        endpoint_map = {
            Operation.ONBOARD.value: '/api/v1/instance-controller/onboard',
            Operation.ACTIVATE.value: '/api/v1/instance-controller/activate',
            Operation.DEACTIVATE.value: '/api/v1/instance-controller/deactivate',
            Operation.UPDATE.value: '/api/v1/instance-controller/update'
        }
        
        endpoint = endpoint_map.get(operation)
        if not endpoint:
            return APIResponse(success=False, error=f"Unknown operation: {operation}")
        
        url = f"{self.base_url}{endpoint}"
        
        # Determine HTTP method
        method = 'PUT' if operation == Operation.UPDATE.value else 'POST'
        
        # Execute with retry logic
        return self._execute_with_retry(method, url, payload)
    
    def _execute_with_retry(self, method: str, url: str, 
                           payload: Dict[str, Any]) -> APIResponse:
        """Execute request with retry logic"""
        last_error = None
        
        for attempt in range(1, self.retry_count + 1):
            try:
                logger.info(f"Attempt {attempt} of {self.retry_count}")
                logger.info(f"Making {method} request to {url}")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    json=payload,
                    timeout=self.timeout
                )
                
                # Log response
                logger.info(f"Response Status: {response.status_code}")
                logger.info(f"Response Headers: {dict(response.headers)}")
                logger.info(f"Response Body: {response.text}")
                
                # Check if successful
                response.raise_for_status()
                
                # Parse response
                data = response.json() if response.content else {}
                
                return APIResponse(
                    success=True,
                    status_code=response.status_code,
                    data=data
                )
                
            except requests.exceptions.Timeout as e:
                last_error = f"Request timeout: {str(e)}"
                logger.warning(f"Attempt {attempt} failed: {last_error}")
                
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                error_body = e.response.text
                
                last_error = f"HTTP {status_code}: {error_body}"
                logger.error(f"Attempt {attempt} failed: {last_error}")
                
                # Don't retry on 4xx errors (client errors)
                if 400 <= status_code < 500:
                    return APIResponse(
                        success=False,
                        status_code=status_code,
                        error=last_error
                    )
                
            except requests.exceptions.RequestException as e:
                last_error = f"Request failed: {str(e)}"
                logger.error(f"Attempt {attempt} failed: {last_error}")
            
            # Wait before retry (exponential backoff)
            if attempt < self.retry_count:
                wait_time = self.retry_backoff * (2 ** (attempt - 1))
                logger.info(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
        
        # All retries failed
        return APIResponse(success=False, error=last_error)


class ParameterValidator:
    """Validate input parameters"""
    
    @staticmethod
    def validate_instance_name(name: str) -> bool:
        """Validate instance name format"""
        if not name or not isinstance(name, str):
            logger.error("Instance name is required")
            return False
        
        if len(name) < 3 or len(name) > 50:
            logger.error("Instance name must be between 3 and 50 characters")
            return False
        
        if not all(c.isalnum() or c in '-_' for c in name):
            logger.error("Instance name can only contain alphanumeric characters, hyphens, and underscores")
            return False
        
        return True
    
    @staticmethod
    def validate_required_fields(params: Dict[str, Any], required: list) -> bool:
        """Validate required fields are present"""
        for field in required:
            if field not in params or params[field] is None:
                logger.error(f"Missing required field: {field}")
                return False
        return True
    
    @staticmethod
    def validate_all(params: Dict[str, Any]) -> bool:
        """Validate all parameters"""
        # Check required fields
        if not ParameterValidator.validate_required_fields(
            params, ['operation', 'instanceName']
        ):
            return False
        
        # Validate instance name
        if not ParameterValidator.validate_instance_name(params['instanceName']):
            return False
        
        # Validate operation
        valid_operations = [op.value for op in Operation]
        if params['operation'] not in valid_operations:
            logger.error(f"Invalid operation: {params['operation']}")
            return False
        
        return True


def build_payload(params: Dict[str, Any]) -> Dict[str, Any]:
    """Build API payload from parameters"""
    payload = {
        'instanceName': params.get('instanceName'),
        'region': params.get('region'),
        'retailer': params.get('retailer'),
        'retailerVariant': params.get('retailerVariant'),
        'activate': params.get('activate', 'false').lower() == 'true',
        'enableDisableEntity': params.get('enableDisableEntity', 'all'),
        'metadata': {
            'executedBy': params.get('executedBy', 'System'),
            'buildNumber': params.get('buildNumber'),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    }
    
    # Remove None values
    return {k: v for k, v in payload.items() if v is not None}


def print_banner():
    """Print execution banner"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  CLIENT SETUP PLATFORM API HANDLER                            ║
║  Version 1.0                                                  ║
╚═══════════════════════════════════════════════════════════════╝
""")


def print_results(response: APIResponse, params: Dict[str, Any], duration: float):
    """Print execution results"""
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║  {'✅ OPERATION COMPLETED SUCCESSFULLY' if response.success else '❌ OPERATION FAILED':^61} ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Status Code      : {response.status_code or 'N/A':43} ║
║  Instance Name    : {params.get('instanceName', 'N/A'):43} ║
║  Operation        : {params.get('operation', 'N/A'):43} ║
║  Duration         : {duration:.2f} seconds{' ' * (43 - len(f'{duration:.2f} seconds'))} ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    if response.success:
        print("Response Data:")
        print(json.dumps(response.data, indent=2))
    else:
        print(f"Error: {response.error}")


def main():
    """Main execution function"""
    print_banner()
    
    # Get parameters from environment variables (set by Jenkins)
    params = {
        'operation': os.getenv('OPERATION'),
        'instanceName': os.getenv('INSTANCE_NAME'),
        'region': os.getenv('REGION'),
        'retailer': os.getenv('RETAILER'),
        'retailerVariant': os.getenv('RETAILER_VARIANT'),
        'activate': os.getenv('ACTIVATE'),
        'enableDisableEntity': os.getenv('ENABLE_DISABLE_ENTITY'),
        'executedBy': os.getenv('BUILD_USER', 'System'),
        'buildNumber': os.getenv('BUILD_NUMBER')
    }
    
    logger.info(f"Parameters: {json.dumps(params, indent=2)}")
    
    # Get API configuration
    api_base_url = os.getenv('API_BASE_URL', 
                             'http://client-setup-platform.beta-dbx.commerceiq.ai')
    x_api_key = os.getenv('X_API_KEY')
    
    if not x_api_key:
        logger.error("❌ X_API_KEY environment variable not set!")
        sys.exit(1)
    
    # Validate parameters
    logger.info("🔍 Validating parameters...")
    if not ParameterValidator.validate_all(params):
        logger.error("❌ Parameter validation failed!")
        sys.exit(1)
    logger.info("✅ Parameters validated successfully")
    
    # Build payload
    logger.info("🔨 Building API payload...")
    payload = build_payload(params)
    logger.info(f"Payload: {json.dumps(payload, indent=2)}")
    
    # Initialize API handler
    logger.info("🚀 Initializing API handler...")
    api_handler = ClientSetupAPIHandler(
        base_url=api_base_url,
        x_api_key=x_api_key,
        timeout=int(os.getenv('TIMEOUT_SECONDS', '30')),
        retry_count=int(os.getenv('RETRY_COUNT', '3')),
        retry_backoff=int(os.getenv('RETRY_BACKOFF', '5'))
    )
    
    # Execute operation
    logger.info("⚡ Executing operation...")
    start_time = time.time()
    result = api_handler.execute_operation(params['operation'], payload)
    duration = time.time() - start_time
    
    # Print results
    print_results(result, params, duration)
    
    # Save result to file for Jenkins
    result_file = f"api_result_{os.getenv('BUILD_NUMBER', 'unknown')}.json"
    with open(result_file, 'w') as f:
        json.dump(result.to_dict(), f, indent=2)
    logger.info(f"Results saved to {result_file}")
    
    # Exit with appropriate code
    sys.exit(0 if result.success else 1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)

