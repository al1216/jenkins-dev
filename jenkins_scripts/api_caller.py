#!/usr/bin/env python3
"""
API Caller Script for Jenkins
Handles HTTP requests with retry logic when HTTP Request Plugin is not available
"""

import sys
import json
import time
import argparse
import urllib.request
import urllib.error
import ssl
from typing import Dict, Any, Tuple


class APIResponse:
    """Simple response object to mimic httpRequest response"""
    def __init__(self, status: int, content: str):
        self.status = status
        self.content = content


def make_api_call(
    url: str,
    payload: Dict[str, Any],
    api_key: str,
    timeout: int = 30,
    max_retries: int = 3,
    ignore_ssl: bool = True
) -> Tuple[int, str]:
    """
    Make an API call with retry logic
    
    Args:
        url: The full API endpoint URL
        payload: The JSON payload to send
        api_key: The X-API-Key header value
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        ignore_ssl: Whether to ignore SSL certificate errors
        
    Returns:
        Tuple of (status_code, response_body)
    """
    
    # Prepare request
    data = json.dumps(payload).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key
    }
    
    # Create SSL context if needed
    ssl_context = None
    if ignore_ssl:
        ssl_context = ssl._create_unverified_context()
    
    last_error = None
    retry_count = 0
    
    while retry_count < max_retries:
        if retry_count > 0:
            wait_time = retry_count * 5
            print(f"🔄 Retry attempt {retry_count + 1} of {max_retries}", file=sys.stderr)
            print(f"⏳ Waiting {wait_time} seconds before retry...", file=sys.stderr)
            time.sleep(wait_time)
        
        try:
            # Create request
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            
            # Make the request
            if ssl_context:
                response = urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
            else:
                response = urllib.request.urlopen(req, timeout=timeout)
            
            # Read response
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            
            if 200 <= status_code < 300:
                print(f"✅ Response Status: {status_code}", file=sys.stderr)
                print(f"📄 Raw Response: {response_body}", file=sys.stderr)
                return status_code, response_body
            else:
                last_error = f"Status: {status_code}, Body: {response_body}"
                print(f"❌ API call failed. {last_error}", file=sys.stderr)
                retry_count += 1
                
        except urllib.error.HTTPError as e:
            status_code = e.code
            try:
                response_body = e.read().decode('utf-8')
            except:
                response_body = str(e)
            
            last_error = f"HTTP Error {status_code}: {response_body}"
            print(f"❌ API call failed. {last_error}", file=sys.stderr)
            retry_count += 1
            
        except urllib.error.URLError as e:
            last_error = f"URL Error: {str(e.reason)}"
            print(f"❌ API call failed. {last_error}", file=sys.stderr)
            retry_count += 1
            
        except Exception as e:
            last_error = f"Unexpected error: {str(e)}"
            print(f"❌ API call failed. {last_error}", file=sys.stderr)
            retry_count += 1
    
    # All retries failed
    error_msg = f"❌ All {max_retries} attempts failed. Last error: {last_error}"
    print(error_msg, file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Make HTTP API calls with retry logic for Jenkins'
    )
    parser.add_argument('--url', required=True, help='API endpoint URL')
    parser.add_argument('--payload', required=True, help='JSON payload as string')
    parser.add_argument('--api-key', required=True, help='X-API-Key header value')
    parser.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds')
    parser.add_argument('--max-retries', type=int, default=3, help='Maximum retry attempts')
    parser.add_argument('--ignore-ssl', action='store_true', default=True, help='Ignore SSL errors')
    
    args = parser.parse_args()
    
    # Parse payload
    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON payload: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"🚀 Executing API call to {args.url}...", file=sys.stderr)
    
    # Make the API call
    status_code, response_body = make_api_call(
        url=args.url,
        payload=payload,
        api_key=args.api_key,
        timeout=args.timeout,
        max_retries=args.max_retries,
        ignore_ssl=args.ignore_ssl
    )
    
    # Output result as JSON for Jenkins to parse
    result = {
        'status': status_code,
        'content': response_body
    }
    print(json.dumps(result))


if __name__ == '__main__':
    main()

