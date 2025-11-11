#!/usr/bin/env python3
"""
Test script for api_caller.py
Use this to verify the API caller works before deploying to Jenkins
"""

import json
import subprocess
import sys
from pathlib import Path


def test_api_caller():
    """Test the API caller with httpbin.org (a test API)"""
    
    script_dir = Path(__file__).parent
    api_caller = script_dir / "api_caller.py"
    
    if not api_caller.exists():
        print(f"❌ Error: api_caller.py not found at {api_caller}")
        sys.exit(1)
    
    # Test payload
    test_payload = {
        "user": "test@example.com",
        "metadata": {
            "test": True,
            "timestamp": "2025-01-01T00:00:00Z"
        },
        "instanceName": "test-instance"
    }
    
    # Test with httpbin.org (a safe test endpoint)
    test_url = "https://httpbin.org/post"
    test_api_key = "test-key-12345"
    
    print("=" * 60)
    print("Testing API Caller Script")
    print("=" * 60)
    print(f"\n📝 Test Configuration:")
    print(f"   URL: {test_url}")
    print(f"   Payload: {json.dumps(test_payload, indent=2)}")
    print(f"   API Key: {test_api_key}")
    print(f"\n🚀 Executing test...\n")
    
    try:
        # Run the API caller
        result = subprocess.run(
            [
                "python3",
                str(api_caller),
                "--url", test_url,
                "--payload", json.dumps(test_payload),
                "--api-key", test_api_key,
                "--timeout", "10",
                "--max-retries", "2"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Print stderr (progress messages)
        if result.stderr:
            print("📊 Progress Log:")
            print("-" * 60)
            print(result.stderr)
            print("-" * 60)
        
        # Check exit code
        if result.returncode != 0:
            print(f"\n❌ Test FAILED with exit code {result.returncode}")
            sys.exit(1)
        
        # Parse and display results
        try:
            response = json.loads(result.stdout)
            print(f"\n✅ Test PASSED!")
            print(f"\n📦 Response:")
            print(f"   Status Code: {response['status']}")
            print(f"   Response Body:")
            
            # Pretty print the response body if it's JSON
            try:
                body = json.loads(response['content'])
                print(json.dumps(body, indent=2))
            except:
                print(f"   {response['content']}")
                
        except json.JSONDecodeError as e:
            print(f"\n❌ Failed to parse response JSON: {e}")
            print(f"Raw output: {result.stdout}")
            sys.exit(1)
            
    except subprocess.TimeoutExpired:
        print("\n❌ Test FAILED: Timeout after 30 seconds")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test FAILED with error: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All tests passed successfully!")
    print("=" * 60)
    print("\nℹ️  The API caller is ready to use in Jenkins")


if __name__ == '__main__':
    test_api_caller()

