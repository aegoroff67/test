#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

def test_pdf_error_handling():
    base_url = "https://pdf-report-fixer.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    # Create user and get token
    timestamp = datetime.now().strftime('%H%M%S')
    test_email = f"error_test_{timestamp}@example.com"
    
    signup_data = {
        "name": f"Error Test User {timestamp}",
        "email": test_email,
        "password": "TestPass123!",
        "organization_name": f"Error Test Org {timestamp}",
        "industry": "Technology"
    }
    
    print("🔍 Creating test user...")
    response = requests.post(f"{api_url}/auth/signup", json=signup_data)
    if response.status_code != 200:
        print(f"❌ Signup failed: {response.status_code} - {response.text}")
        return False
    
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    print("✅ User created and authenticated")
    
    # Test 1: Non-existent assessment
    print("\n🔍 Testing non-existent assessment...")
    fake_id = "non-existent-assessment-id"
    response = requests.get(f"{api_url}/assessments/{fake_id}/report", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test 2: Incomplete assessment
    print("\n🔍 Testing incomplete assessment...")
    response = requests.post(f"{api_url}/assessments", json={}, headers=headers)
    if response.status_code == 200:
        assessment_id = response.json()['id']
        print(f"Created assessment: {assessment_id}")
        
        # Try to generate PDF without completing assessment
        response = requests.get(f"{api_url}/assessments/{assessment_id}/report", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    
    return True

if __name__ == "__main__":
    test_pdf_error_handling()