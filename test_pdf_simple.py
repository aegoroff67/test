#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

# Test PDF generation with a simple request
def test_pdf_simple():
    base_url = "https://aimatrix-assess.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    # First, create a user and get token
    timestamp = datetime.now().strftime('%H%M%S')
    test_email = f"pdf_test_{timestamp}@example.com"
    
    signup_data = {
        "name": f"PDF Test User {timestamp}",
        "email": test_email,
        "password": "TestPass123!",
        "organization_name": f"PDF Test Org {timestamp}",
        "industry": "Technology"
    }
    
    print("🔍 Creating test user...")
    response = requests.post(f"{api_url}/auth/signup", json=signup_data)
    if response.status_code != 200:
        print(f"❌ Signup failed: {response.status_code} - {response.text}")
        return False
    
    token = response.json()['access_token']
    print("✅ User created and authenticated")
    
    # Create assessment
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = requests.post(f"{api_url}/assessments", json={}, headers=headers)
    if response.status_code != 200:
        print(f"❌ Assessment creation failed: {response.status_code} - {response.text}")
        return False
    
    assessment_id = response.json()['id']
    print(f"✅ Assessment created: {assessment_id}")
    
    # Get questions and answer them quickly
    response = requests.get(f"{api_url}/assessments/{assessment_id}/questions", headers=headers)
    if response.status_code != 200:
        print(f"❌ Get questions failed: {response.status_code} - {response.text}")
        return False
    
    questions_data = response.json()
    all_questions = []
    for domain_data in questions_data:
        questions = domain_data.get('questions', [])
        all_questions.extend(questions)
    
    print(f"✅ Retrieved {len(all_questions)} questions")
    
    # Answer all questions
    for i, question in enumerate(all_questions):
        answer_data = {
            "question_id": question['id'],
            "option": "GOOD",
            "note": f"Quick test answer {i+1}"
        }
        
        response = requests.post(f"{api_url}/assessments/{assessment_id}/answer", 
                               json=answer_data, headers=headers)
        if response.status_code != 200:
            print(f"❌ Answer {i+1} failed: {response.status_code}")
            return False
    
    print(f"✅ Answered all {len(all_questions)} questions")
    
    # Submit assessment
    response = requests.post(f"{api_url}/assessments/{assessment_id}/submit", 
                           json={}, headers=headers)
    if response.status_code != 200:
        print(f"❌ Submit failed: {response.status_code} - {response.text}")
        return False
    
    print("✅ Assessment submitted")
    
    # Test PDF generation
    print("🔍 Testing PDF generation...")
    response = requests.get(f"{api_url}/assessments/{assessment_id}/report", 
                          headers=headers, timeout=60)
    
    print(f"📊 PDF Response Status: {response.status_code}")
    print(f"📊 Content-Type: {response.headers.get('content-type', 'Not set')}")
    print(f"📊 Content-Disposition: {response.headers.get('content-disposition', 'Not set')}")
    
    if response.status_code == 200:
        pdf_size = len(response.content)
        print(f"📊 PDF Size: {pdf_size} bytes")
        
        if response.content.startswith(b'%PDF'):
            print("✅ Valid PDF format detected")
            return True
        else:
            print("❌ Invalid PDF format")
            print(f"First 100 bytes: {response.content[:100]}")
            return False
    else:
        print(f"❌ PDF generation failed: {response.text}")
        return False

if __name__ == "__main__":
    success = test_pdf_simple()
    if success:
        print("🎉 PDF generation test passed!")
    else:
        print("💥 PDF generation test failed!")